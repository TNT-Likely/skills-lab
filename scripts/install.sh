#!/usr/bin/env bash
# 把 skills/<name>/ 安装到 Agent 技能目录。
# 默认用软链，仓库更新后无需重新安装；--copy 用于需要独立副本的场景。
set -eo pipefail

ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
MODE=symlink
FORCE=0
LIST=0
TARGETS=()
WANTED=()

die() {
  printf '错误: %s\n' "$*" >&2
  exit 1
}

usage() {
  cat <<'EOF'
用法: ./scripts/install.sh [选项] [skill...]

把 skills/<name>/ 安装到 Agent 技能目录。默认安装全部技能并使用软链，
skills-lab 更新后无需重新安装，新开 Agent 会话即可生效。

选项:
  --target DIR   安装到指定目录，可重复；默认 ~/.agents/skills 与 ~/.claude/skills
  --copy         复制而不是软链（复制后需重新运行才能同步更新）
  --force        覆盖已存在的同名目录或指向别处的软链
  --list         列出仓库中的技能
  -h, --help     显示帮助

示例:
  ./scripts/install.sh
  ./scripts/install.sh portal-dashboard
  ./scripts/install.sh --copy --target ~/.agents/skills
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --target)
      [ $# -ge 2 ] || die "--target 需要一个目录"
      TARGETS+=("$2")
      shift 2
      ;;
    --target=*)
      TARGETS+=("${1#*=}")
      shift
      ;;
    --copy)
      MODE=copy
      shift
      ;;
    --force)
      FORCE=1
      shift
      ;;
    --list)
      LIST=1
      shift
      ;;
    -h | --help)
      usage
      exit 0
      ;;
    --)
      shift
      while [ $# -gt 0 ]; do
        WANTED+=("$1")
        shift
      done
      ;;
    -*)
      die "未知选项: $1（用 --help 查看用法）"
      ;;
    *)
      WANTED+=("$1")
      shift
      ;;
  esac
done

ALL=()
for dir in "$ROOT"/skills/*/; do
  [ -f "${dir}SKILL.md" ] || continue
  ALL+=("$(basename "$dir")")
done
[ ${#ALL[@]} -gt 0 ] || die "skills/ 下没有找到含 SKILL.md 的技能"

if [ "$LIST" -eq 1 ]; then
  printf '%s\n' "${ALL[@]}"
  exit 0
fi

if [ ${#WANTED[@]} -gt 0 ]; then
  for name in "${WANTED[@]}"; do
    found=0
    for known in "${ALL[@]}"; do
      [ "$known" = "$name" ] && found=1
    done
    [ "$found" -eq 1 ] || die "技能不存在: $name（可选: ${ALL[*]}）"
  done
  SKILLS=("${WANTED[@]}")
else
  SKILLS=("${ALL[@]}")
fi

if [ ${#TARGETS[@]} -eq 0 ]; then
  TARGETS=("$HOME/.agents/skills" "$HOME/.claude/skills")
fi

failed=0
for target in "${TARGETS[@]}"; do
  case "$target" in
    "~/"*) target="$HOME/${target#\~/}" ;;
  esac
  mkdir -p "$target"
  printf '→ %s\n' "$target"

  for name in "${SKILLS[@]}"; do
    src="$ROOT/skills/$name"
    dest="$target/$name"

    if [ -L "$dest" ]; then
      current=$(readlink "$dest" || true)
      if [ "$current" = "$src" ]; then
        printf '  ✓ %s 已链接\n' "$name"
        continue
      fi
      if [ "$FORCE" -ne 1 ]; then
        printf '  ! %s 已存在并指向 %s（用 --force 覆盖）\n' "$name" "$current" >&2
        failed=1
        continue
      fi
      rm -f "$dest"
    elif [ -e "$dest" ]; then
      if [ "$FORCE" -ne 1 ]; then
        printf '  ! %s 已存在（用 --force 覆盖）\n' "$name" >&2
        failed=1
        continue
      fi
      rm -rf "$dest"
    fi

    if [ "$MODE" = copy ]; then
      cp -R "$src" "$dest"
      printf '  ✓ %s 已复制\n' "$name"
    else
      ln -s "$src" "$dest"
      printf '  ✓ %s 已链接\n' "$name"
    fi
  done
done

if [ "$failed" -ne 0 ]; then
  exit 1
fi

printf '\n完成。新开 Agent 会话即可使用；软链安装会跟随 skills-lab 的更新。\n'

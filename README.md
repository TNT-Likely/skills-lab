# skills-lab

一个可以持续收集、验证和分享 Agent Skills 的小仓库。每个 Skill 都放在 `skills/<name>/` 下，默认中文，英文说明放在对应的 `README.en.md` 或仓库级英文文档中。

当前第一个 Skill 是 [`flow-builder`](skills/flow-builder/SKILL.md)：它帮助 Agent 把业务流程、截图、HTML、表格或口述需求，整理成可以真正操作的系统原型。它不只生成流程图，也关注表单、CRUD、台账、状态流转、角色视图、异常处理、追溯和未来代码迁移。

第二个 Skill 是 [`portal-dashboard`](skills/portal-dashboard/SKILL.md)：一套「Clash 面板风」的文档优先门户视觉系统（暖灰底、近白卡片、iOS 蓝、大圆角胶囊、tabular 数字），用于本地知识库 / 脚本门户首页。附带 [`assets/starter.html`](skills/portal-dashboard/assets/starter.html) 自包含起步模板（零依赖、file:// 直开）与 [`references/measurements.md`](skills/portal-dashboard/references/measurements.md) 采样记录。

![flow-builder demo](examples/demo.gif)

## 示例

[`examples/mfg-procurement-to-assembly.html`](examples/mfg-procurement-to-assembly.html) 是一个脱敏的制造流程示例，展示零部件从采购、到货、质检、入库、领料、装配绑定、下线放行、交付到售后反查的交互式图表。它只使用合成业务数据，不包含飞书地址、访问令牌或内部路径。

[`examples/mfg-vcu-after-sales-replacement.html`](examples/mfg-vcu-after-sales-replacement.html) 是一个更小的纵向切片，专门演示售后 VCU 换件：飞书任务、VIN/旧件查询、新件校验、UDS/蓝牙写入、读回、Melon 换件事务、任务回写和反向追溯。配套的 [中文实施计划](examples/mfg-vcu-after-sales-implementation-plan.md) 和 [English plan](examples/mfg-vcu-after-sales-implementation-plan.en.md) 说明了职责边界、接口顺序、数据主权、迁移路径和验收矩阵。

本地预览：

```bash
python3 -m http.server 8792 --directory examples
# 浏览器打开 http://127.0.0.1:8792/mfg-procurement-to-assembly.html
```

## 安装

### 通用安装（推荐）

跨 Agent 用 [`npx skills`](https://skills.sh)，默认软链：一份 canonical 副本在 `~/.agents/skills/<name>`，Claude Code 通过 `~/.claude/skills/<name>` 链过去。

```bash
# 全部技能 → Claude Code + Codex
npx skills add TNT-Likely/skills-lab -g -a claude-code -a codex --skill '*' -y

# 只装一个
npx skills add TNT-Likely/skills-lab --skill flow-builder -g -a claude-code -a codex -y

# 仓库更新后（全局安装）
npx skills update -g
```

`--copy` 可改为复制；复制模式同样用 `npx skills update` 同步，不是重新安装。

### Claude Code 插件市场

```text
/plugin marketplace add TNT-Likely/skills-lab
/plugin install flow-builder@skills-lab
/plugin install portal-dashboard@skills-lab
```

由 Claude Code 的 `/plugin` 管理更新；Claude Code 用户不需要再跑 `npx skills`。

### 本地开发（直链仓库）

```bash
git clone https://github.com/tnt-likely/skills-lab.git
cd skills-lab
./scripts/install.sh               # 全部技能 → ~/.agents/skills + ~/.claude/skills
./scripts/install.sh flow-builder  # 只装一个
./scripts/install.sh --copy        # 需要独立副本时
```

工作树就是源：改文件或 `git pull` 后，新开 Agent 会话即生效，**不需要 update**。适合自己持续编辑；对外分发用上面的 `npx skills` 或插件市场。

- 默认软链而不是硬链：git 拉取/切换会替换文件 inode，硬链会失效，也覆盖不了之后新增的 `assets/`、`references/`。
- 同名目录已存在时脚本拒绝覆盖；确认后用 `--force`。
- 多技能仓库不保留根 `SKILL.md`：`npx skills` 遇到根技能时只识别它、忽略 `skills/`。每个技能都在 `skills/<name>/SKILL.md`。

## 目录

```text
skills-lab/
├── README.md
├── README.en.md
├── .claude-plugin/
│   └── marketplace.json
├── skills/
│   ├── flow-builder/
│   │   └── SKILL.md
│   └── portal-dashboard/
│       ├── SKILL.md
│       ├── assets/
│       │   └── starter.html
│       └── references/
│           └── measurements.md
├── examples/
│   ├── demo.gif
│   └── mfg-procurement-to-assembly.html
└── scripts/
    ├── install.sh
    └── validate.py
```

## 发布约定

示例必须使用合成数据。提交前检查 HTML、文档、图片和脚本中是否包含私有 URL、令牌、个人路径或未授权业务资料。

## License

MIT

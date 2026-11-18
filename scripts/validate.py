#!/usr/bin/env python3
"""Small publication check for the skills-lab repository."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    ROOT / "README.md",
    ROOT / "README.en.md",
    ROOT / "SKILL.md",
    ROOT / "skills/flow-builder/SKILL.md",
    ROOT / "examples/demo.gif",
    ROOT / "examples/mfg-procurement-to-assembly.html",
    ROOT / "LICENSE",
]
missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
if missing:
    raise SystemExit(f"missing required files: {', '.join(missing)}")

for skill in (ROOT / "SKILL.md", ROOT / "skills/flow-builder/SKILL.md"):
    text = skill.read_text(encoding="utf-8")
    if not re.search(r"^name: flow-builder$", text, re.M):
        raise SystemExit(f"invalid skill name: {skill}")
    if not re.search(r"^description: Use when .+", text, re.M):
        raise SystemExit(f"invalid skill description: {skill}")

html = (ROOT / "examples/mfg-procurement-to-assembly.html").read_text(encoding="utf-8")
if "<!-        <g id=\"node-demand\"" in html:
    raise SystemExit("commented demand node")
nodes = set(re.findall(r'data-node-id="([^"]+)"', html))
edges = re.findall(r'data-edge-from="([^"]+)" data-edge-to="([^"]+)"', html)
if len(nodes) < 15:
    raise SystemExit(f"expected at least 15 nodes, found {len(nodes)}")
unknown = [(a, b) for a, b in edges if a not in nodes or b not in nodes]
if unknown:
    raise SystemExit(f"edge endpoints missing: {unknown}")
if not re.search(r"售后|服务|维修|换件|反查", html):
    raise SystemExit("example has no after-sales trace language")
for forbidden in ("bytedance.larkoffice.com", "feishu.cn", "/Users/zcj/", "TL4Ebo3q"):
    if forbidden in html:
        raise SystemExit(f"private material found: {forbidden}")

print(f"validated {len(nodes)} nodes, {len(edges)} edges, required files present")

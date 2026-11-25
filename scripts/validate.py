#!/usr/bin/env python3
"""Small publication check for the skills-lab repository."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    ROOT / "README.md",
    ROOT / "README.en.md",
    ROOT / ".claude-plugin/marketplace.json",
    ROOT / "skills/portal-dashboard/SKILL.md",
    ROOT / "examples/demo.gif",
    ROOT / "examples/mfg-procurement-to-assembly.html",
    ROOT / "examples/mfg-vcu-after-sales-replacement.html",
    ROOT / "examples/mfg-vcu-after-sales-implementation-plan.md",
    ROOT / "examples/mfg-vcu-after-sales-implementation-plan.en.md",
    ROOT / "scripts/install.sh",
    ROOT / "LICENSE",
]
missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
if missing:
    raise SystemExit(f"missing required files: {', '.join(missing)}")

skill = ROOT / "skills/portal-dashboard/SKILL.md"
text = skill.read_text(encoding="utf-8")
if not re.search(r"^name: portal-dashboard$", text, re.M):
    raise SystemExit(f"invalid skill name: {skill}")
if not re.search(r"^description: Use when .+", text, re.M):
    raise SystemExit(f"invalid skill description: {skill}")

marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
plugins = {p.get("name"): p for p in marketplace.get("plugins", [])}
for name in ("portal-dashboard",):
    if name not in plugins:
        raise SystemExit(f"marketplace missing plugin: {name}")
    for rel in plugins[name].get("skills", []):
        if not (ROOT / rel / "SKILL.md").exists():
            raise SystemExit(f"marketplace skill path missing: {rel}")

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

vcu_html = (ROOT / "examples/mfg-vcu-after-sales-replacement.html").read_text(encoding="utf-8")
vcu_plan = (ROOT / "examples/mfg-vcu-after-sales-implementation-plan.md").read_text(encoding="utf-8")
for marker in ("执行成功换件", "模拟校验失败", "反向追溯", "Melon", "飞书", "UDS", "READBACK", "idempotency"):
    if marker not in vcu_html and marker not in vcu_plan:
        raise SystemExit(f"VCU example missing marker: {marker}")
for forbidden in ("bytedance.larkoffice.com", "feishu.cn", "/Users/zcj/", "TL4Ebo3q"):
    if forbidden in vcu_html or forbidden in vcu_plan:
        raise SystemExit(f"private material found in VCU example: {forbidden}")
vcu_nodes = len(__import__("re").findall(r'data-node-id="', vcu_html))
if vcu_nodes < 10:
    raise SystemExit(f"expected at least 10 VCU flow nodes, found {vcu_nodes}")

print(f"validated {len(nodes)} nodes, {len(edges)} edges, required files present")

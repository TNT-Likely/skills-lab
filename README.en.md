# skills-lab

A small public collection of Agent Skills that can be added, tested, and shared over time. Each skill lives under `skills/<name>/`; Chinese is the default language and English documentation is provided here.

The first skill is [`flow-builder`](skills/flow-builder/SKILL.md). It helps an agent turn a business process, screenshot, HTML reference, spreadsheet, or rough request into an interactive system prototype. It covers more than diagrams: forms, CRUD, ledgers, state transitions, role views, exception handling, traceability, and a path toward production code.

The second skill is [`portal-dashboard`](skills/portal-dashboard/SKILL.md): a "Clash-panel-inspired" docs-first portal visual system (warm gray background, near-white cards, iOS blue, large-radius pills, tabular numerals) for local knowledge-base / script portal home pages. It ships with a self-contained [`assets/starter.html`](skills/portal-dashboard/assets/starter.html) starter template (zero dependencies, opens directly from `file://`) and [`references/measurements.md`](skills/portal-dashboard/references/measurements.md) sampling records.

![flow-builder demo](examples/demo.gif)

## Example

[`examples/mfg-procurement-to-assembly.html`](examples/mfg-procurement-to-assembly.html) is a sanitized manufacturing example. It shows a component moving through purchasing, receipt, inspection, inventory, picking, installation binding, release, delivery, service lookup, and replacement trace. It uses synthetic data only and contains no private Feishu URL, token, or local path.

[`examples/mfg-vcu-after-sales-replacement.html`](examples/mfg-vcu-after-sales-replacement.html) is a smaller vertical slice for an after-sales VCU replacement. It covers the Feishu task, VIN and old-part lookup, new-part validation, UDS/BLE write, readback, the Melon replacement transaction, task callback, and reverse trace. The [Chinese implementation plan](examples/mfg-vcu-after-sales-implementation-plan.md) and [English plan](examples/mfg-vcu-after-sales-implementation-plan.en.md) describe ownership, API order, data authority, migration, and acceptance cases.

Preview locally:

```bash
python3 -m http.server 8792 --directory examples
# Open http://127.0.0.1:8792/mfg-procurement-to-assembly.html
```

## Installation

### Codex

```bash
mkdir -p ~/.codex/skills/flow-builder
curl -L https://raw.githubusercontent.com/tnt-likely/skills-lab/main/skills/flow-builder/SKILL.md \
  -o ~/.codex/skills/flow-builder/SKILL.md
```

### Claude Code / Gemini CLI / other agents

Copy `skills/flow-builder/` into the runtime's skills directory, or add its `SKILL.md` to the agent's skill search path:

```bash
git clone https://github.com/tnt-likely/skills-lab.git
cp -R skills-lab/skills/flow-builder ~/.agents/skills/flow-builder
```

Skill directories differ between runtimes. Keep the directory name `flow-builder` and the `SKILL.md` file. The root `SKILL.md` can also be loaded as a single-file skill.

## Repository layout

```text
skills-lab/
├── README.md
├── README.en.md
├── SKILL.md
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
```

## Publishing rules

Examples must use synthetic data. Before publishing, scan HTML, docs, images, and scripts for private URLs, tokens, personal paths, and unauthorized business material.

## License

MIT

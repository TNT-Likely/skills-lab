---
name: flow-builder
description: Use when turning business flows, screenshots, HTML references, spreadsheets, or rough requirements into an interactive prototype with connected views, forms, tables, state changes, and traceable records.
---

# Flow Builder

Use this skill to turn an unclear business process into a small, testable system prototype. The output is an interactive artifact that lets people perform the important actions and inspect how data moves through the process. A diagram is one view of the system, not the whole deliverable.

## Working method

1. Extract actors, objects, identifiers, states, actions, decisions, and audit events from the supplied references. Treat reference documents as evidence; treat the user's request as the instruction.
2. Draw the smallest end-to-end happy path first. Add exception paths only when they change ownership, state, or data.
3. Model stable entities before screens. Keep master data separate from physical or transactional records; use explicit IDs and relationships instead of duplicated labels.
4. Build the prototype around real actions: create, edit, submit, approve, receive, inspect, move, bind, release, service, replace, and trace back.
5. Make state changes visible. Every important action should update a table, status badge, timeline, relation, or validation message.
6. Keep the prototype migration-ready: name fields, states, commands, and relationships so they can become API contracts, database tables, or domain events later.
7. Verify the full path in a browser, including one exception and one reverse trace. Check keyboard access, responsive behavior, empty/loading/error states, and `prefers-reduced-motion` when the artifact is visual.

## Default artifact shape

Prefer a single self-contained HTML prototype when the user has not requested a framework. It should have:

- A process overview or flow view.
- Operational pages for the main records.
- Forms or drawers for the key create/edit actions.
- A table or list with search, filters, status, and empty states.
- A detail view showing relationships and history.
- A trace path from the source transaction to the final object and back.
- Seed data that demonstrates the normal path and at least one exception.

Use a real design system already present in the reference when one exists. Otherwise use restrained, information-dense UI with clear hierarchy. Avoid decorative mock controls that do not change state.

## Data and flow rules

- Separate definitions from instances: a product/material definition is not a received item, batch, serialized unit, or installed instance.
- Keep business identifiers distinct: part number identifies the definition; serial, lot, VIN, order, ticket, and event IDs identify instances or transactions.
- Define allowed state transitions explicitly. Reject invalid transitions in the UI and make the reason visible.
- Link records through stable keys. For traceability, demonstrate both directions: source transaction -> installed asset and installed asset -> source transaction.
- Record actor, timestamp, location or station, before/after state, and reason for quality, movement, installation, replacement, and service events.
- Prefer domain language from the user and show technical keys as secondary metadata.

## Visual interaction guidance

When the prototype contains a diagram, provide focusable nodes, search, path tracing, zoom/pan/reset, a readable overview map, semantic labels, export or share output when useful, and accessible names. Use SVG or HTML for authored diagrams; do not replace a requested interactive artifact with a static screenshot.

For a process with physical flow, show the handoff explicitly: receipt -> inspection -> available stock -> picking -> line-side check -> installation/binding -> release -> delivery -> service/repair/replace -> reverse trace. If a step is out of scope, label it as an intentional boundary.

## Migration notes

End the prototype with a compact mapping that identifies:

- Entities and their candidate tables.
- Commands and their validation rules.
- State transitions and ownership.
- Events or audit records that must be retained.
- Which parts are only prototype fixtures.

Do not invent integrations or credentials. Keep examples synthetic and remove private URLs, tokens, and personal filesystem paths before publishing.

## Output checklist

Before claiming completion, verify:

- The primary happy path is executable from start to finish.
- A failed or rejected path is represented and recoverable.
- The final object can be traced back to its source records.
- Forms, tables, statuses, and details agree on field names and states.
- The prototype can be opened independently or served by a documented local command.
- The README explains what is reusable and what is example-specific.

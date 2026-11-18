# VCU After-sales Replacement Vertical Slice

This plan covers one testable slice: `service ticket -> VIN lookup -> new VCU validation -> UDS/BLE write -> readback -> Melon replacement transaction -> Feishu task close -> reverse trace`. Once this works, the same boundary can be reused for T-Box and other serialized parts.

## Scope

The service agent starts a replacement task in Feishu. The app asks Melon for the vehicle's current VCU, scans a candidate PN/SN, and receives explicit validation results. Only after device write and readback succeed does Melon atomically detach the old part, bind the new part, and append the replacement history. Feishu receives progress, a result summary, and a Melon reference.

Feishu and Melon must not both write the current VCU relationship. The real UDS/BLE driver may begin as a simulator, but the adapter must model success, failure, timeout, and readback mismatch.

## End-to-end flow

```text
Feishu creates service task
  -> app scans VIN
  -> Melon returns vehicle and current VCU
  -> app scans new PN/SN
  -> Melon validates fit, uniqueness, acceptance, stock, and conflicts
  -> Melon creates replacement session and old-part snapshot
  -> UDS/BLE writes vehicle configuration
  -> readback verifies SN/configuration
  -> Melon commits replacement transaction
  -> old relationship is detached and new VCU is bound
  -> PART_REPLACED trace event is appended
  -> Feishu task is updated and closed
```

Recoverable paths are required: validation rejection, device failure or timeout, readback mismatch, and idempotent duplicate submission.

## Ownership and system boundary

| Concern | Feishu | Melon | Source of truth |
| --- | --- | --- | --- |
| Service task | Task, assignee, site, symptom, priority | Accepts external task reference | Feishu |
| Vehicle relationship | Read-only display | VIN, vehicle state, current VCU lookup | Melon |
| New part scan | Task/app entry point | Candidate PN/SN validation | Melon |
| Device write | Progress display | Command result, timeout, retry evidence | Melon |
| Replacement commit | Result summary and link | Atomic relationship, part state, trace event update | Melon |
| Task close | Status, notes, notification | Completion result and `replacement_id` | Feishu display; Melon fact |
| Reverse trace | Opens linked result | Queries VIN, old SN, new SN, and ticket history | Melon |

Every business fact has one writer. Feishu may retain `source_system` and `source_record_id`; its record ID is an external reference, never a Melon domain key.

## Candidate domain model and API

Entities: service ticket reference, vehicle, serialized part, replacement session, and trace event. Suggested endpoints:

```text
GET  /mfg/vehicles/{vin}/current-parts?partType=VCU
POST /mfg/replacements/validate
POST /mfg/replacements/sessions
POST /mfg/replacements/{id}/device-write
POST /mfg/replacements/{id}/readback
POST /mfg/replacements/{id}/commit
GET  /mfg/replacements/{id}
GET  /mfg/vehicles/{vin}/trace?partType=VCU
```

Validation must cover VIN scope, model compatibility, accepted and available new SN, cross-vehicle uniqueness, conflicting in-progress sessions, readback equality, and idempotency.

## Delivery phases

1. **Feishu workflow validation.** Keep only ticket number, VIN, model, old SN, new PN/SN, reason, service site, technician, status, Melon session, and result link. Verify success, validation failure, device failure, and duplicate submission with synthetic records.
2. **Melon shadow API.** Reuse existing part registration, installation, and assembly queries. Add lookup, validation, session, and simulated device results without changing the production relationship.
3. **One real service bay.** Pick one model, site, and VCU type. Connect the real UDS/BLE adapter. Allow commit only after readback succeeds.
4. **Feishu callback and reverse lookup.** A controlled adapter writes status, completion time, summary, `replacement_id`, and a result link. Repeated callbacks must be harmless.
5. **T-Box reuse.** Reuse the session, idempotency, trace, and synchronization boundaries after VCU acceptance.

## Acceptance matrix

Normal replacement switches the current relationship and closes the task. Bad PN, an occupied SN, device failure, readback mismatch, duplicate commit, Feishu callback failure, and reverse trace each have the behavior described in the Chinese plan. A successful result must expose VIN, old SN, new SN, operator, time, device evidence, and source task.

## Migration notes

The browser prototype simulates API responses and uses synthetic IDs. Preserve the node names, states, commands, and event types when moving to Melon. The first production command should be `CommitReplacement`, receiving the replacement ID, old/new part IDs, VIN, operator, idempotency key, and readback evidence, then updating the current relationship and appending the trace event in one transaction.

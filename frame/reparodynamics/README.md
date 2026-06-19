# pallet-reparodynamics

FRAME pallet scaffold for SubReparo repair-ledger records.

## Purpose

The pallet records safe repair summaries from the local-first SubReparo Immune engine.

It should store small bounded fields:

- reporter account;
- category label;
- severity label;
- summary digest or short label;
- status;
- block number.

## First extrinsics

Target calls:

```text
submit_repair_event(category, severity, digest)
update_repair_status(event_id, status)
```

## First events

```text
RepairEventSubmitted
RepairStatusUpdated
```

## Storage

```text
NextEventId
RepairEvents<EventId, RepairEvent>
```

## Security notes

- Do not store raw private files, logs, or user data.
- Bound all vectors.
- Define origin checks before public use.
- Add benchmarks before production use.
- Add tests for event creation, status update, invalid event id, and bounds.

## Integration path

1. Add this pallet to the SDK workspace.
2. Add the pallet to the selected runtime dependencies.
3. Configure max label and digest lengths.
4. Add it to runtime construction.
5. Build and run local node.
6. Submit first repair event from a dev account.

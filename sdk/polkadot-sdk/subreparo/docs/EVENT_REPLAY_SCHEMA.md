# SubReparo Event Replay Schema

Use this schema to reconstruct repair behavior from runtime events.

## Repair replay record

```json
{
  "schema": "subreparo.repair_replay.v1",
  "block_number": 0,
  "event_index": 0,
  "epoch": 0,
  "nonce": 1,
  "pre_repair_drift": 120,
  "gradient": 25,
  "correction": 25,
  "remaining_drift": 95,
  "max_repair_step": 100,
  "cooldown_after": 3,
  "repairs_this_block": 1,
  "valid_bounds": true,
  "valid_nonce": true,
  "valid_epoch": true
}
```

## Required replay checks

```text
abs(correction) <= MaxRepairStep
nonce not previously seen for epoch
epoch equals runtime EpochIndex
remaining_drift equals pre_repair_drift - correction
cooldown was inactive before repair
repair count did not exceed MaxRepairsPerBlock
repairs were not paused
```

## Audit output

A devnet reviewer should be able to replay all `RepairApplied` events and independently verify the checks above.

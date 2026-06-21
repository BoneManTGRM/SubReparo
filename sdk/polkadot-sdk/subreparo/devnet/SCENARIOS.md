# SubReparo Devnet Scenarios

These are manual devnet scenarios for the SDK/TGRM runtime package after runtime wiring.

## Scenario 1: Manual bounded repair

```text
1. Start devnet.
2. Submit SubReparo.sample_drift(120).
3. Submit SubReparo.repair(epoch=0, nonce=1, gradient=25).
4. Confirm RepairApplied(25, 95).
5. Confirm cooldown is set.
```

## Scenario 2: Replay rejection

```text
1. Submit SubReparo.sample_drift(120).
2. Submit SubReparo.repair(epoch=0, nonce=100, gradient=25).
3. Submit the same repair again.
4. Confirm DuplicateNonce error.
```

## Scenario 3: Pause switch

```text
1. Submit SubReparo.set_paused(true).
2. Attempt SubReparo.repair(...).
3. Confirm RepairsArePaused error.
4. Submit SubReparo.set_paused(false).
```

## Scenario 4: Controller persistence

```text
1. Configure Tau=25 and Persistence=3.
2. Submit drift above Tau.
3. Advance blocks.
4. Confirm controller waits for consecutive breaches before suggesting repair.
```

## Scenario 5: Finality backoff

```text
1. Submit SubReparoFinalityBackoff.set_finality_lag(13).
2. Confirm repairs are paused.
3. Submit SubReparoFinalityBackoff.set_finality_lag(4).
4. Confirm repairs resume.
```

## Scenario 6: Metrics/replay

```text
1. Export event timeline.
2. Reconstruct each repair from epoch, nonce, drift, gradient, correction, and remaining drift.
3. Confirm all corrections obey configured bounds.
```

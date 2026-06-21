# SubReparo Runtime Observability

SubReparo should be observable before any runtime repair is enabled beyond a local devnet.

## Runtime events

```text
SubReparo.DriftSampled(drift)
SubReparo.RepairApplied(correction, remaining_drift)
SubReparo.RepairsPaused(paused)
SubReparo.EpochAdvanced(epoch)
SubReparoController.ControllerObserved(drift, consecutive_breaches)
SubReparoController.ControllerSuggested(gradient)
SubReparoFinalityBackoff.FinalityLagUpdated(lag)
SubReparoFinalityBackoff.BackoffPauseChanged(paused)
```

## Suggested metrics

```text
subreparo_drift_level
subreparo_repairs_applied_total
subreparo_repair_correction_abs_total
subreparo_repairs_paused
subreparo_epoch_index
subreparo_cooldown_remaining
subreparo_repairs_this_block
subreparo_controller_breaches
subreparo_controller_suggestions_total
subreparo_finality_lag
subreparo_backoff_pause_total
```

## Devnet dashboard panels

```text
current drift
repair corrections over time
pause state
cooldown remaining
repairs per block
controller breach count
finality lag
repair event timeline
```

## Alert candidates

```text
RepairsPaused remains true for long window
FinalityLag above PauseThreshold
RepairsThisBlock frequently reaches MaxRepairsPerBlock
DriftLevel does not converge after repeated repairs
DuplicateNonce errors appear
CooldownActive errors spike unexpectedly
```

## Replay audit

Every repair should be reproducible from:

```text
epoch
nonce
pre-repair drift
gradient
bounded correction
post-repair drift
event index
block number
```

Do not claim production readiness until event replay and metric extraction are tested on a devnet.

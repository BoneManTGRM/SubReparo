# pallet-subreparo-finality-backoff

Finality-health guard for SubReparo runtime repair.

## Purpose

SubReparo should slow or pause repairs when finality health is degraded. This keeps runtime repair coherent during reorg or lag risk.

## Policy

```text
if FinalityLag > PauseThreshold:
    RepairsPaused = true

if FinalityLag <= ResumeThreshold:
    RepairsPaused = false
```

## Events

```text
FinalityLagUpdated(lag)
BackoffPauseChanged(paused)
```

## Integration note

This scaffold uses a simple lag value. A production runtime should wire this to a real finality health signal or governance/oracle-approved source.

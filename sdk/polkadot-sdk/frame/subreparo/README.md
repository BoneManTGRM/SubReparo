# pallet-subreparo

Core SubReparo runtime pallet for bounded TGRM repair.

## Purpose

`pallet-subreparo` stores runtime drift state and applies bounded repairs only when all safety gates pass.

## Safety gates

```text
privileged origin
not paused
correct epoch
unique nonce
per-block repair budget
cooldown inactive
drift present
bounded correction
```

## Core storage

```text
DriftLevel
EpochIndex
SeenNonces
RepairsPaused
RepairsThisBlock
EpochCooldownRemaining
```

## Core calls

```text
repair(origin, epoch, nonce, gradient)
set_paused(origin, paused)
sample_drift(origin, drift)
advance_epoch(origin)
```

## Core events

```text
DriftSampled(drift)
RepairApplied(correction, remaining_drift)
RepairsPaused(paused)
EpochAdvanced(epoch)
```

## Integration status

This directory is a compile-oriented scaffold target for Polkadot SDK integration. It is intentionally conservative and should be wired into a mock runtime, benchmarked, and reviewed before runtime deployment.

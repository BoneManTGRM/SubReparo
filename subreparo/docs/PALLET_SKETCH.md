# SubReparo Pallet Sketch

This is the target pallet structure for the SDK/TGRM refocus.

## pallet-subreparo

Core storage:

```rust
DriftLevel: i64
EpochIndex: u32
SeenNonces: map (epoch, nonce) -> ()
RepairsPaused: bool
RepairsThisBlock: u32
EpochCooldownRemaining: u32
```

Core calls:

```rust
repair(origin, epoch, nonce, gradient)
set_paused(origin, paused)
```

Core events:

```rust
RepairApplied(correction)
RepairsPaused(paused)
```

Core errors:

```rust
NoDriftDetected
RepairBudgetExceeded
CooldownActive
RepairsArePaused
DuplicateNonce
BadEpoch
```

## controller pallet

Reads drift, computes bounded gradient, and submits repair through the configured authorized origin.

Target controls:

```rust
MaxStep
Gain
Tau
Persistence
```

## finality backoff pallet

Reads or receives finality lag health and toggles pause/slow mode.

Policy:

```text
if finality_lag > high_threshold: pause repairs
if finality_lag <= recovery_threshold: resume repairs
```

## Integration notes

The first production-quality version must fix these before claiming runtime readiness:

```text
compile against selected Polkadot SDK version
origin wiring
benchmark-generated weights
unit tests/mock runtime
property tests for repair bounds
runtime integration example
Prometheus/Grafana metrics guide
```
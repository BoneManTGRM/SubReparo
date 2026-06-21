# SubReparo Runtime Example Wiring

This is an illustrative runtime wiring example. Adjust paths, constants, origins, and runtime type names for the selected SDK template.

## Runtime config imports

```rust
use frame_support::parameter_types;
```

## Conservative constants

```rust
parameter_types! {
    pub const MaxRepairsPerBlock: u32 = 1;
    pub const EpochCooldown: u32 = 3;
    pub const MaxRepairStep: i64 = 100;
    pub const Tau: i64 = 25;
    pub const Gain: i64 = 4;
    pub const MaxStep: i64 = 50;
    pub const Persistence: u32 = 3;
    pub const PauseThreshold: u32 = 12;
    pub const ResumeThreshold: u32 = 4;
}
```

## pallet-subreparo config

```rust
impl pallet_subreparo::Config for Runtime {
    type RuntimeEvent = RuntimeEvent;
    type ControllerOrigin = frame_system::EnsureRoot<AccountId>;
    type MaxRepairsPerBlock = MaxRepairsPerBlock;
    type EpochCooldown = EpochCooldown;
    type MaxRepairStep = MaxRepairStep;
}
```

## pallet-subreparo-controller config

```rust
impl pallet_subreparo_controller::Config for Runtime {
    type RuntimeEvent = RuntimeEvent;
    type Tau = Tau;
    type Gain = Gain;
    type MaxStep = MaxStep;
    type Persistence = Persistence;
}
```

## pallet-subreparo-finality-backoff config

```rust
impl pallet_subreparo_finality_backoff::Config for Runtime {
    type RuntimeEvent = RuntimeEvent;
    type PauseThreshold = PauseThreshold;
    type ResumeThreshold = ResumeThreshold;
}
```

## construct_runtime example

```rust
construct_runtime!(
    pub enum Runtime
    {
        System: frame_system,
        SubReparo: pallet_subreparo,
        SubReparoController: pallet_subreparo_controller,
        SubReparoFinalityBackoff: pallet_subreparo_finality_backoff,
    }
);
```

## Devnet interaction sketch

```text
SubReparo.sample_drift(120)
SubReparo.repair(epoch=0, nonce=1, gradient=25)
SubReparoFinalityBackoff.set_finality_lag(13)
SubReparo.repair(...) -> should fail while paused
SubReparoFinalityBackoff.set_finality_lag(4)
SubReparo.repair(...) -> can proceed if cooldown and nonce gates pass
```

## Production warning

Do not enable automatic controller repair in a production runtime until benchmark weights, origin policy, finality health source, replay tests, and property tests are complete.

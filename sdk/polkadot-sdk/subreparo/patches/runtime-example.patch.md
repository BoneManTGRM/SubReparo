# Runtime Patch Example

This is a human-readable patch guide, not an auto-applied patch.

## Add runtime dependencies

Add the pallet dependencies to the selected runtime crate.

## Add constants

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

## Add runtime config impls

See:

```text
sdk/polkadot-sdk/subreparo/docs/RUNTIME_EXAMPLE_WIRING.md
```

## Add construct_runtime entries

```rust
SubReparo: pallet_subreparo,
SubReparoController: pallet_subreparo_controller,
SubReparoFinalityBackoff: pallet_subreparo_finality_backoff,
```

## Verify

Run:

```bash
cargo check -p <runtime-crate>
cargo test -p pallet-subreparo
cargo test -p pallet-subreparo-controller
cargo test -p pallet-subreparo-finality-backoff
```

# Next 10 SDK/TGRM Updates

This pass added or improved the next ten SDK-focused items.

## Completed

1. Wired `pallet-subreparo` to its `weights`, `mock`, `tests`, and `benchmarking` modules.
2. Added `WeightInfo` associated type to `pallet-subreparo`.
3. Wired `pallet-subreparo` mock runtime to stub weights.
4. Wired `pallet-subreparo-controller` to its `weights`, `mock`, `tests`, and `benchmarking` modules.
5. Added `WeightInfo` associated type to `pallet-subreparo-controller`.
6. Wired `pallet-subreparo-controller` mock runtime to stub weights.
7. Wired `pallet-subreparo-finality-backoff` to its `weights`, `mock`, `tests`, and `benchmarking` modules.
8. Added `WeightInfo` associated type to `pallet-subreparo-finality-backoff` and wired mock weights.
9. Added Python TGRM harness invariant tests and GitHub Actions harness workflow.
10. Added runtime observability guide, verification checklist, and Prometheus metric examples.

## Remaining caveat

The repository has been improved as a scaffold, but the pallets still need a real `cargo check` inside a fully initialized Polkadot SDK checkout. API mismatches may remain depending on the selected SDK revision.

## Next pass

```text
1. Add Rust correction-bound tests.
2. Add bad epoch and max repairs per block tests.
3. Add benchmarking command examples per pallet.
4. Add storage migration/version placeholder.
5. Add events replay schema.
6. Add devnet scenario script.
7. Add final reviewer README.
8. Add workspace patch file for SDK Cargo.toml.
9. Add runtime patch file example.
10. Run/check CI harness workflow.
```

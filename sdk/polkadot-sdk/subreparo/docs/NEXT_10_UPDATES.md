# Next 10 SDK/TGRM Updates

This pass added or improved the next ten SDK-focused items.

## Completed

1. Wired `pallet-subreparo` to its `weights`, `mock`, `tests`, and `benchmarking` modules.
2. Added `WeightInfo` associated type to `pallet-subreparo`.
3. Wired `pallet-subreparo` mock runtime to stub weights.
4. Wired `pallet-subreparo-controller` to its `weights`, `mock`, `tests`, and `benchmarking` modules.
5. Added `WeightInfo` associated type to `pallet-subreparo-controller`.
6. Wired `pallet-subreparo-finality-backoff` to its `weights`, `mock`, `tests`, and `benchmarking` modules.
7. Added `WeightInfo` associated type to `pallet-subreparo-finality-backoff` and wired mock weights.
8. Added Python TGRM harness invariant tests.
9. Added runtime observability guide.
10. Added runtime verification checklist and GitHub Actions harness workflow.

## Remaining caveat

The connector blocked one controller mock-runtime patch. The controller pallet itself is wired for `WeightInfo`; the mock runtime still needs the same `type WeightInfo = ();` pattern added before `cargo test -p pallet-subreparo-controller` can be trusted.

## Next pass

```text
1. Retry controller mock WeightInfo patch.
2. Run/check CI harness workflow.
3. Add property-test style Rust cases for correction bounds.
4. Add mock tests for bad epoch and max repairs per block.
5. Add benchmarking command examples per pallet.
6. Add storage migration/version placeholder.
7. Add events replay schema.
8. Add Prometheus mapping example.
9. Add devnet scenario script.
10. Add final reviewer README.
```

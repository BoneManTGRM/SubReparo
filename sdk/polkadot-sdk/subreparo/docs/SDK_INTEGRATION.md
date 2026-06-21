# SubReparo SDK Integration Guide

This guide describes the target integration path for SubReparo as a Polkadot SDK/Substrate runtime modification.

## Runtime pallets

```text
frame/subreparo
frame/subreparo-controller
frame/subreparo-finality-backoff
```

## Runtime wiring checklist

1. Add pallet crates to the SDK workspace.
2. Add pallets to the runtime `construct_runtime!` macro.
3. Configure `ControllerOrigin` conservatively.
4. Set conservative constants for `MaxRepairsPerBlock`, `EpochCooldown`, `MaxRepairStep`, `Tau`, `Gain`, and `Persistence`.
5. Wire finality health input to `pallet-subreparo-finality-backoff`.
6. Run unit tests and mock runtime tests.
7. Run FRAME benchmarks and generate weights.
8. Run a devnet with Prometheus/Grafana metrics.
9. Inject drift and verify bounded correction.
10. Simulate finality lag and verify backoff behavior.

## Conservative default constants

```text
MaxRepairsPerBlock = 1
EpochCooldown = 3
MaxRepairStep = 100
Tau = 25
Gain = 4
Persistence = 3
PauseThreshold = 12
ResumeThreshold = 4
```

## Added scaffold support

The repo now includes:

```text
Cargo.toml files
mock runtimes
unit-test scaffolds
benchmarking stubs
weights stubs
workspace integration notes
runtime example wiring
observability guide
verification checklist
Python TGRM harness invariant tests
GitHub Actions harness workflow
```

## Review policy

No production runtime should enable automatic repair until the following are demonstrated:

```text
repair bounds hold under property tests
nonce replay guard rejects duplicates
cooldown prevents oscillation
pause switch stops all repairs
backoff pauses repairs under finality lag
weights are benchmark-generated
repair events are observable and replayable
```

## Demo command

Use the Python harness to demonstrate the core idea before runtime integration:

```bash
python subreparo/harness/tgrm_vs_baseline.py --csv subreparo/harness/tgrm_vs_baseline.csv
python -m pytest subreparo/harness
```

The harness is not the runtime. It is only a reproducible comparison demo for drift correction behavior.

## Deeper docs

```text
sdk/polkadot-sdk/subreparo/docs/WORKSPACE_INTEGRATION.md
sdk/polkadot-sdk/subreparo/docs/RUNTIME_EXAMPLE_WIRING.md
sdk/polkadot-sdk/subreparo/docs/OBSERVABILITY.md
sdk/polkadot-sdk/subreparo/docs/VERIFICATION_CHECKLIST.md
```

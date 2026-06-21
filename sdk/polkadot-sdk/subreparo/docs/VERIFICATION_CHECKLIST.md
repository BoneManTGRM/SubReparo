# SubReparo Runtime Verification Checklist

Use this checklist before claiming SDK/runtime readiness.

## Compile checks

```bash
cargo check -p pallet-subreparo
cargo check -p pallet-subreparo-controller
cargo check -p pallet-subreparo-finality-backoff
```

## Unit tests

```bash
cargo test -p pallet-subreparo
cargo test -p pallet-subreparo-controller
cargo test -p pallet-subreparo-finality-backoff
```

## Harness checks

```bash
python subreparo/harness/tgrm_vs_baseline.py --csv subreparo/harness/tgrm_vs_baseline.csv
python -m pytest subreparo/harness
```

## Required invariants

```text
repair correction never exceeds MaxRepairStep
repair is rejected when paused
repair is rejected during cooldown
repair is rejected for duplicate epoch/nonce
repair is rejected for bad epoch
repairs per block never exceeds MaxRepairsPerBlock
controller does not apply before Persistence breaches
controller respects Tau threshold
finality lag above PauseThreshold pauses repair
finality lag at or below ResumeThreshold resumes repair
```

## Benchmarking

```text
run FRAME benchmarks
generate real weights
replace stub weights
confirm weights are included in runtime
```

## Devnet validation

```text
sample drift
apply manual repair
trigger controller repair
advance epoch
simulate duplicate nonce
pause repairs
simulate finality lag
confirm emitted events
extract metrics
replay repair history
```

## Claim boundary

Until all items above pass, SubReparo should be described as:

```text
research/prototype SDK runtime modification scaffold
```

Not:

```text
production-ready runtime
autonomous security system
Polkadot replacement
```
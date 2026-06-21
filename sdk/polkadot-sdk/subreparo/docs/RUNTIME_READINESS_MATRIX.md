# SubReparo Runtime Readiness Matrix

| Area | Status | Evidence path | Required before production |
|---|---:|---|---|
| Core pallet scaffold | Drafted | `frame/subreparo` | `cargo check`, unit tests, review |
| Controller scaffold | Drafted | `frame/subreparo-controller` | `cargo check`, controller policy review |
| Finality backoff scaffold | Drafted | `frame/subreparo-finality-backoff` | real finality signal source |
| Mock tests | Drafted | `src/tests.rs` per pallet | run against SDK checkout |
| Weights | Stub only | `src/weights.rs` per pallet | FRAME benchmarks |
| Benchmarks | Stub only | `src/benchmarking.rs` per pallet | generated production weights |
| Harness | Added | `subreparo/harness` | CI pass and report artifacts |
| Observability | Documented | `docs/OBSERVABILITY.md` | node/runtime metric extraction |
| Replay audit | Documented | `docs/EVENT_REPLAY_SCHEMA.md` | event replay script |
| Runtime wiring | Example only | `docs/RUNTIME_EXAMPLE_WIRING.md` | real runtime integration |
| Devnet scenarios | Documented | `devnet/SCENARIOS.md` | executed devnet transcript |

## Current readiness label

```text
research/prototype SDK runtime modification scaffold
```

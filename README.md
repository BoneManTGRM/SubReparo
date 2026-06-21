# SubReparo

SubReparo is a modified Polkadot SDK/Substrate runtime package that applies **Reparodynamics** and the **Targeted Gradient Repair Mechanism (TGRM)** to bounded runtime self-repair.

It is not an AI-agent platform, antivirus, or endpoint security product. The core project is a runtime/control-layer modification focused on:

```text
measure drift -> trigger threshold -> apply bounded repair -> enforce cooldown -> log proof -> verify stability
```

## Product position

SubReparo is a **TGRM repair layer for Polkadot SDK/Substrate runtimes**.

The project goal is to make runtime repair:

```text
bounded
authorized
replay-safe
cooldown-limited
observable
benchmarkable
reversible where possible
compatible with Polkadot SDK integration
```

## Architecture

```text
SubReparo SDK Runtime
├─ pallet-subreparo              -> bounded drift repair, pause switch, nonce/replay guard
├─ pallet-subreparo-controller   -> automated bounded gradient suggestion/application
├─ pallet-finality-backoff       -> slows or pauses repair during finality lag risk
├─ benchmarking + weights        -> FRAME benchmarking stubs and generated weights path
├─ observability                 -> events, metrics names, audit/replay guidance
├─ comparison harness            -> TGRM vs baseline simulation/demo
└─ docs                          -> integration, safety policy, reviewer checklist
```

## Core law

SubReparo implements the Reparodynamics/TGRM idea:

```text
error = measured runtime drift
if abs(error) > τ and persistence >= m:
    correction = clamp(gradient(error), -E_max, +E_max)
    apply correction only if authorized, within budget, and outside cooldown
    emit RepairApplied event
    record epoch + nonce to prevent replay
else:
    do nothing
```

## Safety model

SubReparo repairs must be constrained by runtime policy:

```text
privileged origin only
per-block repair cap
epoch cooldown
energy/step cap
emergency pause switch
nonce-based replay protection
finality lag backoff
benchmark-derived weights
observable events and metrics
```

## SDK foundation

SubReparo uses Polkadot SDK as its foundation through:

```text
sdk/polkadot-sdk
```

Install or update the SDK foundation:

```bash
git submodule update --init --recursive
```

or:

```bash
bash scripts/bootstrap-sdk-foundation.sh
```

Windows:

```powershell
./scripts/bootstrap-sdk-foundation.ps1
```

## Intended SDK layout

```text
sdk/polkadot-sdk/frame/subreparo
sdk/polkadot-sdk/frame/subreparo-controller
sdk/polkadot-sdk/frame/subreparo-finality-backoff
sdk/polkadot-sdk/subreparo/docs
sdk/polkadot-sdk/subreparo/harness
```

Current scaffolded path may also include earlier names such as:

```text
sdk/polkadot-sdk/frame/reparodynamics
```

Those should be consolidated toward the SDK layout above.

## Build direction

Target deliverable:

```text
A reviewer-ready Polkadot SDK runtime modification package implementing bounded TGRM repair.
```

Next implementation priorities:

```text
1. pallet-subreparo: compile-ready FRAME pallet
2. pallet-subreparo-controller: bounded gradient controller
3. pallet-finality-backoff: finality lag pause/slowdown policy
4. replay-safe epoch + nonce handling
5. emergency pause and privileged origin wiring
6. frame-benchmarking stubs and weights
7. simulation/comparison harness
8. Prometheus/Grafana metric guide
9. devnet run instructions
10. reviewer checklist
```

## What this is not

```text
not an antivirus
not a phone app
not an AI-agent framework
not a promise of automatic security
not a replacement for Polkadot governance or runtime review
```

## What this is

```text
an experimental SDK/runtime repair mechanism
an applied Reparodynamics/TGRM implementation
a bounded control-loop scaffold
a runtime safety and observability research package
a path toward auditable adaptive runtime behavior
```

## Verification goals

A credible SubReparo demo should prove:

```text
bounded correction never exceeds configured limits
cooldown prevents oscillation
replay guard rejects duplicate repair nonces
pause switch stops repair
finality lag backoff slows or pauses repair
benchmarks produce weights
TGRM harness improves drift/stability under controlled conditions
all repair events are replayable from logs
```

## Development status

Research/prototype. The repo is being refocused into a Polkadot SDK/Substrate runtime modification package. Older agent, desktop, mobile, and antivirus-oriented scaffolds may remain temporarily but are not the core SubReparo direction.

## License

Code: Apache-2.0 target.

Docs/papers: CC BY 4.0 target unless otherwise stated.

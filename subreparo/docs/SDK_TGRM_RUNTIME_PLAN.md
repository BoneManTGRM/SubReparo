# SubReparo SDK/TGRM Runtime Plan

SubReparo is being refocused as a Polkadot SDK/Substrate runtime modification that applies Reparodynamics and TGRM to bounded runtime self-repair.

## Correct scope

```text
SubReparo = modified SDK runtime + bounded TGRM repair pallets
```

SubReparo is not currently positioned as:

```text
AI agent platform
antivirus
endpoint security tool
mobile app
AGI system
```

## Core runtime components

```text
pallet-subreparo
  Stores drift level, epoch, nonce history, pause state, cooldown, and per-block repair count.
  Applies bounded repair only from authorized origins.

pallet-subreparo-controller
  Reads drift and proposes/applies bounded gradient corrections.
  Uses MaxStep/Gain-style parameters to prevent overshoot.

pallet-finality-backoff
  Watches finality lag signal.
  Pauses or slows repairs when lag exceeds threshold.
  Resumes when finality health recovers.

benchmarking/weights
  FRAME benchmarking stubs.
  Generated WeightInfo path.

comparison harness
  TGRM vs baseline drift simulation.
```

## TGRM repair law

```text
error = measured_drift
if abs(error) > tau and persistence >= m:
    gradient = bounded_gradient(error)
    correction = clamp(gradient, -dmax, +dmax)
    correction = clamp(correction, -E_max, +E_max)
    apply only if origin/cooldown/budget/nonce/finality checks pass
    emit event
else:
    no-op
```

## Safety requirements

```text
privileged origin only
nonce replay protection
epoch binding
per-block budget cap
epoch cooldown
emergency pause
bounded gradient
finality lag backoff
benchmark-derived weights
observable events
replayable audit trail
```

## Reviewer checklist

```text
1. Pallets compile under current Polkadot SDK.
2. Runtime origin gating is explicit.
3. Repair extrinsic rejects duplicate epoch/nonce pairs.
4. Cooldown prevents repeated rapid repair.
5. MaxRepairsPerBlock enforces budget.
6. Pause switch stops repairs.
7. Finality backoff toggles repair pause/slow mode.
8. Events are emitted for repair and pause changes.
9. FRAME benchmarks run and weights are generated.
10. Harness demonstrates bounded drift correction.
```

## Repository cleanup direction

Older agent/mobile/antivirus work should be treated as experimental side scaffolding and not the primary product. The main README and roadmap should emphasize SDK runtime repair.

## Next build pass

```text
1. Create compile-oriented pallet-subreparo scaffold.
2. Create compile-oriented controller scaffold.
3. Create finality-backoff scaffold.
4. Add harness code in subreparo/harness.
5. Add SDK integration README.
6. Add benchmarking and weights stubs.
7. Add CI commands for Rust formatting/build when SDK path is present.
```
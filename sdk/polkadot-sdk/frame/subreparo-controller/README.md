# pallet-subreparo-controller

Controller scaffold for bounded TGRM repair suggestions.

## Purpose

The controller reads drift from `pallet-subreparo`, computes a bounded gradient, and applies repair through the configured runtime origin policy.

## Controls

```text
Tau        -> minimum drift threshold
Gain       -> proportional divisor/multiplier control
MaxStep    -> absolute correction cap
Persistence -> number of consecutive breaches required before repair
```

## Safety

The controller must never bypass `pallet-subreparo` safety gates. It should only suggest or call repair through runtime-approved origins and should remain pause-aware.

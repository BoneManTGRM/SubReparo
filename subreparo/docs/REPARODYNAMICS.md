# Reparodynamics, TGRM, and RYE

This document defines the SubReparo-specific theory layer.

## Reparodynamics

Reparodynamics is the study and engineering of adaptive repair loops.

SubReparo applies it to software, AI agents, websites, and future on-chain repair memory.

The core loop is:

```text
stress -> fracture -> repair -> verification -> scar memory -> adaptation
```

## TGRM

TGRM means Targeted Gradient Repair Mechanism.

It gives SubReparo a repair control loop:

```text
TEST -> DETECT -> REPAIR -> VERIFY -> MEMORY
```

### TEST

Establish expected project state.

### DETECT

Find stress signals and classify likely fracture type.

### REPAIR

Prepare or apply an approved repair.

### VERIFY

Re-run the relevant check and confirm measurable improvement.

### MEMORY

Store the lesson as scar memory so future runs improve.

## RYE

RYE means Repair Yield per Energy.

```text
RYE = repair_gain / energy_cost
```

RYE helps SubReparo choose repairs that create the most verified improvement for the least cost.

## Why this is different

Most tools stop at alerts.

SubReparo should move beyond alerts:

```text
alert -> repair plan -> verification -> memory -> better future behavior
```

## Chain relevance

The chain should store safe summaries of verified repair events:

- category;
- severity;
- digest;
- repair phase;
- outcome;
- RYE score;
- block time.

Raw private project data stays local.

## Implementation status

Current implementation:

```text
tools/subreparo-immune/src/subreparo_immune/reparodynamics.py
```

Current chain scaffold:

```text
frame/reparodynamics/
```

Next step:

Add `repair_phase`, `repair_outcome`, and `rye_score` fields to the chain runtime once the SDK runtime is wired.

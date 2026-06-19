# SubReparo

SubReparo is a local-first repair-memory system for AI agents, software projects, websites, and autonomous infrastructure.

This repository is the clean private home for SubReparo. It is not a fork.

## Core idea

```text
observe -> detect -> record -> repair -> verify -> remember -> learn -> improve
```

## Architecture

```text
SubReparo Immune  -> local-first engine, score, reports, ledger, export payload
SubReparo Chain   -> Polkadot SDK / FRAME repair-ledger memory
```

## Full SDK foundation

SubReparo uses Polkadot SDK as its chain foundation through a pinned SDK workspace path:

```text
sdk/polkadot-sdk
```

This keeps the repository clean while still giving SubReparo the full SDK foundation.

To install the SDK foundation locally:

```bash
git submodule update --init --recursive
```

Or run:

```bash
bash scripts/bootstrap-sdk-foundation.sh
```

Windows:

```powershell
./scripts/bootstrap-sdk-foundation.ps1
```

The SDK workspace receives the SubReparo additions:

```text
sdk/polkadot-sdk/frame/reparodynamics
sdk/polkadot-sdk/tools/subreparo-immune
sdk/polkadot-sdk/subreparo/docs
```

## Reparodynamics layer

SubReparo is not only a scanner.

It includes first-class Reparodynamics concepts:

```text
stress -> fracture -> repair -> verification -> scar memory -> adaptation
```

TGRM repair phases:

```text
TEST -> DETECT -> REPAIR -> VERIFY -> MEMORY
```

RYE metric:

```text
RYE = repair_gain / energy_cost
```

These are implemented in:

```text
tools/subreparo-immune/src/subreparo_immune/reparodynamics.py
subreparo/docs/REPARODYNAMICS.md
```

## What works now

- local Python engine under `tools/subreparo-immune`;
- PyPI-ready package metadata;
- project scanning;
- dependency manifest review;
- git working-tree review;
- website response check;
- score and markdown report;
- Reparodynamics, TGRM, and RYE metrics;
- local repair ledger;
- chain export payload;
- CI workflow for the Python tool;
- `frame/reparodynamics` pallet scaffold;
- SDK bootstrap and bridge docs.

## Quick test

```bash
cd tools/subreparo-immune
python -m pip install -e .
subreparo-immune init .
subreparo-immune run .
```

Outputs:

```text
.subreparo/report.md
.subreparo/repair_ledger.jsonl
.subreparo/chain_export.json
```

## Chain target

```text
.subreparo/chain_export.json
        -> submit_repair_event
        -> pallet-reparodynamics
        -> SubReparo repair ledger
```

## Private data rule

Raw project files, local logs, private notes, and customer data should stay local by default.

The chain should store safe summaries, labels, status values, RYE metrics, TGRM phases, and digests only.

## Status

Alpha MVP. Local-first product is usable; SDK foundation is pinned by submodule/bootstrap path; chain pallet is scaffolded and still needs runtime wiring, tests, benchmarks, and review.

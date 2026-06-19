# SubReparo V2

SubReparo is a local-first repair-memory system for AI agents, software projects, websites, and autonomous infrastructure.

This repository is the clean private home for SubReparo V2. It is not a fork.

## Core idea

```text
observe -> detect -> record -> repair -> verify -> remember -> learn -> improve
```

## Architecture

```text
SubReparo Immune  -> local-first engine, score, reports, ledger, export payload
SubReparo Chain   -> Polkadot SDK / FRAME repair-ledger memory
```

## What works now

- local Python engine under `tools/subreparo-immune`;
- PyPI-ready package metadata;
- project scanning;
- dependency manifest review;
- git working-tree review;
- website response check;
- score and markdown report;
- local repair ledger;
- chain export payload;
- CI workflow for the Python tool;
- `frame/reparodynamics` pallet scaffold;
- SDK migration and bridge docs.

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

The chain should store safe summaries, labels, status values, and digests only.

## Status

Alpha MVP. Local-first product is usable; chain pallet is scaffolded and still needs runtime wiring, tests, benchmarks, and review.

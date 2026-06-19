# SubReparo Immune

Local-first repair-memory engine for AI agents, software projects, websites, and autonomous systems.

SubReparo Immune runs locally first. It does not require the chain to provide value.

## Install for development

```bash
cd tools/subreparo-immune
python -m pip install -e .
```

## Run

```bash
subreparo-immune init .
subreparo-immune run .
subreparo-immune run . --json
subreparo-immune run . --website https://example.com
subreparo-immune quality . --json
subreparo-cortex . --status --json
subreparo-immune dashboard
```

## Outputs

```text
.subreparo/report.md
.subreparo/repair_ledger.jsonl
.subreparo/chain_export.json
.subreparo/cortex_memory.jsonl
.subreparo/cortex_tasks.jsonl
.subreparo/approval_queue.jsonl
.subreparo/outcome_records.jsonl
.subreparo/quality_report.json
.subreparo/snapshots/
```

## Current checks

- local-only file review;
- content pattern review;
- dependency manifest review;
- git working-tree review;
- website response check;
- project score and markdown report;
- digest/export payload for future chain bridge.

## Cortex dashboard visibility

The local dashboard now surfaces the Cortex operator layer:

- task count;
- memory count;
- pending approval count;
- outcome count;
- quality gate report;
- latest snapshot manifest;
- pending approval reasons.

This keeps the platform local-first while making the adaptive repair loop visible enough to supervise before repair execution becomes more autonomous.

## PyPI packaging

This package is configured for PyPI publication.

Build locally:

```bash
python -m pip install build twine
python -m build
python -m twine check dist/*
```

Publish later only after tests, docs, and naming are confirmed.

## Local-first principle

SubReparo Immune must remain useful without the chain.

The chain should receive safe summaries and digests only.

Raw project files, private logs, and customer data should stay local by default.

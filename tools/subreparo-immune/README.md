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
subreparo-immune setup . --mode simple
subreparo-immune run .
subreparo-immune run . --json
subreparo-immune run . --website https://example.com
subreparo-immune feedback . --false-positive src/app.py --reason "known safe"
subreparo-immune trust . --json
subreparo-immune watch-plan . --json
subreparo-immune quality . --json
subreparo-immune sign-report . --json
subreparo-cortex . --status --json
subreparo-cortex . --components --json
subreparo-immune dashboard
```

## Outputs

```text
.subreparo/report.md
.subreparo/repair_ledger.jsonl
.subreparo/chain_export.json
.subreparo/feedback.json
.subreparo/trust_report.json
.subreparo/setup_profile.json
.subreparo/report_signature.json
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
- false-positive feedback;
- file, folder, and domain trust scoring;
- first-run setup profile;
- watcher backend planning;
- local report integrity signatures;
- project score and markdown report;
- digest/export payload for future chain bridge.

## Cortex AI-agent components

The Cortex layer now exposes the five AI-agent components:

1. LLM brain
2. Prompting and instructions
3. Memory
4. External knowledge
5. Tools

The local registry also tracks the three minimum ingredients: external knowledge, tools, and prompting.

The LLM brain is registered but not connected by default. A live model connector should require explicit configuration and approval before any private project context leaves the machine.

Command:

```bash
subreparo-cortex . --components --json
```

## Cortex dashboard visibility

The local dashboard now surfaces the Cortex operator layer and protection state:

- task count;
- memory count;
- pending approval count;
- outcome count;
- AI agent component readiness;
- false-positive feedback;
- trust report;
- watch plan;
- report signature;
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

# SubReparo

SubReparo is a local-first adaptive repair platform for AI agents, software projects, endpoints, websites, and autonomous infrastructure.

This repository is the clean private home for SubReparo. It is not a fork.

## Product position

SubReparo is not only an antivirus and not only a scanner.

It is an adaptive repair and resilience layer:

```text
observe -> detect -> explain -> isolate -> repair -> verify -> remember -> improve
```

## Best direction

The strongest path is broader than cybersecurity:

```text
SubReparo Adaptive Repair Platform
```

Cybersecurity is one protection module. The larger product is self-healing infrastructure for software, AI systems, developer machines, client environments, and future chain-backed repair memory.

## Architecture

```text
SubReparo Immune     -> local defensive sensors, patrol, baseline, quarantine, reports
SubReparo Cortex     -> planning, approval queue, status report, memory, safe work loop
SubReparo Repair     -> repair planning, verification, timeline, audit, learning memory
SubReparo Platform   -> policy, dashboard, modes, inventory, incident bundles, quality gates
SubReparo Chain      -> Polkadot SDK / FRAME repair-ledger memory
```

## AI agent ingredients

SubReparo Cortex now exposes the standard AI-agent component stack:

```text
1. LLM brain
2. Prompting and instructions
3. Memory
4. External knowledge
5. Tools
```

The three minimum ingredients are also tracked explicitly:

```text
external knowledge + tools + prompting
```

The LLM brain is registered as a component, but no external model is connected by default. Any live model connector must be defensive, local-first where possible, and approval-gated before private project context is shared outside the machine.

Run:

```bash
subreparo-cortex . --components --json
```

Details: `subreparo/docs/AGENT_COMPONENTS.md`.

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

SubReparo includes first-class Reparodynamics concepts:

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
- defensive immune patrol for scripts, binaries, launchers, startup entries, browser extensions, runtime processes, and network signals;
- baseline integrity memory and diffing;
- dependency manifest review, dependency inventory, and firewall suggestions;
- quarantine staging and restore controls;
- policy allowlist/blocklist/ignore-target management;
- false-positive feedback records;
- file, folder, and domain trust scoring;
- trust scores in markdown reports, append-only ledger records, and chain export payloads;
- first-run setup profile;
- watcher backend and target planning with native-watchdog detection and polling fallback;
- local report integrity signatures with optional HMAC key support;
- Cortex planning, memory, approval queue, status report, swarm routing, swarm plans, and outcome records;
- Cortex AI-agent component registry for LLM brain, prompting, memory, external knowledge, and tools;
- safe project snapshots before high-risk work;
- quality gate command and CI smoke tests;
- git working-tree review;
- website response check;
- score and markdown report;
- timeline and risk trend summaries;
- incident bundle export with privacy redaction;
- hash-chained audit log;
- local tabbed dashboard;
- rule catalog and rule changelog;
- Reparodynamics, TGRM, and RYE metrics;
- local repair ledger;
- chain export payload;
- CI workflow for the Python tool;
- `frame/reparodynamics` pallet scaffold;
- SDK bootstrap and bridge docs.

## Quick install

Unix/macOS:

```bash
bash scripts/install-subreparo-immune.sh
```

Windows PowerShell:

```powershell
./scripts/install-subreparo-immune.ps1
```

Manual:

```bash
cd tools/subreparo-immune
python -m pip install -e .
```

## Quick test

```bash
subreparo-immune init .
subreparo-immune setup . --mode simple
subreparo-immune doctor .
subreparo-immune patrol .
subreparo-immune baseline .
subreparo-immune diff .
subreparo-immune trust .
subreparo-immune quality .
subreparo-immune sign-report .
subreparo-monitor . --once
```

## Useful commands

```bash
subreparo-immune run . --json
subreparo-immune isolate .
subreparo-immune isolate . --apply
subreparo-immune quarantine .
subreparo-immune quarantine . --restore-index 0
subreparo-immune policy . --allow-hash <sha256>
subreparo-immune policy . --block-hash <sha256>
subreparo-immune policy . --ignore-target <target>
subreparo-immune feedback . --false-positive <target> --reason "known safe"
subreparo-immune trust . --json
subreparo-immune setup . --mode developer --watch src
subreparo-immune watch-plan . --json
subreparo-immune sign-report . --json
subreparo-immune sign-report . --verify --json
subreparo-immune timeline .
subreparo-immune trends .
subreparo-immune inventory .
subreparo-immune firewall .
subreparo-immune bundle .
subreparo-immune audit .
subreparo-immune rules
subreparo-immune quality . --json
subreparo-immune dashboard
subreparo-cortex . --plan --json
subreparo-cortex . --next --json
subreparo-cortex . --memory --json
subreparo-cortex . --approvals --json
subreparo-cortex . --status --json
subreparo-cortex . --components --json
subreparo-cortex . --swarm --json
subreparo-cortex . --route 'run quality checks' --json
subreparo-cortex . --orchestrate 'run quality checks' --json
subreparo-cortex . --plans --json
```

Outputs:

```text
.subreparo/report.md
.subreparo/repair_ledger.jsonl
.subreparo/chain_export.json
.subreparo/quarantine_manifest.jsonl
.subreparo/audit.jsonl
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

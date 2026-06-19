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
SubReparo Repair     -> repair planning, verification, timeline, audit, learning memory
SubReparo Platform   -> policy, dashboard, modes, inventory, incident bundles
SubReparo Chain      -> Polkadot SDK / FRAME repair-ledger memory
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
- git working-tree review;
- website response check;
- score and markdown report;
- timeline and risk trend summaries;
- incident bundle export with privacy redaction;
- hash-chained audit log;
- local dashboard;
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
subreparo-immune doctor .
subreparo-immune patrol .
subreparo-immune baseline .
subreparo-immune diff .
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
subreparo-immune timeline .
subreparo-immune trends .
subreparo-immune inventory .
subreparo-immune firewall .
subreparo-immune bundle .
subreparo-immune audit .
subreparo-immune rules
subreparo-immune dashboard
```

Outputs:

```text
.subreparo/report.md
.subreparo/repair_ledger.jsonl
.subreparo/chain_export.json
.subreparo/quarantine_manifest.jsonl
.subreparo/audit.jsonl
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

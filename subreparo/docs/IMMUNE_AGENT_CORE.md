# SubReparo Immune Agent Core

## Direction

SubReparo Immune should become the LLM-agent core for SubReparo.

The Python-first prototype is built around this autonomous loop:

```text
observe -> detect -> plan -> repair -> verify
```

The loop uses scars, outcomes, and repair-ledger records as long-term memory.

## Core idea

SubReparo Immune is not only a scanner. It is the local defensive agent brain that coordinates:

```text
observations
findings
swarm plans
repair plans
verification
scar memory
proof export
```

## Long-term memory

The agent records local memory under `.subreparo`:

```text
.subreparo/agent_cycles.jsonl
.subreparo/agent_scars.jsonl
.subreparo/outcome_records.jsonl
.subreparo/repair_ledger.jsonl
```

These records are the practical scar memory layer.

## Tool use

The first tool-use layer is local and bounded:

```text
scan_project
immune_patrol
scan_git
swarm_orchestrator
agent_proof_export
```

High-impact actions remain approval-gated.

## Python-first commands

Run one cycle:

```bash
cd tools/subreparo-immune
python -m subreparo_immune.immune_agent_cli ../../ --cycle "self-heal project" --json
```

Show scar memory:

```bash
python -m subreparo_immune.immune_agent_cli ../../ --scars --json
```

Build latest proof payload:

```bash
python -m subreparo_immune.immune_agent_cli ../../ --proof --json
```

Write latest proof payload:

```bash
python -m subreparo_immune.immune_agent_cli ../../ --write-proof --json
```

Bot/frontend backend payload:

```bash
python -m subreparo_immune.immune_agent_cli ../../ --bot-backend "self-heal project" --json
```

## Chain later

The prototype exports a chain-ready proof payload:

```text
.subreparo/agent_proof_export.json
```

Target later:

```text
pallet-reparodynamics::submit_agent_proof
```

The on-chain pallet should store verifiable shared state/proofs across agents, not raw private project data.

## Clawdbot backend direction

A Clawdbot-style frontend can call the SubReparo backend adapter to display:

```text
current goal
swarm orchestration
agent cycle result
repair plan
proof export
approval requirements
```

The adapter does not execute high-impact actions. It returns safe backend payloads for display and approval.

## Safety boundary

SubReparo Immune agent core must remain:

```text
local-first
approval-gated
proof-recording
non-destructive by default
private-data-preserving
```

# SubReparo AI Agent Components

SubReparo Cortex now tracks the standard AI-agent ingredient stack as explicit local platform state.

## The three minimum ingredients

1. External knowledge
2. Tools
3. Prompting

These are enough to make a basic agent useful when the system can read grounded context, follow clear instructions, and call bounded tools.

## The five platform components

1. **LLM brain** — reasoning layer for interpreting local findings and proposing repair plans.
2. **Prompting and instructions** — defensive scope, policy, approval rules, and role instructions.
3. **Memory** — local task, approval, outcome, quality, snapshot, and scar-memory records.
4. **External knowledge** — local documentation, scan reports, dependency manifests, rule catalogs, website checks, and safe lookups.
5. **Tools** — bounded local commands for scan, patrol, baseline, quarantine, reporting, dashboard, and chain export.

## Current safety boundary

The component registry does not call an external model. The LLM brain is registered as a component, but it is not connected by default.

Any live LLM connector must remain defensive, local-first where possible, and approval-gated before private project context is shared outside the machine.

High-impact tool use remains review-first or explicit-approval only.

## Command

```bash
subreparo-cortex . --components --json
```

The command returns:

- registered component count;
- operational local component count;
- component purposes;
- local artifact readiness;
- safety boundaries;
- actions that require approval.

## Dashboard

The local dashboard includes an **AI agent components** panel so the operator can see whether the agent stack is present before more autonomous repair workflows are added.

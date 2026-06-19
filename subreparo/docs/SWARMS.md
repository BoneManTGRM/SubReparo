# SubReparo Swarms

SubReparo Cortex uses swarms as coordinated specialist roles with bounded tools.

The swarm system is not uncontrolled autonomy. It is a router that maps a task to:

```text
role -> allowed tools -> approval requirement -> reason
```

## Swarm roles

Initial roles:

```text
planner   -> breaks goals into safe tasks
sentinel  -> watches risk and immune signals
builder   -> applies safe docs/tests/local improvements
tester    -> runs quality gates and verification
reviewer  -> reviews high-impact tasks
archivist -> records memory, outcomes, status, and snapshots
```

## Swarm tools

Initial bounded tools:

```text
scan_project      -> project scanner
immune_patrol     -> local immune patrol
baseline_diff     -> integrity diff
quality_gate      -> compile/test verification
skill_review      -> manifest review without execution
snapshot          -> local pre-change archive
quarantine_stage  -> staged isolation, approval required
```

## Routing examples

```bash
subreparo-cortex . --swarm --json
subreparo-cortex . --route "run quality checks" --json
subreparo-cortex . --route "scan risk and patrol baseline" --json
```

## Safety rule

Any task involving deletion, spending, publishing, sending external messages, secrets, or production changes must route to review or block.

## Design target

Swarms should make SubReparo feel like a coordinated team:

```text
Planner decides the next step.
Sentinel checks risk.
Builder makes safe changes.
Tester verifies.
Reviewer handles approval.
Archivist records what happened.
```

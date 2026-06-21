# SubReparo Factory

SubReparo Factory is the ecosystem layer for producing useful, reviewed, reusable agents.

## Goal

SubReparo should not be a single assistant. It should become a platform that can define, review, register, and manage specialized agents.

## Pipeline

```text
idea -> blueprint -> manifest -> permission review -> scaffold -> tests -> registry -> dashboard
```

## Current blueprints

```text
code_review       -> review project changes and produce safe notes
test_builder      -> suggest and stage tests under review
docs_writer       -> draft setup docs, README sections, and operator notes
website_monitor   -> check website health with network-read only
report_generator  -> generate structured local reports from SubReparo state
```

## Commands

List blueprints:

```bash
subreparo-factory . --blueprints --json
```

Preview a manifest and review result:

```bash
subreparo-factory . --manifest code_review --json
```

Create a local scaffold and register it when the review allows it:

```bash
subreparo-factory . --create code_review --register --json
```

List registry records:

```bash
subreparo-factory . --registry --json
```

## Factory records

Factory output is stored locally under:

```text
.subreparo/factory/
.subreparo/factory/agents/
.subreparo/factory/agent_registry.jsonl
```

## Safety model

Every generated agent manifest includes:

```text
purpose
category
tools
permissions
memory policy
approval policy
test plan
review result
```

Low-risk agents can be registered automatically. Agents with write, network, external-message, or publishing permissions require review. Blocked permissions are not allowed.

## Blocked permissions

```text
delete_data
spend_money
read_secrets
shell_write
credential_access
```

## Next product step

Expose Factory in the Control Center dashboard with:

```text
blueprint catalog
local registry
review status
scaffolded agent folders
quality score per generated agent
```

## Long-term ecosystem

The larger SubReparo ecosystem should contain:

```text
agent blueprints
agent registry
skill/plugin registry
repair playbooks
dashboards
proof exports
fleet workspaces
marketplace-ready templates
```

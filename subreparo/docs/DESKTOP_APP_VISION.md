# SubReparo Desktop Application Vision

## Long-term vision

SubReparo should evolve into a desktop application for Windows, macOS, and Linux.

The goal is to make SubReparo feel like an operating system for autonomous repair and protection rather than a collection of scripts.

## Core experience

The desktop app should provide a visual control center for SubReparo Cortex, Immune, Swarms, Repair, Platform, and Chain.

The user should be able to open the program and immediately see:

```text
What is SubReparo doing?
What are the swarms working on?
What needs approval?
What has changed?
What passed verification?
What needs repair?
```

## Required desktop features

### 1. Live swarm visualization

Show active swarm roles, planned steps, and current swarm state.

Initial roles:

```text
Planner
Sentinel
Builder
Tester
Reviewer
Archivist
```

### 2. Interactive graph of agent collaboration

Show how roles, tools, memory, approvals, and outputs connect.

Example:

```text
Goal -> Planner -> Sentinel -> Builder -> Tester -> Reviewer -> Archivist
```

### 3. Memory browser

Let the user inspect local Cortex memory:

```text
.subreparo/cortex_memory.jsonl
.subreparo/cortex_tasks.jsonl
.subreparo/outcome_records.jsonl
.subreparo/swarm_plans.jsonl
```

### 4. Threat and health dashboard

Show project/system health in one place:

```text
risk score
findings by severity
quarantine state
baseline changes
policy status
skill/plugin risk
quality status
```

### 5. Timeline of actions

Show a chronological view of actions, detections, approvals, snapshots, outcomes, audits, and reports.

### 6. One-click scan and repair

The first version should support safe one-click actions:

```text
run scan
run quality gate
create snapshot
review skills
show repair plan
```

High-impact actions must still require explicit approval.

### 7. 24/7 background monitoring

Run SubReparo in the background with safe scheduled loops:

```text
hourly checks
nightly reports
approval-needed alerts
condition-based risk warnings
```

### 8. Approval queue for high-impact actions

Show pending approvals clearly before any sensitive action.

High-impact actions include:

```text
delete data
spend money
send external messages
publish public content
change production infrastructure
share private context
run high-impact security actions
```

### 9. Self-learning metrics and performance trends

Show how SubReparo improves over time:

```text
repair outcomes
quality pass rate
recurring risks
successful patterns
failed strategies
RYE score trends
TGRM phase history
```

## App structure

Recommended UI sections:

```text
Home
Swarms
Tasks
Approvals
Memory
Health
Timeline
Reports
Skills
Settings
```

## First desktop MVP

The first MVP should be a local web dashboard before native packaging.

Phase 1:

```text
local dashboard at 127.0.0.1
Cortex status panel
swarm plan panel
approval queue panel
quality report panel
memory/event panel
```

Phase 2:

```text
package as desktop app
Windows installer
macOS app bundle
Linux AppImage/deb/rpm
background service
tray icon
notifications
```

## Safety boundary

The desktop app must preserve SubReparo's core control rules:

```text
local-first by default
no silent high-impact actions
approval queue for sensitive tasks
clear logs and outcome records
snapshots before larger changes
private data never shared by default
```

## Product meaning

This is the version that turns SubReparo from a command-line tool into a visible autonomous repair platform.

It becomes a control center for:

```text
software repair
AI-agent safety
cyber defense
system health
business automation
proof-of-repair memory
```

# SubReparo Cortex Architecture

## Goal

SubReparo Cortex is the 24/7 operating layer for the SubReparo ecosystem.

It is not true AGI. It is an AGI-like autonomous work system built from specialized agents, tools, memory, verification, schedules, approval gates, and repair loops.

## Core AI-agent ingredients

SubReparo Cortex is built around the three base ingredients of a useful AI-agent system:

```text
1. External knowledge
2. Tools
3. Prompting
```

These map directly into the five AI-agent components that SubReparo must support:

```text
1. LLMs / brain
2. Prompting / instructions
3. Memory
4. External knowledge
5. Tools
```

SubReparo adds a sixth practical requirement on top:

```text
6. Verification and approval gates
```

That extra layer is what keeps the platform useful, auditable, and controlled instead of becoming an unsafe always-on bot.

## Core architecture

```text
                 SubReparo Cortex
                        |
   +--------------------+--------------------+
   |                    |                    |
Planning             Memory              Learning
   |                    |                    |
Tool Use          Verification        Multi-Agent Teams
   |                    |                    |
Code | Web Apps | Research | Reports | Monitoring | APIs
                        |
                 SubReparo Immune
                        |
          Detect -> Isolate -> Verify -> Recover
                        |
                 SubReparo Chain
        Repair proofs | Audit | Learning history
```

## Component mapping

### 1. LLMs / brain

The reasoning layer that interprets goals, writes plans, drafts code/docs, compares alternatives, and explains decisions.

### 2. Prompting / instructions

The operating rules, task templates, safety boundaries, approval rules, and role-specific instructions that shape how Cortex behaves.

### 3. Memory

Local project memory, task history, outcome records, audit logs, repair lessons, user preferences, and roadmap state.

### 4. External knowledge

Docs, repo files, uploaded references, issue trackers, research notes, APIs, project reports, and future approved knowledge sources.

### 5. Tools

GitHub, local analyzers, quality gates, CI, dashboards, reports, safe skill review, snapshots, incident bundles, SubReparo Immune, and SubReparo Chain.

### 6. Verification and approval gates

Quality checks, tests, smoke tests, explainability, rollback/snapshot records, approval queue, blocked-action rules, and proof-of-repair records.

## Operating principle

SubReparo Cortex should behave like a 24/7 human operator, but with stricter controls:

```text
observe -> plan -> act -> verify -> learn -> report -> repeat
```

## Human-control rule

Low-risk actions may be automated.

High-impact actions require user approval.

High-impact actions include:

- spending money;
- sending email externally;
- deleting data;
- changing production infrastructure;
- publishing public content;
- running aggressive security actions;
- sharing private data;
- legal, medical, financial, or safety-critical decisions.

## Core subsystems

### 1. Long-term memory

Stores durable knowledge about projects, decisions, results, failures, successful repairs, preferences, and known constraints.

### 2. Hierarchical planning

Breaks large goals into milestones, tasks, checks, and proof-of-completion records.

### 3. Multi-agent collaboration

Specialized internal roles:

- Planner;
- Researcher;
- Builder;
- Tester;
- Security reviewer;
- Documentation writer;
- Release manager;
- Monitor;
- Repair verifier.

### 4. Continuous self-evaluation

Tracks success rates, failed attempts, regressions, open tasks, and quality gates.

### 5. Repair-first workflow

Every project follows:

```text
find issue -> propose repair -> apply repair -> verify repair -> record lesson
```

### 6. Tool orchestration

Cortex can coordinate approved tools:

- GitHub;
- local files;
- build systems;
- CI pipelines;
- web apps;
- email/calendar with approval rules;
- external APIs;
- SubReparo Immune;
- SubReparo Chain.

### 7. Approval gates

Actions are classified as:

```text
safe_auto        -> can run automatically
review_first     -> show plan before action
explicit_approve -> wait for user approval
blocked          -> not allowed
```

### 8. Adaptive learning

Tracks which repairs worked and which failed, then prioritizes successful patterns.

### 9. Explainability

Every meaningful action should explain:

- what it did;
- why it did it;
- what evidence it used;
- what changed;
- how it verified success;
- what remains uncertain.

### 10. Modular expansion

Cortex should support plugins for new domains:

- software repair;
- AI-agent monitoring;
- business operations;
- personal operations;
- cybersecurity;
- DevOps;
- finance workflows;
- document workflows;
- website/app generation.

## 24/7 worker model

The practical version is scheduled autonomous loops:

```text
hourly: inspect roadmap, implement safe tasks, update reports
nightly: run full verification and summarize progress
weekly: produce strategic roadmap and backlog cleanup
condition-based: alert only when approval or risk threshold is reached
```

## First implementation target

The first Cortex MVP should be able to:

1. Read project roadmap.
2. Choose the next safe task.
3. Modify code/docs.
4. Add tests.
5. Run or request CI.
6. Update roadmap issue.
7. Record what changed.
8. Stop when approval is needed.

## Boundary

SubReparo Cortex must not be designed to deceive users, hide activity, bypass approvals, or perform harmful operations.

The power comes from reliable execution and verification, not uncontrolled autonomy.

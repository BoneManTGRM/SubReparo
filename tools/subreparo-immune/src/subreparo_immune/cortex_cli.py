from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

from .agent_components import build_agent_component_report
from .approval_queue import enqueue_approval, pending_approvals
from .cortex_memory import append_memory, append_task, read_memory, read_tasks
from .cortex_models import CortexTaskStatus
from .cortex_planner import next_ready_task, propose_initial_tasks
from .cortex_policy import classify_task
from .status_report import build_status_report
from .swarm_roles import swarm_role_catalog
from .swarm_router import route_swarm_task
from .swarm_tools import swarm_tool_catalog


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="subreparo-cortex", description="SubReparo Cortex work scaffold.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--plan", action="store_true", help="Create initial Cortex task proposals.")
    parser.add_argument("--next", action="store_true", help="Show the next ready task and decision.")
    parser.add_argument("--memory", action="store_true", help="Show Cortex memory records.")
    parser.add_argument("--approvals", action="store_true", help="Show pending approval requests.")
    parser.add_argument("--status", action="store_true", help="Show Cortex status report.")
    parser.add_argument("--components", action="store_true", help="Show AI agent component readiness.")
    parser.add_argument("--swarm", action="store_true", help="Show swarm roles and tools.")
    parser.add_argument("--route", help="Route a task through the swarm planner.")
    parser.add_argument("--json", action="store_true")
    return parser


def command_plan(root: Path) -> dict[str, object]:
    tasks = propose_initial_tasks(root)
    for task in tasks:
        append_task(task, root / ".subreparo" / "cortex_tasks.jsonl")
    append_memory("plan_created", {"task_count": len(tasks)}, root / ".subreparo" / "cortex_memory.jsonl")
    return {"tasks": [task.to_dict() for task in tasks]}


def command_next(root: Path) -> dict[str, object]:
    tasks = read_tasks(root / ".subreparo" / "cortex_tasks.jsonl")
    if not tasks:
        tasks = propose_initial_tasks(root)
    task = next_ready_task(tasks)
    if task is None:
        return {"next_task": None, "decision": None}
    decision = classify_task(task)
    next_status = CortexTaskStatus.RUNNING if decision.allowed else CortexTaskStatus.WAITING_APPROVAL
    updated = replace(task, status=next_status)
    if not decision.allowed:
        enqueue_approval(updated, decision.approval_level, decision.reason, root / ".subreparo" / "approval_queue.jsonl")
    append_memory("next_task_selected", {"task": updated.to_dict(), "decision": decision.to_dict()}, root / ".subreparo" / "cortex_memory.jsonl")
    return {"next_task": updated.to_dict(), "decision": decision.to_dict()}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.path).resolve()
    if args.plan:
        payload = command_plan(root)
    elif args.next:
        payload = command_next(root)
    elif args.memory:
        payload = {"memory": read_memory(root / ".subreparo" / "cortex_memory.jsonl")}
    elif args.approvals:
        payload = {"approvals": [item.to_dict() for item in pending_approvals(root / ".subreparo" / "approval_queue.jsonl")]}
    elif args.status:
        payload = build_status_report(root)
    elif args.components:
        payload = build_agent_component_report(root)
    elif args.swarm:
        payload = {"roles": swarm_role_catalog(), "tools": swarm_tool_catalog()}
    elif args.route:
        payload = {"route": route_swarm_task(args.route).to_dict()}
    else:
        payload = {
            "message": "Use --plan, --next, --memory, --approvals, --status, --components, --swarm, or --route.",
            "commands": [
                "subreparo-cortex . --plan",
                "subreparo-cortex . --next",
                "subreparo-cortex . --memory",
                "subreparo-cortex . --approvals",
                "subreparo-cortex . --status",
                "subreparo-cortex . --components",
                "subreparo-cortex . --swarm",
                "subreparo-cortex . --route 'run quality checks'",
            ],
        }

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

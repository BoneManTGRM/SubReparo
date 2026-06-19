from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

from .cortex_memory import append_memory, append_task, read_memory, read_tasks
from .cortex_models import CortexTaskStatus
from .cortex_planner import next_ready_task, propose_initial_tasks
from .cortex_policy import classify_task


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="subreparo-cortex", description="SubReparo Cortex autonomous work scaffold.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--plan", action="store_true", help="Create initial Cortex task proposals.")
    parser.add_argument("--next", action="store_true", help="Show the next ready task and approval decision.")
    parser.add_argument("--memory", action="store_true", help="Show Cortex memory records.")
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
    else:
        payload = {
            "message": "Use --plan, --next, or --memory.",
            "commands": ["subreparo-cortex . --plan", "subreparo-cortex . --next", "subreparo-cortex . --memory"],
        }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

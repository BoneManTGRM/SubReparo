from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .cortex_models import CortexTask

MEMORY_PATH = Path(".subreparo") / "cortex_memory.jsonl"
TASKS_PATH = Path(".subreparo") / "cortex_tasks.jsonl"


def append_memory(event: str, payload: dict[str, Any], path: Path = MEMORY_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"event": event, "payload": payload}, sort_keys=True) + "\n")


def read_memory(path: Path = MEMORY_PATH) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"event": "unreadable", "payload": {"raw": line}})
    return rows


def append_task(task: CortexTask, path: Path = TASKS_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(task.to_dict(), sort_keys=True) + "\n")


def read_tasks(path: Path = TASKS_PATH) -> list[CortexTask]:
    if not path.exists():
        return []
    tasks: list[CortexTask] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        tasks.append(CortexTask.from_dict(json.loads(line)))
    return tasks

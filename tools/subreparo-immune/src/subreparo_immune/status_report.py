from __future__ import annotations

from pathlib import Path
from typing import Any

from .approval_queue import pending_approvals
from .cortex_memory import read_memory, read_tasks
from .outcome_records import list_outcomes
from .trends import risk_trends


def build_status_report(root: Path) -> dict[str, Any]:
    root = root.resolve()
    state = root / ".subreparo"
    return {
        "schema": "subreparo.status_report.v1",
        "task_count": len(read_tasks(state / "cortex_tasks.jsonl")),
        "memory_count": len(read_memory(state / "cortex_memory.jsonl")),
        "pending_approvals": len(pending_approvals(state / "approval_queue.jsonl")),
        "outcome_count": len(list_outcomes(state / "outcome_records.jsonl")),
        "risk_trends": risk_trends(root),
    }

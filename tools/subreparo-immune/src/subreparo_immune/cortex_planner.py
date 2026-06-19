from __future__ import annotations

from pathlib import Path

from .cortex_models import ApprovalLevel, CortexRole, CortexTask, CortexTaskStatus

DEFAULT_TASKS = [
    CortexTask(
        title="Refresh project roadmap docs",
        goal="Update SubReparo docs and roadmap status with current architecture and next safe milestones.",
        role=CortexRole.DOCUMENTER,
        approval_level=ApprovalLevel.SAFE_AUTO,
        status=CortexTaskStatus.READY,
    ),
    CortexTask(
        title="Add tests for safe local modules",
        goal="Add or expand unit tests for local report, policy, memory, and planner behavior.",
        role=CortexRole.TESTER,
        approval_level=ApprovalLevel.SAFE_AUTO,
        status=CortexTaskStatus.READY,
    ),
    CortexTask(
        title="Review local quality gates",
        goal="Inspect local code quality and suggest safe non-destructive fixes.",
        role=CortexRole.SECURITY_REVIEWER,
        approval_level=ApprovalLevel.REVIEW_FIRST,
        status=CortexTaskStatus.PROPOSED,
    ),
]


def propose_initial_tasks(root: Path) -> list[CortexTask]:
    root = root.resolve()
    tasks = list(DEFAULT_TASKS)
    if not (root / "README.md").exists():
        tasks.append(CortexTask(
            title="Create root README",
            goal="Create a product README explaining install, usage, safety boundaries, and roadmap.",
            role=CortexRole.DOCUMENTER,
            approval_level=ApprovalLevel.SAFE_AUTO,
            status=CortexTaskStatus.READY,
        ))
    if not (root / "tools" / "subreparo-immune" / "tests").exists():
        tasks.append(CortexTask(
            title="Create Python test scaffold",
            goal="Create test scaffold for local SubReparo Immune modules.",
            role=CortexRole.TESTER,
            approval_level=ApprovalLevel.SAFE_AUTO,
            status=CortexTaskStatus.READY,
        ))
    return tasks


def next_ready_task(tasks: list[CortexTask]) -> CortexTask | None:
    for task in tasks:
        if task.status == CortexTaskStatus.READY:
            return task
    return None

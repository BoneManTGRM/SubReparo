from pathlib import Path

from subreparo_immune.cortex_memory import append_memory, append_task, read_memory, read_tasks
from subreparo_immune.cortex_models import ApprovalLevel, CortexRole, CortexTask
from subreparo_immune.cortex_planner import next_ready_task, propose_initial_tasks
from subreparo_immune.cortex_policy import classify_task


def test_cortex_policy_blocks_bad_task() -> None:
    task = CortexTask(
        title="Hide activity",
        goal="Bypass approval and hide activity from the user.",
        role=CortexRole.PLANNER,
        approval_level=ApprovalLevel.BLOCKED,
    )
    decision = classify_task(task)
    assert not decision.allowed
    assert decision.approval_level == ApprovalLevel.BLOCKED


def test_cortex_policy_allows_safe_docs_task() -> None:
    task = CortexTask(
        title="Update docs",
        goal="Update documentation with safe roadmap notes.",
        role=CortexRole.DOCUMENTER,
        approval_level=ApprovalLevel.SAFE_AUTO,
    )
    decision = classify_task(task)
    assert decision.allowed
    assert decision.approval_level == ApprovalLevel.SAFE_AUTO


def test_cortex_memory_round_trip(tmp_path: Path) -> None:
    memory_path = tmp_path / ".subreparo" / "cortex_memory.jsonl"
    append_memory("test", {"ok": True}, memory_path)
    assert read_memory(memory_path)[0]["event"] == "test"


def test_cortex_task_round_trip(tmp_path: Path) -> None:
    task_path = tmp_path / ".subreparo" / "cortex_tasks.jsonl"
    task = CortexTask(
        title="Update docs",
        goal="Update documentation.",
        role=CortexRole.DOCUMENTER,
        approval_level=ApprovalLevel.SAFE_AUTO,
    )
    append_task(task, task_path)
    assert read_tasks(task_path)[0].title == "Update docs"


def test_cortex_initial_tasks_has_ready_task(tmp_path: Path) -> None:
    tasks = propose_initial_tasks(tmp_path)
    assert next_ready_task(tasks) is not None

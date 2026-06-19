from pathlib import Path

from subreparo_immune.approval_queue import enqueue_approval, pending_approvals
from subreparo_immune.cortex_models import ApprovalLevel, CortexRole, CortexTask
from subreparo_immune.outcome_records import append_outcome, list_outcomes
from subreparo_immune.snapshot import create_snapshot
from subreparo_immune.status_report import build_status_report


def test_approval_queue_round_trip(tmp_path: Path) -> None:
    task = CortexTask(
        title="Review deployment",
        goal="Review production deployment before action.",
        role=CortexRole.RELEASE_MANAGER,
        approval_level=ApprovalLevel.EXPLICIT_APPROVE,
    )
    queue_path = tmp_path / ".subreparo" / "approval_queue.jsonl"
    enqueue_approval(task, ApprovalLevel.EXPLICIT_APPROVE, "needs review", queue_path)
    approvals = pending_approvals(queue_path)
    assert len(approvals) == 1
    assert approvals[0].task["title"] == "Review deployment"


def test_outcome_records_round_trip(tmp_path: Path) -> None:
    path = tmp_path / ".subreparo" / "outcome_records.jsonl"
    append_outcome("Quality gate", "passed", "compile checks passed", ["compileall"], ["pytest"], path)
    records = list_outcomes(path)
    assert len(records) == 1
    assert records[0].status == "passed"


def test_snapshot_skips_subreparo_state(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("print('ok')\n", encoding="utf-8")
    (tmp_path / ".subreparo").mkdir()
    (tmp_path / ".subreparo" / "secret.txt").write_text("local state\n", encoding="utf-8")
    record = create_snapshot(tmp_path)
    assert Path(record.archive_path).exists()
    assert record.file_count == 1


def test_status_report_shape(tmp_path: Path) -> None:
    payload = build_status_report(tmp_path)
    assert payload["schema"] == "subreparo.status_report.v1"
    assert payload["pending_approvals"] == 0

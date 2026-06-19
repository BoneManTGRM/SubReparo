import json
from pathlib import Path

from subreparo_immune.approval_queue import enqueue_approval
from subreparo_immune.cortex_memory import append_memory, append_task
from subreparo_immune.cortex_models import ApprovalLevel, CortexRole, CortexTask
from subreparo_immune.dashboard import render_approvals, render_page, render_snapshots, tail_jsonl
from subreparo_immune.outcome_records import append_outcome


def test_tail_jsonl_skips_missing_file(tmp_path: Path) -> None:
    assert tail_jsonl(tmp_path / "missing.jsonl") == []


def test_tail_jsonl_keeps_unreadable_rows(tmp_path: Path) -> None:
    path = tmp_path / "events.jsonl"
    path.write_text('{"ok": true}\nnot-json\n', encoding="utf-8")

    rows = tail_jsonl(path)

    assert rows[0] == {"ok": True}
    assert rows[1] == {"unreadable": "not-json"}


def test_render_approvals_lists_pending_task(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    task = CortexTask(
        title="Review deploy",
        goal="Deploy production change.",
        role=CortexRole.RELEASE_MANAGER,
        approval_level=ApprovalLevel.EXPLICIT_APPROVE,
    )
    enqueue_approval(
        task,
        ApprovalLevel.EXPLICIT_APPROVE,
        "Explicit approval required.",
        tmp_path / ".subreparo" / "approval_queue.jsonl",
    )

    rendered = render_approvals()

    assert "Review deploy" in rendered
    assert "explicit_approve" in rendered


def test_render_snapshots_lists_latest_manifest(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    manifest = tmp_path / ".subreparo" / "snapshots" / "snapshot_manifest.jsonl"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(
        json.dumps({"archive_path": "snapshot.tar.gz", "file_count": 3}) + "\n",
        encoding="utf-8",
    )

    rendered = render_snapshots()

    assert "snapshot.tar.gz" in rendered
    assert "file_count" in rendered


def test_render_page_includes_cortex_metrics(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    state = tmp_path / ".subreparo"
    task = CortexTask(
        title="Update docs",
        goal="Update local docs.",
        role=CortexRole.DOCUMENTER,
        approval_level=ApprovalLevel.SAFE_AUTO,
    )
    append_task(task, state / "cortex_tasks.jsonl")
    append_memory("test", {"ok": True}, state / "cortex_memory.jsonl")
    append_outcome(
        "Dashboard test",
        "completed",
        "Validated dashboard rendering.",
        path=state / "outcome_records.jsonl",
    )

    page = render_page()

    assert "Cortex control layer" in page
    assert "Tasks: 1" in page
    assert "Memory: 1" in page
    assert "Outcomes: 1" in page

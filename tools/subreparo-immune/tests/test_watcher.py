from __future__ import annotations

from pathlib import Path

from subreparo_immune import watcher


def _events_by_path(events: list[dict[str, object]]) -> dict[str, str]:
    return {str(event["path"]): str(event["event_type"]) for event in events}


def test_file_snapshot_diff_detects_created_modified_and_deleted(tmp_path: Path) -> None:
    deleted = tmp_path / "deleted.txt"
    modified = tmp_path / "modified.txt"
    deleted.write_text("delete me", encoding="utf-8")
    modified.write_text("before", encoding="utf-8")

    first = watcher.build_file_snapshot(tmp_path)

    deleted.unlink()
    modified.write_text("after with size change", encoding="utf-8")
    (tmp_path / "created.ps1").write_text("Write-Output 'new local script'", encoding="utf-8")

    second = watcher.build_file_snapshot(tmp_path)
    events = watcher.diff_file_snapshots(first, second)
    by_path = _events_by_path(events)

    assert by_path["deleted.txt"] == "deleted"
    assert by_path["modified.txt"] == "modified"
    assert by_path["created.ps1"] == "created"
    assert next(event for event in events if event["path"] == "created.ps1")["severity"] == "medium"


def test_poll_file_events_is_privacy_preserving(tmp_path: Path) -> None:
    secret = tmp_path / "secret.txt"
    secret.write_text("do not read or hash this content", encoding="utf-8")

    payload = watcher.poll_file_events(tmp_path)
    snapshot = payload["snapshot"]
    file_record = snapshot["files"]["secret.txt"]

    assert payload["backend"] == "polling_snapshot"
    assert file_record["size"] == len("do not read or hash this content")
    assert "sha256" not in file_record
    assert payload["safety"]["content_reading"] is False


def test_build_watch_plan_reports_native_backend(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(watcher, "native_watchdog_available", lambda: True)

    plan = watcher.build_watch_plan(tmp_path)

    assert plan["backend"] == "native_watchdog"
    assert plan["native_available"] is True
    assert plan["safety"]["alert_only_by_default"] is True


def test_collect_native_file_events_falls_back_without_watchdog(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(watcher, "native_watchdog_available", lambda: False)

    payload = watcher.collect_native_file_events([tmp_path], duration=0.1)

    assert payload["backend"] == "polling_fallback"
    assert payload["native_available"] is False
    assert payload["events"] == []
    assert "optional native watcher dependency" in payload["recommendation"]

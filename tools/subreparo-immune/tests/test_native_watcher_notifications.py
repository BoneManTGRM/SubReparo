from pathlib import Path

from subreparo_immune.native_watcher import append_watch_alert, build_native_watcher_status, make_alert
from subreparo_immune.notifications import create_notification, write_notification


def test_native_watcher_status_is_local(tmp_path: Path) -> None:
    status = build_native_watcher_status(tmp_path)

    assert status["schema"] == "subreparo.native_watcher.v1"
    assert status["local_only"] is True


def test_watch_alert_appends_jsonl(tmp_path: Path) -> None:
    alert = make_alert("created", tmp_path / "file.txt")
    append_watch_alert(tmp_path, alert)

    assert (tmp_path / ".subreparo" / "watch_alerts.jsonl").exists()


def test_notification_records_jsonl(tmp_path: Path) -> None:
    notification = create_notification("SubReparo", "Local alert", level="info")
    path = write_notification(tmp_path, notification)

    assert path.exists()
    assert "subreparo.notification.v1" in path.read_text(encoding="utf-8")

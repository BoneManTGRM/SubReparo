from pathlib import Path

from subreparo_immune.monitor_cli import run_once
from subreparo_immune.setup_wizard import create_setup_profile


def test_monitor_can_use_watch_plan_targets(tmp_path: Path) -> None:
    watched = tmp_path / "watched"
    watched.mkdir()
    create_setup_profile(tmp_path, watched_paths=[str(watched)])

    payload = run_once(tmp_path, all_targets=True)

    assert "monitored_targets" in payload
    assert any(item["path"] == str(watched) for item in payload["monitored_targets"])
    assert any(item["kind"] == "process" for item in payload["monitored_targets"])

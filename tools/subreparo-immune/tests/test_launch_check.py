from pathlib import Path

from subreparo_immune.launch_check import build_launch_check


def test_launch_check_reports_scripts_and_docs(tmp_path: Path) -> None:
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "start-subreparo-control-center.sh").write_text("#!/usr/bin/env bash\n", encoding="utf-8")
    (tmp_path / "scripts" / "start-subreparo-control-center.command").write_text("#!/usr/bin/env bash\n", encoding="utf-8")
    (tmp_path / "scripts" / "start-subreparo-control-center.cmd").write_text("@echo off\n", encoding="utf-8")
    (tmp_path / "subreparo" / "docs").mkdir(parents=True)
    (tmp_path / "subreparo" / "docs" / "CONTROL_CENTER_LAUNCH.md").write_text("# Launch\n", encoding="utf-8")
    (tmp_path / "subreparo" / "docs" / "DESKTOP_APP_VISION.md").write_text("# Vision\n", encoding="utf-8")

    payload = build_launch_check(tmp_path)

    assert payload["schema"] == "subreparo.control_center_launch_check.v1"
    assert payload["localhost_only"] is True
    assert payload["scripts"]["unix"]["present"] is True
    assert payload["scripts"]["windows_cmd"]["present"] is True
    assert payload["docs"]["launch_guide"]["present"] is True

from pathlib import Path

from subreparo_immune.watcher import build_watch_plan, default_watch_targets


def test_default_watch_targets_cover_standard_locations(tmp_path: Path) -> None:
    targets = default_watch_targets(tmp_path)
    kinds = {target["kind"] for target in targets}

    assert {"downloads", "desktop", "documents", "temp"}.issubset(kinds)
    assert "browser_downloads" in kinds
    assert "archive_extraction" in kinds
    assert "process" in kinds
    assert "removable" in kinds


def test_watch_plan_is_local_and_passive(tmp_path: Path) -> None:
    plan = build_watch_plan(tmp_path)

    assert plan["schema"] == "subreparo.watch_plan.v1"
    assert plan["safety"]["local_only"] is True
    assert plan["safety"]["alert_only_by_default"] is True

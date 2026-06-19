import json
from pathlib import Path

from subreparo_immune.alerts import append_alert_inbox, build_native_alert_report
from subreparo_immune.alerts_cli import main as alerts_main
from subreparo_immune.fleet_cli import main as fleet_main
from subreparo_immune.fleet_dashboard import build_fleet_dashboard
from subreparo_immune.installer_cli import main as installer_main
from subreparo_immune.installer_manifest import build_installer_manifest
from subreparo_immune.tray_app import build_tray_manifest, write_tray_manifest
from subreparo_immune.tray_cli import main as tray_main
from subreparo_immune.updater import build_update_plan, write_update_plan
from subreparo_immune.updater_cli import main as updater_main


def test_native_alert_report_builds_from_watch_alerts(tmp_path: Path) -> None:
    state = tmp_path / ".subreparo"
    state.mkdir()
    event = {"severity": "high", "event_type": "created", "path": "Downloads/item"}
    (state / "watch_alerts.jsonl").write_text(
        json.dumps(event) + "\n",
        encoding="utf-8",
    )

    report = build_native_alert_report(tmp_path)

    assert report["schema"] == "subreparo.native_alerts.v1"
    assert report["pending_plan_count"] == 1
    assert report["plans"][0]["severity"] == "high"
    assert report["safety"]["local_only"] is True


def test_append_alert_inbox_writes_local_records(tmp_path: Path) -> None:
    report = build_native_alert_report(tmp_path)
    path = append_alert_inbox(tmp_path, list(report["plans"]))

    assert path.name == "native_alerts.jsonl"
    assert path.exists()


def test_tray_manifest_exposes_safe_menu(tmp_path: Path) -> None:
    manifest = build_tray_manifest(tmp_path)

    assert manifest["schema"] == "subreparo.desktop_tray.v1"
    assert manifest["backend"]["starts_gui_by_default"] is False
    assert {item["id"] for item in manifest["menu_items"]} >= {"open_dashboard", "alerts"}


def test_write_tray_manifest(tmp_path: Path) -> None:
    path = write_tray_manifest(tmp_path)

    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema"] == "subreparo.desktop_tray.v1"


def test_installer_manifest_covers_desktop_platforms() -> None:
    manifest = build_installer_manifest()

    platforms = {item["platform"] for item in manifest["platforms"]}
    entrypoints = set(manifest["platforms"][0]["entrypoints"])
    assert platforms == {"windows", "macos", "linux"}
    assert {"subreparo-updater", "subreparo-fleet"} <= entrypoints
    assert manifest["release_gate"]["manual_review_required"] is True


def test_update_plan_is_dry_run_by_default(tmp_path: Path) -> None:
    plan = build_update_plan("9.9.9")
    path = write_update_plan(tmp_path, "9.9.9")

    assert plan["status"] == "approval_required"
    assert plan["auto_apply_default"] is False
    assert path.exists()


def test_fleet_dashboard_is_local_manifest(tmp_path: Path) -> None:
    dashboard = build_fleet_dashboard(tmp_path)

    assert dashboard["schema"] == "subreparo.fleet_dashboard.v1"
    assert dashboard["mode"] == "local_manifest"
    assert dashboard["totals"]["nodes"] == 1


def test_platform_completion_clis_return_json(tmp_path: Path, capsys) -> None:
    commands = [
        (alerts_main, [str(tmp_path), "--json"]),
        (tray_main, [str(tmp_path), "--json"]),
        (installer_main, [str(tmp_path), "--json"]),
        (updater_main, [str(tmp_path), "--json"]),
        (fleet_main, [str(tmp_path), "--json"]),
    ]

    for func, argv in commands:
        assert func(argv) == 0

    output = capsys.readouterr().out
    assert "subreparo.native_alerts.v1" in output
    assert "subreparo.desktop_tray.v1" in output
    assert "subreparo.installers.v1" in output
    assert "subreparo.update_plan.v1" in output
    assert "subreparo.fleet_dashboard.v1" in output

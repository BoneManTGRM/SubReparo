from pathlib import Path

from subreparo_immune.dependency_risk import scan_dependency_risk
from subreparo_immune.modes import get_mode, mode_catalog
from subreparo_immune.notifications import create_notification, write_notification
from subreparo_immune.quarantine import list_records, remove_staged_record, stage_file
from subreparo_immune.sbom import generate_sbom, write_sbom


def test_mode_catalog_contains_simple() -> None:
    names = {item["name"] for item in mode_catalog()}
    assert "simple" in names
    assert get_mode("missing").name == "simple"


def test_dependency_risk_flags_unpinned_requirement(tmp_path: Path) -> None:
    (tmp_path / "requirements.txt").write_text("requests\n", encoding="utf-8")
    findings = scan_dependency_risk(tmp_path)
    assert any("not pinned" in finding.message for finding in findings)


def test_sbom_generates_manifest_component(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
    payload = generate_sbom(tmp_path)
    assert payload["component_count"] == 1
    target = write_sbom(tmp_path)
    assert target.exists()


def test_notification_write(tmp_path: Path) -> None:
    path = write_notification(tmp_path, create_notification("Test", "Message", "info"))
    assert path.exists()


def test_remove_staged_record_only_removes_staged_file(tmp_path: Path) -> None:
    target = tmp_path / "tool.exe"
    target.write_bytes(b"MZ")
    stage_file(tmp_path, target, reason="test")
    removed = remove_staged_record(tmp_path, 0)
    assert removed.original_path.endswith("tool.exe")
    assert list_records(tmp_path / ".subreparo") == []

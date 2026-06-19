from pathlib import Path

from subreparo_immune.setup_wizard import create_setup_profile, load_setup_profile
from subreparo_immune.signed_reports import create_report_signature, verify_report_signature
from subreparo_immune.watcher import build_watch_plan


def test_setup_profile_persists_local_first_defaults(tmp_path: Path) -> None:
    profile = create_setup_profile(tmp_path, mode="developer", watched_paths=[str(tmp_path / "src")])
    loaded = load_setup_profile(tmp_path)

    assert profile.mode == "developer"
    assert loaded is not None
    assert loaded.local_only is True
    assert loaded.approval_gate_high_impact is True
    assert loaded.watched_paths == (str(tmp_path / "src"),)


def test_watch_plan_uses_setup_targets(tmp_path: Path) -> None:
    watched = tmp_path / "watched"
    watched.mkdir()
    create_setup_profile(tmp_path, watched_paths=[str(watched)])

    plan = build_watch_plan(tmp_path)

    assert plan["schema"] == "subreparo.watch_plan.v1"
    assert plan["targets"][0]["path"] == str(watched)
    assert plan["targets"][0]["exists"] is True
    assert plan["safety"]["non_destructive"] is True


def test_report_signature_create_and_verify(tmp_path: Path) -> None:
    state = tmp_path / ".subreparo"
    state.mkdir()
    (state / "report.md").write_text("# report\n", encoding="utf-8")
    (state / "chain_export.json").write_text("{}\n", encoding="utf-8")

    signature = create_report_signature(tmp_path)
    verification = verify_report_signature(tmp_path)

    assert signature["schema"] == "subreparo.report_signature.v1"
    assert signature["signature_type"] == "sha256_manifest"
    assert verification["valid"] is True


def test_report_signature_detects_changed_artifact(tmp_path: Path) -> None:
    state = tmp_path / ".subreparo"
    state.mkdir()
    report = state / "report.md"
    report.write_text("# report\n", encoding="utf-8")
    create_report_signature(tmp_path)
    report.write_text("# changed\n", encoding="utf-8")

    verification = verify_report_signature(tmp_path)

    assert verification["valid"] is False

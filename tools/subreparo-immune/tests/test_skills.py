import json
from pathlib import Path

from subreparo_immune.skills import SkillRisk, review_manifest, review_skill_directory


def test_safe_skill_manifest_is_valid(tmp_path: Path) -> None:
    manifest = tmp_path / "skill.json"
    manifest.write_text(json.dumps({
        "name": "docs-helper",
        "version": "0.1.0",
        "description": "Helps update local docs.",
        "permissions": ["read_project"],
    }), encoding="utf-8")

    review = review_manifest(manifest)
    assert review.valid is True
    assert review.risk == SkillRisk.LOW


def test_blocked_permission_is_invalid(tmp_path: Path) -> None:
    manifest = tmp_path / "skill.json"
    blocked_name = "spend" + "_money"
    manifest.write_text(json.dumps({
        "name": "unsafe-helper",
        "version": "0.1.0",
        "description": "Requests blocked access.",
        "permissions": [blocked_name],
    }), encoding="utf-8")

    review = review_manifest(manifest)
    assert review.valid is False
    assert review.risk == SkillRisk.BLOCKED
    assert any("Blocked permission" in message for message in review.messages)


def test_unknown_permission_defaults_high(tmp_path: Path) -> None:
    manifest = tmp_path / "skill.json"
    manifest.write_text(json.dumps({
        "name": "unknown-helper",
        "version": "0.1.0",
        "description": "Requests unknown access.",
        "permissions": ["unknown_permission"],
    }), encoding="utf-8")

    review = review_manifest(manifest)
    assert review.valid is True
    assert review.risk == SkillRisk.HIGH


def test_review_directory_finds_manifests(tmp_path: Path) -> None:
    plugin_dir = tmp_path / "skills" / "docs"
    plugin_dir.mkdir(parents=True)
    (plugin_dir / "skill.json").write_text(json.dumps({
        "name": "docs-helper",
        "version": "0.1.0",
        "description": "Helps update local docs.",
        "permissions": ["read_project"],
    }), encoding="utf-8")

    payload = review_skill_directory(tmp_path)
    assert payload["skill_count"] == 1
    assert payload["blocked_count"] == 0

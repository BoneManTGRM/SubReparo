from pathlib import Path

from subreparo_immune.agent_factory import (
    build_agent_manifest,
    create_agent_from_blueprint,
    list_blueprints,
    list_registered_agents,
    review_agent_manifest,
)


def test_blueprints_include_core_templates() -> None:
    keys = {item["key"] for item in list_blueprints()}
    assert "code_review" in keys
    assert "test_builder" in keys
    assert "docs_writer" in keys


def test_low_risk_manifest_can_register() -> None:
    manifest = build_agent_manifest("code_review")
    review = review_agent_manifest(manifest)
    assert review["risk"] == "low"
    assert review["approved_for_registry"] is True


def test_write_permission_requires_review() -> None:
    manifest = build_agent_manifest("docs_writer")
    review = review_agent_manifest(manifest)
    assert review["risk"] == "medium"
    assert review["approved_for_registry"] is False


def test_scaffold_and_registry_record(tmp_path: Path) -> None:
    result = create_agent_from_blueprint(tmp_path, "code_review", register=True)
    item_id = result["manifest"]["id"]
    assert (tmp_path / ".subreparo" / "factory" / "agents" / item_id / "agent.json").exists()
    records = list_registered_agents(tmp_path)
    assert len(records) == 1
    assert records[0]["registered"] is True

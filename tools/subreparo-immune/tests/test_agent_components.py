from pathlib import Path

from subreparo_immune.agent_components import build_agent_component_report
from subreparo_immune.cortex_cli import main as cortex_main


def test_agent_component_report_registers_required_components(tmp_path: Path) -> None:
    report = build_agent_component_report(tmp_path)

    names = {component["name"] for component in report["components"]}

    assert report["schema"] == "subreparo.agent_components.v1"
    assert report["component_count"] == 5
    assert report["registered_count"] == 5
    assert report["minimal_agent_ingredients"] == [
        "external_knowledge",
        "tools",
        "prompting",
    ]
    assert names == {
        "LLM brain",
        "Prompting and instructions",
        "Memory",
        "External knowledge",
        "Tools",
    }


def test_agent_component_report_detects_local_memory_artifact(tmp_path: Path) -> None:
    source = tmp_path / "src" / "subreparo_immune"
    source.mkdir(parents=True)
    (source / "cortex_memory.py").write_text("# memory artifact\n", encoding="utf-8")

    report = build_agent_component_report(tmp_path)
    memory = next(component for component in report["components"] if component["key"] == "memory")

    assert memory["artifact_present"] is True
    assert memory["operational"] is True


def test_llm_component_is_registered_but_not_connected_by_default(tmp_path: Path) -> None:
    report = build_agent_component_report(tmp_path)
    brain = next(component for component in report["components"] if component["key"] == "llm_brain")

    assert brain["implementation_level"] == "registered_not_connected"
    assert brain["operational"] is False
    assert "external model calls" in brain["approval_required_for"]


def test_cortex_components_command_outputs_json(tmp_path: Path, capsys) -> None:
    exit_code = cortex_main([str(tmp_path), "--components", "--json"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "subreparo.agent_components.v1" in captured.out
    assert "LLM brain" in captured.out

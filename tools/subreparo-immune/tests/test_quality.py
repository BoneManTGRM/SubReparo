from pathlib import Path

from subreparo_immune.quality import default_quality_commands, run_quality


def test_default_quality_commands_for_non_tool_project(tmp_path: Path) -> None:
    commands = default_quality_commands(tmp_path)
    assert commands
    assert "compileall" in commands[0]


def test_quality_compileall_passes_on_simple_project(tmp_path: Path) -> None:
    module = tmp_path / "sample.py"
    module.write_text("x = 1\n", encoding="utf-8")
    payload = run_quality(tmp_path)
    assert payload["passed"] is True
    assert payload["checks"]

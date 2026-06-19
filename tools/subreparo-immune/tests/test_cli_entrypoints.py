from pathlib import Path

from subreparo_immune.modes_cli import main as modes_main
from subreparo_immune.quarantine_cli import main as quarantine_main
from subreparo_immune.sbom_cli import main as sbom_main


def test_modes_cli_json(capsys) -> None:
    assert modes_main(["--json"]) == 0
    output = capsys.readouterr().out
    assert "simple" in output


def test_sbom_cli_json(tmp_path: Path, capsys) -> None:
    (tmp_path / "requirements.txt").write_text("requests==2.0.0\n", encoding="utf-8")
    assert sbom_main([str(tmp_path), "--json"]) == 0
    output = capsys.readouterr().out
    assert "component_count" in output


def test_quarantine_cli_empty(tmp_path: Path, capsys) -> None:
    assert quarantine_main([str(tmp_path), "--json"]) == 0
    output = capsys.readouterr().out
    assert "records" in output

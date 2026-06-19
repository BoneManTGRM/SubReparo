from pathlib import Path

from subreparo_immune.pdf_report import create_pdf_report
from subreparo_immune.pdf_report_cli import main as pdf_report_main


def test_pdf_report_writes_file_header(tmp_path: Path) -> None:
    state = tmp_path / ".subreparo"
    state.mkdir()
    (state / "report.md").write_text("# SubReparo\nScore: 100\n", encoding="utf-8")

    payload = create_pdf_report(tmp_path)
    output_path = Path(payload["path"])

    assert payload["schema"] == "subreparo.pdf_report.v1"
    assert output_path.exists()
    assert output_path.read_bytes().startswith(b"%PDF-1.4")


def test_pdf_report_cli_runs_json(tmp_path: Path, capsys) -> None:
    exit_code = pdf_report_main([str(tmp_path), "--json"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "subreparo.pdf_report.v1" in captured.out

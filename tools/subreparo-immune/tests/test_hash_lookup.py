from pathlib import Path

from subreparo_immune.hash_lookup import build_hash_lookup
from subreparo_immune.hash_lookup_cli import main as hash_lookup_main


def test_hash_lookup_exports_hashes_without_content(tmp_path: Path) -> None:
    script = tmp_path / "tool.py"
    script.write_text("print('safe fixture')\n", encoding="utf-8")

    payload = build_hash_lookup(tmp_path)

    assert payload["schema"] == "subreparo.hash_lookup.v1"
    assert payload["hash_only"] is True
    assert payload["raw_file_content_included"] is False
    assert payload["records"][0]["relative_path"] == "tool.py"
    assert "safe fixture" not in str(payload)
    assert (tmp_path / ".subreparo" / "hash_lookup.json").exists()


def test_hash_lookup_cli_runs_json(tmp_path: Path, capsys) -> None:
    (tmp_path / "app.sh").write_text("echo ok\n", encoding="utf-8")

    exit_code = hash_lookup_main([str(tmp_path), "--json"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "subreparo.hash_lookup.v1" in captured.out

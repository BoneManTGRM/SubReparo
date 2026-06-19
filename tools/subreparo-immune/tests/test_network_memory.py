import json
from pathlib import Path

from subreparo_immune.network_memory import build_network_memory
from subreparo_immune.network_memory_cli import main as network_memory_main


def test_network_memory_detects_new_repeated_and_dns_patterns(tmp_path: Path) -> None:
    state = tmp_path / ".subreparo"
    state.mkdir()
    rows = [
        {"domain": "example.com", "dns_status": "nxdomain"},
        {"domain": "example.com", "dns_status": "nxdomain"},
        {"domain": "example.com", "dns_status": "nxdomain"},
    ]
    (state / "network_observations.jsonl").write_text(
        "".join(json.dumps(row) + "\n" for row in rows),
        encoding="utf-8",
    )

    payload = build_network_memory(tmp_path)

    assert payload["schema"] == "subreparo.network_memory.v1"
    assert payload["new_domains"] == ["example.com"]
    assert payload["repeated_beaconing_candidates"][0]["count"] == 3
    assert payload["dns_anomalies"][0]["status"] == "nxdomain"


def test_network_memory_cli_runs_json(tmp_path: Path, capsys) -> None:
    exit_code = network_memory_main([str(tmp_path), "--json"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "subreparo.network_memory.v1" in captured.out

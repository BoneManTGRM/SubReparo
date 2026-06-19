from pathlib import Path

from subreparo_immune.agent_core import read_scar_memory, run_agent_cycle
from subreparo_immune.agent_proofs import build_agent_proof_export, write_agent_proof_export
from subreparo_immune.clawdbot_backend import handle_clawdbot_goal


def test_agent_cycle_records_memory(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    payload = run_agent_cycle(tmp_path, goal="self-heal project")
    assert payload["schema"] == "subreparo.immune_agent_cycle.v1"
    assert payload["cycle"]["proof_digest"]
    assert (tmp_path / ".subreparo" / "agent_cycles.jsonl").exists()
    assert (tmp_path / ".subreparo" / "agent_scars.jsonl").exists()


def test_scar_memory_shape(tmp_path: Path) -> None:
    memory = read_scar_memory(tmp_path)
    assert memory["schema"] == "subreparo.agent_scars.v1"
    assert memory["repair_ledger_tail"] == []


def test_agent_proof_export_after_cycle(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    run_agent_cycle(tmp_path, goal="self-heal project")
    proof = build_agent_proof_export(tmp_path)
    assert proof["ready"] is True
    assert proof["cycle_digest"]
    path = write_agent_proof_export(tmp_path)
    assert path.exists()


def test_bot_backend_payload(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    payload = handle_clawdbot_goal(tmp_path, "run quality checks")
    assert payload["schema"] == "subreparo.clawdbot_backend.v1"
    assert payload["proof_export"]["ready"] is True
    assert payload["safety_boundary"]["high_impact_actions_execute"] is False

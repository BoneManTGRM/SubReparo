from __future__ import annotations

from pathlib import Path
from typing import Any

from .agent_core import run_agent_cycle
from .agent_proofs import build_agent_proof_export, write_agent_proof_export
from .swarm_orchestrator import orchestrate_swarm


def handle_clawdbot_goal(root: Path, goal: str, write_proof: bool = True) -> dict[str, Any]:
    """Return a backend payload a bot/frontend can display.

    This adapter intentionally does not send messages or execute high-impact actions.
    A Clawdbot-style interface can call it to get SubReparo's self-healing plan,
    cycle result, proof payload, and approval state.
    """
    root = root.resolve()
    orchestration = orchestrate_swarm(root, goal)
    agent_cycle = run_agent_cycle(root, goal=goal, apply_safe_repairs=False)
    proof_path = str(write_agent_proof_export(root)) if write_proof else None
    return {
        "schema": "subreparo.clawdbot_backend.v1",
        "goal": goal,
        "orchestration": orchestration,
        "agent_cycle": agent_cycle,
        "proof_export": build_agent_proof_export(root),
        "proof_path": proof_path,
        "safety_boundary": {
            "high_impact_actions_execute": False,
            "approval_required_for_repair": True,
            "official_connectors_only": True,
        },
    }

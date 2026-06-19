from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .agent_core import AGENT_CYCLES_PATH, stable_digest

PROOF_EXPORT_PATH = Path(".subreparo") / "agent_proof_export.json"


def latest_agent_cycle(root: Path) -> dict[str, Any] | None:
    path = root.resolve() / AGENT_CYCLES_PATH
    if not path.exists():
        return None
    lines = [line for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()]
    if not lines:
        return None
    return json.loads(lines[-1])


def build_agent_proof_export(root: Path) -> dict[str, Any]:
    root = root.resolve()
    latest = latest_agent_cycle(root)
    if latest is None:
        return {
            "schema": "subreparo.agent_proof_export.v1",
            "ready": False,
            "reason": "No agent cycle found.",
        }
    proof_payload = {
        "schema": "subreparo.agent_proof_export.v1",
        "ready": True,
        "cycle_digest": latest.get("proof_digest"),
        "goal": latest.get("goal"),
        "phase": latest.get("phase"),
        "highest_severity": latest.get("highest_severity"),
        "finding_count": latest.get("finding_count"),
        "verified": latest.get("verified"),
    }
    proof_payload["export_digest"] = stable_digest(proof_payload)
    proof_payload["chain_target"] = {
        "pallet": "pallet-reparodynamics",
        "call": "submit_agent_proof",
        "status": "prototype_payload_only",
    }
    return proof_payload


def write_agent_proof_export(root: Path) -> Path:
    root = root.resolve()
    target = root / PROOF_EXPORT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(build_agent_proof_export(root), indent=2, sort_keys=True), encoding="utf-8")
    return target

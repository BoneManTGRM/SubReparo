from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

FLEET_SCHEMA = "subreparo.fleet_dashboard.v1"
FLEET_DASHBOARD = Path(".subreparo") / "fleet_dashboard.json"


def _count_lines(path: Path) -> int:
    if not path.exists():
        return 0
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return sum(1 for line in lines if line.strip())


def _json_file_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"present": False}
    try:
        payload = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        return {"present": True, "readable": False}
    keys = sorted(payload.keys()) if isinstance(payload, dict) else []
    return {"present": True, "readable": True, "keys": keys}


def _node_id(root: Path) -> str:
    digest = hashlib.sha256(str(root.resolve()).encode("utf-8")).hexdigest()
    return digest[:16]


def build_fleet_node(root: Path) -> dict[str, Any]:
    root = root.resolve()
    state = root / ".subreparo"
    return {
        "node_id": _node_id(root),
        "name": root.name or "local-root",
        "state_present": state.exists(),
        "counts": {
            "alerts": _count_lines(state / "watch_alerts.jsonl"),
            "native_alerts": _count_lines(state / "native_alerts.jsonl"),
            "approvals": _count_lines(state / "approval_queue.jsonl"),
            "outcomes": _count_lines(state / "outcome_records.jsonl"),
            "agent_cycles": _count_lines(state / "agent_cycles.jsonl"),
        },
        "reports": {
            "quality": _json_file_state(state / "quality_report.json"),
            "trust": _json_file_state(state / "trust_report.json"),
            "signature": _json_file_state(state / "report_signature.json"),
        },
    }


def build_fleet_dashboard(root: Path, nodes: list[Path] | None = None) -> dict[str, Any]:
    root = root.resolve()
    selected = nodes or [root]
    fleet_nodes = [build_fleet_node(node) for node in selected]
    totals = {
        "nodes": len(fleet_nodes),
        "alerts": sum(int(node["counts"]["alerts"]) for node in fleet_nodes),
        "approvals": sum(int(node["counts"]["approvals"]) for node in fleet_nodes),
    }
    return {
        "schema": FLEET_SCHEMA,
        "mode": "local_manifest",
        "totals": totals,
        "nodes": fleet_nodes,
        "safety": {
            "local_only": True,
            "raw_file_content_collected": False,
            "remote_listener_started": False,
        },
    }


def write_fleet_dashboard(root: Path, nodes: list[Path] | None = None) -> Path:
    root = root.resolve()
    path = root / FLEET_DASHBOARD
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_fleet_dashboard(root, nodes=nodes)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return path

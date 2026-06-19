from __future__ import annotations

import hashlib
import json
import platform
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .audit import last_hash
from .rules import rule_catalog
from .trends import risk_trends

STATE_DIR = Path(".subreparo")
NODE_PATH = STATE_DIR / "aegis_node.json"
MESH_EXPORT_PATH = STATE_DIR / "aegis_mesh_export.json"


@dataclass(frozen=True)
class AegisNode:
    node_id: str
    created_at: str
    product: str
    node_type: str
    os_name: str
    os_release: str
    privacy_mode: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_node_id() -> str:
    return hashlib.sha256(str(uuid.uuid4()).encode("utf-8")).hexdigest()


def init_node(root: Path, node_type: str = "aegis-node", privacy_mode: str = "local-first") -> AegisNode:
    path = root.resolve() / NODE_PATH
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        return AegisNode(**data)
    node = AegisNode(
        node_id=new_node_id(),
        created_at=now(),
        product="Aegis Mesh",
        node_type=node_type,
        os_name=platform.system(),
        os_release=platform.release(),
        privacy_mode=privacy_mode,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(node.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return node


def load_node(root: Path) -> AegisNode:
    path = root.resolve() / NODE_PATH
    if not path.exists():
        return init_node(root)
    return AegisNode(**json.loads(path.read_text(encoding="utf-8")))


def mesh_export(root: Path) -> dict[str, Any]:
    root = root.resolve()
    node = load_node(root)
    payload = {
        "product": "Aegis Mesh",
        "generated_at": now(),
        "node": node.to_dict(),
        "audit_tip": last_hash(root / STATE_DIR / "audit.jsonl"),
        "risk_trends": risk_trends(root),
        "rule_catalog": rule_catalog(),
        "privacy_boundary": "digest-and-summary-only; no raw files by default",
    }
    out = root / MESH_EXPORT_PATH
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return payload

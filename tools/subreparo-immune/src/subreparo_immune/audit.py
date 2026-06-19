from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

AUDIT_PATH = Path(".subreparo") / "audit.jsonl"


@dataclass(frozen=True)
class AuditRecord:
    created_at: str
    event: str
    payload: dict[str, Any]
    previous_hash: str
    record_hash: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(data: dict[str, Any]) -> str:
    encoded = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def last_hash(path: Path = AUDIT_PATH) -> str:
    if not path.exists():
        return "0" * 64
    lines = [line for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()]
    if not lines:
        return "0" * 64
    try:
        return json.loads(lines[-1]).get("record_hash", "0" * 64)
    except json.JSONDecodeError:
        return "0" * 64


def append_audit(event: str, payload: dict[str, Any], path: Path = AUDIT_PATH) -> AuditRecord:
    path.parent.mkdir(parents=True, exist_ok=True)
    previous = last_hash(path)
    base = {
        "created_at": now(),
        "event": event,
        "payload": payload,
        "previous_hash": previous,
    }
    record = AuditRecord(record_hash=digest(base), **base)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record.to_dict(), sort_keys=True) + "\n")
    return record


def verify_audit(path: Path = AUDIT_PATH) -> bool:
    previous = "0" * 64
    if not path.exists():
        return True
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        data = json.loads(line)
        expected_base = {
            "created_at": data["created_at"],
            "event": data["event"],
            "payload": data["payload"],
            "previous_hash": previous,
        }
        if data.get("previous_hash") != previous:
            return False
        if data.get("record_hash") != digest(expected_base):
            return False
        previous = data["record_hash"]
    return True

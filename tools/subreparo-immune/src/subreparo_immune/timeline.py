from __future__ import annotations

import json
from pathlib import Path
from typing import Any

EVENT_FILES = {
    "repair_ledger.jsonl": "finding",
    "quarantine_manifest.jsonl": "quarantine",
    "watch_alerts.jsonl": "alert",
    "audit.jsonl": "audit",
}


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"created_at": "", "raw": line})
    return rows


def build_timeline(root: Path) -> list[dict[str, Any]]:
    state = root.resolve() / ".subreparo"
    events: list[dict[str, Any]] = []
    for filename, event_type in EVENT_FILES.items():
        for row in _read_jsonl(state / filename):
            created_at = row.get("created_at") or row.get("generated_at") or ""
            events.append({"created_at": created_at, "event_type": event_type, "source": filename, "data": row})
    return sorted(events, key=lambda item: item.get("created_at", ""))

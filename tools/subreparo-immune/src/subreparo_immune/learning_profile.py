from __future__ import annotations

import hashlib
import json
import platform
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .feedback import load_feedback

LEARNING_PROFILE_PATH = Path(".subreparo") / "learning_profile.json"
SCHEMA = "subreparo.learning_profile.v1"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def device_fingerprint() -> str:
    raw = "|".join([
        platform.system(),
        platform.release(),
        platform.machine(),
        platform.python_version(),
    ])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


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
            rows.append({"unreadable": line})
    return rows


def _pattern_key(record: dict[str, Any]) -> str | None:
    finding = record.get("finding")
    if not isinstance(finding, dict):
        return None
    finding_type = finding.get("type")
    message = finding.get("message")
    severity = finding.get("severity")
    if not finding_type or not message:
        return None
    return f"{severity}|{finding_type}|{message}"


def build_learning_profile(root: Path) -> dict[str, Any]:
    root = root.resolve()
    state = root / ".subreparo"
    ledger = _read_jsonl(state / "repair_ledger.jsonl")
    feedback = load_feedback(state / "feedback.json")
    pattern_counts = Counter(key for key in (_pattern_key(row) for row in ledger) if key)
    repeated_patterns = [
        {"pattern": pattern, "count": count, "priority": "high" if count >= 3 else "watch"}
        for pattern, count in pattern_counts.most_common()
        if count >= 2
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": now(),
        "device_profile": {
            "fingerprint": device_fingerprint(),
            "system": platform.system(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
        "normal_profile": {
            "ledger_records": len(ledger),
            "feedback_records": len(feedback.false_positives),
            "state_files_present": sorted(path.name for path in state.glob("*")) if state.exists() else [],
        },
        "repeated_patterns": repeated_patterns,
        "feedback_learning": [record.to_dict() for record in feedback.false_positives],
        "faster_scoring_hints": {
            "repeated_patterns_available": bool(repeated_patterns),
            "false_positive_targets": [record.target for record in feedback.false_positives],
        },
    }
    output = root / LEARNING_PROFILE_PATH
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return payload

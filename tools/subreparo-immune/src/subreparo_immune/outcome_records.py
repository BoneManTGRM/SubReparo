from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OUTCOME_PATH = Path(".subreparo") / "outcome_records.jsonl"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class OutcomeRecord:
    created_at: str
    title: str
    status: str
    summary: str
    evidence: list[str]
    verification: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def append_outcome(
    title: str,
    status: str,
    summary: str,
    evidence: list[str] | None = None,
    verification: list[str] | None = None,
    path: Path = OUTCOME_PATH,
) -> OutcomeRecord:
    record = OutcomeRecord(
        created_at=now(),
        title=title,
        status=status,
        summary=summary,
        evidence=evidence or [],
        verification=verification or [],
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record.to_dict(), sort_keys=True) + "\n")
    return record


def list_outcomes(path: Path = OUTCOME_PATH) -> list[OutcomeRecord]:
    if not path.exists():
        return []
    records: list[OutcomeRecord] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip():
            records.append(OutcomeRecord(**json.loads(line)))
    return records

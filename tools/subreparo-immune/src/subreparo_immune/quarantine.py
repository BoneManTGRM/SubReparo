from __future__ import annotations

import json
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class QuarantineRecord:
    original_path: str
    staged_path: str
    created_at: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_relative(root: Path, path: Path) -> Path:
    root = root.resolve()
    path = path.resolve()
    try:
        return path.relative_to(root)
    except ValueError as exc:
        raise ValueError("Refusing to stage a file outside the selected root.") from exc


def stage_file(root: Path, target: Path, reason: str, state_dir: Path | None = None) -> QuarantineRecord:
    root = root.resolve()
    relative = safe_relative(root, target)
    if not target.exists() or not target.is_file():
        raise FileNotFoundError(str(target))

    state = state_dir or root / ".subreparo"
    quarantine_dir = state / "quarantine"
    manifest_path = state / "quarantine_manifest.jsonl"
    staged_path = quarantine_dir / relative
    staged_path.parent.mkdir(parents=True, exist_ok=True)

    counter = 1
    final_path = staged_path
    while final_path.exists():
        final_path = staged_path.with_name(f"{staged_path.name}.{counter}")
        counter += 1

    shutil.move(str(target), str(final_path))
    record = QuarantineRecord(
        original_path=str(target),
        staged_path=str(final_path),
        created_at=now(),
        reason=reason,
    )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record.to_dict(), sort_keys=True) + "\n")
    return record


def list_records(state_dir: Path) -> list[QuarantineRecord]:
    manifest_path = state_dir / "quarantine_manifest.jsonl"
    if not manifest_path.exists():
        return []
    records: list[QuarantineRecord] = []
    for line in manifest_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip():
            records.append(QuarantineRecord(**json.loads(line)))
    return records

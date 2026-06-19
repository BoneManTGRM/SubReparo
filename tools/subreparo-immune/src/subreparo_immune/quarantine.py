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


def _rewrite_manifest(state_dir: Path, records: list[QuarantineRecord]) -> None:
    manifest_path = state_dir / "quarantine_manifest.jsonl"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        "".join(json.dumps(record.to_dict(), sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


def restore_record(root: Path, index: int, state_dir: Path | None = None) -> QuarantineRecord:
    root = root.resolve()
    state = (state_dir or root / ".subreparo").resolve()
    records = list_records(state)
    if index < 0 or index >= len(records):
        raise IndexError("Quarantine index out of range.")

    record = records[index]
    staged = Path(record.staged_path).resolve()
    original = Path(record.original_path).resolve()

    try:
        staged.relative_to(state)
    except ValueError as exc:
        raise ValueError("Refusing to restore a staged file outside SubReparo state.") from exc

    try:
        original.relative_to(root)
    except ValueError as exc:
        raise ValueError("Refusing to restore outside the selected root.") from exc

    if not staged.exists() or not staged.is_file():
        raise FileNotFoundError(str(staged))
    if original.exists():
        raise FileExistsError(f"Restore target already exists: {original}")

    original.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(staged), str(original))
    _rewrite_manifest(state, [item for idx, item in enumerate(records) if idx != index])
    return record


def restore_all(root: Path, state_dir: Path | None = None) -> list[QuarantineRecord]:
    restored: list[QuarantineRecord] = []
    state = state_dir or root.resolve() / ".subreparo"
    while list_records(state):
        try:
            restored.append(restore_record(root, 0, state_dir=state))
        except (FileExistsError, FileNotFoundError, ValueError):
            break
    return restored


def remove_staged_record(root: Path, index: int, state_dir: Path | None = None) -> QuarantineRecord:
    root = root.resolve()
    state = (state_dir or root / ".subreparo").resolve()
    records = list_records(state)
    if index < 0 or index >= len(records):
        raise IndexError("Quarantine index out of range.")
    record = records[index]
    staged = Path(record.staged_path).resolve()
    try:
        staged.relative_to(state)
    except ValueError as exc:
        raise ValueError("Refusing to remove a staged file outside SubReparo state.") from exc
    if staged.exists() and staged.is_file():
        staged.unlink()
    _rewrite_manifest(state, [item for idx, item in enumerate(records) if idx != index])
    return record

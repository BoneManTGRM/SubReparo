from __future__ import annotations

import json
import tarfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SNAPSHOT_DIR = Path(".subreparo") / "snapshots"
SKIP_DIRS = {".git", ".subreparo", "node_modules", "target", "dist", "build", "__pycache__", ".venv", "venv"}


def now_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


@dataclass(frozen=True)
class SnapshotRecord:
    created_at: str
    archive_path: str
    file_count: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def create_snapshot(root: Path, output_dir: Path | None = None) -> SnapshotRecord:
    root = root.resolve()
    target_dir = output_dir or root / SNAPSHOT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    archive = target_dir / f"snapshot-{now_slug()}.tar.gz"
    file_count = 0
    with tarfile.open(archive, "w:gz") as tar:
        for path in root.rglob("*"):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if path.is_file():
                tar.add(path, arcname=str(path.relative_to(root)))
                file_count += 1
    record = SnapshotRecord(created_at=datetime.now(timezone.utc).isoformat(), archive_path=str(archive), file_count=file_count)
    manifest = target_dir / "snapshot_manifest.jsonl"
    with manifest.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record.to_dict(), sort_keys=True) + "\n")
    return record

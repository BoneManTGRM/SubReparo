from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HASH_LOOKUP_PATH = Path(".subreparo") / "hash_lookup.json"
SCHEMA = "subreparo.hash_lookup.v1"
DEFAULT_SUFFIXES = {
    ".exe", ".scr", ".com", ".dll", ".so", ".dylib", ".ps1", ".bat", ".cmd", ".vbs", ".js", ".sh", ".py",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_hash_lookup(root: Path, suffixes: set[str] | None = None) -> dict[str, Any]:
    root = root.resolve()
    selected_suffixes = suffixes or DEFAULT_SUFFIXES
    rows: list[dict[str, Any]] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if ".subreparo" in path.parts:
            continue
        if path.suffix.lower() not in selected_suffixes:
            continue
        digest = sha256_file(path)
        if digest:
            rows.append({
                "relative_path": str(path.relative_to(root)),
                "sha256": digest,
                "size_bytes": path.stat().st_size,
            })
    payload = {
        "schema": SCHEMA,
        "generated_at": now(),
        "project_root": str(root),
        "hash_only": True,
        "raw_file_content_included": False,
        "records": rows,
    }
    output = root / HASH_LOOKUP_PATH
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return payload

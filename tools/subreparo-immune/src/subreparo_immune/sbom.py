from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .inventory import dependency_inventory


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 128), b""):
            digest.update(chunk)
    return digest.hexdigest()


def generate_sbom(root: Path) -> dict[str, Any]:
    root = root.resolve()
    inventory = dependency_inventory(root)
    components: list[dict[str, Any]] = []
    for manifest in inventory["manifests"]:
        path = root / manifest["path"]
        if path.exists() and path.is_file():
            components.append({
                "type": "manifest",
                "name": path.name,
                "path": manifest["path"],
                "ecosystem": manifest["ecosystem"],
                "sha256": _hash_file(path),
            })
    return {
        "schema": "subreparo.sbom.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "component_count": len(components),
        "components": components,
    }


def write_sbom(root: Path, output: Path | None = None) -> Path:
    root = root.resolve()
    target = output or root / ".subreparo" / "sbom.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(generate_sbom(root), indent=2, sort_keys=True), encoding="utf-8")
    return target

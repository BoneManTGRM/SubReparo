from __future__ import annotations

from pathlib import Path
from typing import Any

MANIFESTS = {
    "package.json": "node",
    "package-lock.json": "node-lock",
    "requirements.txt": "python-pip",
    "pyproject.toml": "python-project",
    "Pipfile": "python-pipenv",
    "poetry.lock": "python-poetry-lock",
    "Cargo.toml": "rust-cargo",
    "Cargo.lock": "rust-cargo-lock",
    "go.mod": "go-module",
    "go.sum": "go-sum",
    "pom.xml": "java-maven",
    "build.gradle": "java-gradle",
}

SKIP_DIRS = {".git", ".subreparo", "node_modules", "target", "dist", "build", "__pycache__", ".venv", "venv"}


def dependency_inventory(root: Path) -> dict[str, Any]:
    root = root.resolve()
    manifests: list[dict[str, str]] = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.name in MANIFESTS:
            manifests.append({
                "path": str(path.relative_to(root)),
                "ecosystem": MANIFESTS[path.name],
            })
    return {"manifest_count": len(manifests), "manifests": sorted(manifests, key=lambda item: item["path"])}

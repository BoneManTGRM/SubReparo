from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import Finding, FindingType, Severity

SKIP_DIRS = {".git", ".subreparo", "node_modules", "target", "dist", "build", "__pycache__", ".venv", "venv"}
WATCH_SUFFIXES = {".exe", ".dll", ".scr", ".com", ".so", ".dylib", ".jar", ".apk", ".bin", ".ps1", ".bat", ".cmd", ".vbs", ".js", ".sh", ".py"}


@dataclass(frozen=True)
class FileState:
    path: str
    size: int
    sha256: str
    suffix: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def iter_files(root: Path):
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 128), b""):
            digest.update(chunk)
    return digest.hexdigest()


def snapshot(root: Path) -> dict[str, FileState]:
    root = root.resolve()
    states: dict[str, FileState] = {}
    for path in iter_files(root):
        try:
            relative = str(path.relative_to(root))
            states[relative] = FileState(
                path=relative,
                size=path.stat().st_size,
                sha256=hash_file(path),
                suffix=path.suffix.lower(),
            )
        except OSError:
            continue
    return states


def write_baseline(root: Path, path: Path | None = None) -> Path:
    root = root.resolve()
    target = path or root / ".subreparo" / "baseline.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "generated_at": now(),
        "root": str(root),
        "files": [state.to_dict() for state in snapshot(root).values()],
    }
    target.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return target


def read_baseline(path: Path) -> dict[str, FileState]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {item["path"]: FileState(**item) for item in payload.get("files", [])}


def compare(root: Path, path: Path | None = None) -> list[Finding]:
    root = root.resolve()
    baseline_path = path or root / ".subreparo" / "baseline.json"
    old = read_baseline(baseline_path)
    current = snapshot(root)
    findings: list[Finding] = []

    if not old:
        findings.append(Finding(
            type=FindingType.IMMUNE_PATROL,
            severity=Severity.INFO,
            target=str(baseline_path),
            message="baseline not found",
            recommendation="Create a baseline after a clean sweep so SubReparo can detect unexpected changes.",
        ))
        return findings

    for relative, state in current.items():
        previous = old.get(relative)
        watched = state.suffix in WATCH_SUFFIXES
        if previous is None and watched:
            findings.append(Finding(
                type=FindingType.IMMUNE_PATROL,
                severity=Severity.HIGH,
                target=relative,
                message="new watched file appeared after baseline",
                recommendation="Review the new file, verify its origin, and isolate it if it is unexpected.",
                detail=f"sha256={state.sha256}; size={state.size}",
            ))
        elif previous is not None and previous.sha256 != state.sha256 and watched:
            findings.append(Finding(
                type=FindingType.IMMUNE_PATROL,
                severity=Severity.HIGH,
                target=relative,
                message="watched file changed after baseline",
                recommendation="Review the changed file and confirm the change was expected.",
                detail=f"old={previous.sha256}; new={state.sha256}; size={state.size}",
            ))

    for relative, previous in old.items():
        if relative not in current and previous.suffix in WATCH_SUFFIXES:
            findings.append(Finding(
                type=FindingType.IMMUNE_PATROL,
                severity=Severity.MEDIUM,
                target=relative,
                message="watched file missing after baseline",
                recommendation="Confirm this removal was expected and not part of suspicious activity.",
            ))

    return findings

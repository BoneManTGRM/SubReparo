from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .inventory import dependency_inventory
from .models import Finding, FindingType, Severity

UNPINNED_PIP = re.compile(r"^[A-Za-z0-9_.-]+\s*$")
RISKY_PACKAGE_SCRIPT_KEYS = {"preinstall", "install", "postinstall", "prepare"}


def scan_dependency_risk(root: Path) -> list[Finding]:
    root = root.resolve()
    findings: list[Finding] = []
    inventory = dependency_inventory(root)
    for manifest in inventory["manifests"]:
        path = root / manifest["path"]
        if path.name == "requirements.txt":
            findings.extend(_scan_requirements(root, path))
        elif path.name == "package.json":
            findings.extend(_scan_package_json(root, path))
    return findings


def _scan_requirements(root: Path, path: Path) -> list[Finding]:
    findings: list[Finding] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if UNPINNED_PIP.match(line):
            findings.append(Finding(
                type=FindingType.DEPENDENCY_REVIEW,
                severity=Severity.MEDIUM,
                target=f"{path.relative_to(root)}:{line_no}",
                message="dependency is not pinned",
                recommendation="Pin dependency versions for reproducible installs and safer review.",
                detail=line,
            ))
    return findings


def _scan_package_json(root: Path, path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        findings.append(Finding(
            type=FindingType.DEPENDENCY_REVIEW,
            severity=Severity.MEDIUM,
            target=str(path.relative_to(root)),
            message="package manifest could not be parsed",
            recommendation="Review package.json manually before installing dependencies.",
        ))
        return findings
    scripts = data.get("scripts", {}) if isinstance(data.get("scripts"), dict) else {}
    for key in sorted(RISKY_PACKAGE_SCRIPT_KEYS & set(scripts)):
        findings.append(Finding(
            type=FindingType.DEPENDENCY_REVIEW,
            severity=Severity.MEDIUM,
            target=f"{path.relative_to(root)}:scripts.{key}",
            message="package install lifecycle script present",
            recommendation="Review install lifecycle scripts before running package installation.",
            detail=str(scripts[key])[:240],
        ))
    return findings

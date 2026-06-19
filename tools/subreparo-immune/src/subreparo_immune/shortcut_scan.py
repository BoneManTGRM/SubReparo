from __future__ import annotations

import re
from pathlib import Path

from .models import Finding, FindingType, Severity

LAUNCHER_SUFFIXES = {".url", ".desktop", ".lnk"}
RISKY_TEXT = re.compile(r"(?i)(powershell|pwsh|cmd\.exe|wscript|cscript|curl|wget|http://|https://|appdata|temp|downloads)")


def scan_shortcuts(root: Path) -> list[Finding]:
    root = root.resolve()
    findings: list[Finding] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in LAUNCHER_SUFFIXES:
            continue
        if path.suffix.lower() == ".lnk":
            findings.append(Finding(
                type=FindingType.IMMUNE_PATROL,
                severity=Severity.LOW,
                target=str(path.relative_to(root)),
                message="shortcut file present",
                recommendation="Confirm this shortcut points to a trusted local application.",
            ))
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if RISKY_TEXT.search(text):
            findings.append(Finding(
                type=FindingType.IMMUNE_PATROL,
                severity=Severity.MEDIUM,
                target=str(path.relative_to(root)),
                message="launcher contains suspicious command or remote target",
                recommendation="Review the launcher destination before opening it.",
                detail=text[:240],
            ))
    return findings

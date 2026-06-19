from __future__ import annotations

import platform
import re
import subprocess
from pathlib import Path

from .models import Finding, FindingType, Severity

RUN_KEY_NAMES = (
    r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run",
    r"HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce",
    r"HKLM\Software\Microsoft\Windows\CurrentVersion\Run",
    r"HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce",
)
RISKY_REGISTRY_TEXT = re.compile(
    r"(?i)(powershell|pwsh|cmd\.exe|wscript|cscript|mshta|rundll32|regsvr32|curl|wget|http://|https://|appdata|temp|tmp|downloads|public)",
)
SCRIPT_OR_BINARY = re.compile(r"(?i)\.(exe|scr|com|bat|cmd|ps1|vbs|jse|js|dll)(?:\s|$|\")")


def _run_reg_query(key: str) -> str:
    try:
        completed = subprocess.run(
            ["reg", "query", key],
            check=False,
            capture_output=True,
            text=True,
            timeout=8,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return completed.stdout or ""


def registry_fixture_files(root: Path | None = None) -> list[Path]:
    if root is None:
        return []
    candidates = [root / "registry", root / "registry_run", root / "RunKeys"]
    files: list[Path] = []
    for candidate in candidates:
        if candidate.is_file():
            files.append(candidate)
        elif candidate.is_dir():
            files.extend(path for path in candidate.rglob("*") if path.is_file())
    return files


def registry_run_entries(root: Path | None = None) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for file in registry_fixture_files(root):
        try:
            rows.append((str(file), file.read_text(encoding="utf-8", errors="ignore")[:12000]))
        except OSError:
            continue
    if platform.system().lower() == "windows":
        for key in RUN_KEY_NAMES:
            output = _run_reg_query(key)
            if output.strip():
                rows.append((key, output[:12000]))
    return rows


def scan_registry_startup(root: Path | None = None) -> list[Finding]:
    findings: list[Finding] = []
    for source, text in registry_run_entries(root):
        if not text.strip():
            continue
        if RISKY_REGISTRY_TEXT.search(text) or SCRIPT_OR_BINARY.search(text):
            severity = Severity.HIGH if RISKY_REGISTRY_TEXT.search(text) else Severity.MEDIUM
            findings.append(Finding(
                type=FindingType.IMMUNE_PATROL,
                severity=severity,
                target=source,
                message="registry startup entry contains risky command or launch target",
                recommendation="Confirm this startup entry is expected. Disable it only after preserving evidence.",
                detail=text[:500],
            ))
    return findings

from __future__ import annotations

import os
import platform
import re
from pathlib import Path

from .models import Finding, FindingType, Severity

TASK_SUFFIXES = {".xml", ".job", ".task", ".service", ".timer", ".plist", ".cron", ".txt", ""}
RISKY_TASK_TEXT = re.compile(
    r"(?i)(powershell\s+-enc|frombase64string|curl\s+|wget\s+|http://|https://|/dev/tcp|"
    r"bash\s+-c|sh\s+-c|chmod\s+\+x|appdata|temp|tmp|downloads|public)",
)
NETWORK_TASK_TEXT = re.compile(r"(?i)(http://|https://|curl\s+|wget\s+|/dev/tcp)")


def candidate_task_locations(root: Path | None = None) -> list[Path]:
    locations: list[Path] = []
    if root is not None:
        locations.extend([
            root / "scheduled_tasks",
            root / "Scheduled Tasks",
            root / "tasks",
            root / "cron.d",
            root / "crontab",
            root / "systemd",
            root / "LaunchAgents",
            root / "LaunchDaemons",
        ])

    system = platform.system().lower()
    home = Path.home()
    if system == "windows":
        system_root = os.environ.get("SystemRoot", r"C:\Windows")
        locations.append(Path(system_root) / "System32" / "Tasks")
    elif system == "darwin":
        locations.extend([
            home / "Library" / "LaunchAgents",
            Path("/Library/LaunchAgents"),
            Path("/Library/LaunchDaemons"),
        ])
    else:
        locations.extend([
            Path("/etc/crontab"),
            Path("/etc/cron.d"),
            Path("/etc/systemd/system"),
            home / ".config" / "systemd" / "user",
        ])
    return [location for location in locations if location.exists()]


def _iter_task_files(location: Path) -> list[Path]:
    if location.is_file():
        return [location]
    if not location.is_dir():
        return []
    return [path for path in location.rglob("*") if path.is_file()]


def scan_scheduled_tasks(root: Path | None = None) -> list[Finding]:
    findings: list[Finding] = []
    for location in candidate_task_locations(root):
        for path in _iter_task_files(location):
            if path.suffix.lower() not in TASK_SUFFIXES:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")[:12000]
            except OSError:
                continue
            if not text.strip():
                continue
            if RISKY_TASK_TEXT.search(text):
                severity = Severity.HIGH if NETWORK_TASK_TEXT.search(text) else Severity.MEDIUM
                findings.append(Finding(
                    type=FindingType.IMMUNE_PATROL,
                    severity=severity,
                    target=str(path),
                    message="scheduled task contains risky command or location",
                    recommendation="Confirm this task is expected. Disable or isolate it if the origin is unknown.",
                    detail=text[:500],
                ))
    return findings

from __future__ import annotations

import os
import platform
from pathlib import Path

from .models import Finding, FindingType, Severity

SUSPICIOUS_SUFFIXES = {".exe", ".scr", ".com", ".bat", ".cmd", ".ps1", ".vbs", ".js", ".jse", ".sh", ".py"}
STARTUP_KEYWORDS = {"appdata", "temp", "tmp", "downloads", "public", "programdata"}


def _home() -> Path:
    return Path.home()


def candidate_startup_locations(root: Path | None = None) -> list[Path]:
    home = _home()
    system = platform.system().lower()
    locations: list[Path] = []

    if root is not None:
        locations.extend([
            root / "startup",
            root / "Startup",
            root / "crontab",
            root / "systemd",
            root / "LaunchAgents",
            root / "LaunchDaemons",
        ])

    if system == "windows":
        appdata = os.environ.get("APPDATA")
        programdata = os.environ.get("PROGRAMDATA")
        if appdata:
            locations.append(Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup")
        if programdata:
            locations.append(Path(programdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup")
    elif system == "darwin":
        locations.extend([
            home / "Library" / "LaunchAgents",
            Path("/Library/LaunchAgents"),
            Path("/Library/LaunchDaemons"),
        ])
    else:
        locations.extend([
            home / ".config" / "autostart",
            home / ".config" / "systemd" / "user",
            home / ".local" / "share" / "systemd" / "user",
            Path("/etc/cron.d"),
            Path("/etc/systemd/system"),
        ])

    return [location for location in locations if location.exists()]


def scan_startup(root: Path | None = None) -> list[Finding]:
    findings: list[Finding] = []
    for location in candidate_startup_locations(root):
        for path in location.rglob("*"):
            if not path.is_file():
                continue
            suffix = path.suffix.lower()
            lower = str(path).lower()
            if suffix in SUSPICIOUS_SUFFIXES:
                findings.append(Finding(
                    type=FindingType.IMMUNE_PATROL,
                    severity=Severity.HIGH,
                    target=str(path),
                    message="startup entry points to a script or executable",
                    recommendation="Confirm this startup item is expected. If not, isolate it and review the source.",
                ))
            elif any(keyword in lower for keyword in STARTUP_KEYWORDS):
                findings.append(Finding(
                    type=FindingType.IMMUNE_PATROL,
                    severity=Severity.MEDIUM,
                    target=str(path),
                    message="startup entry lives in a commonly abused location",
                    recommendation="Review this startup item and confirm it belongs to a trusted application.",
                ))
    return findings

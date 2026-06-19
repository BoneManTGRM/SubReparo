from __future__ import annotations

import json
import platform
from pathlib import Path

from .models import Finding, FindingType, Severity

RISKY_PERMISSIONS = {
    "tabs",
    "webRequest",
    "webRequestBlocking",
    "cookies",
    "history",
    "downloads",
    "nativeMessaging",
    "proxy",
    "management",
    "debugger",
    "scripting",
    "clipboardRead",
}


def browser_roots(root: Path | None = None) -> list[Path]:
    roots: list[Path] = []
    if root is not None:
        roots.extend([root / "Extensions", root / "extensions", root / "browser_extensions"])

    home = Path.home()
    system = platform.system().lower()
    if system == "windows":
        roots.extend([
            home / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "Extensions",
            home / "AppData" / "Local" / "Microsoft" / "Edge" / "User Data" / "Default" / "Extensions",
        ])
    elif system == "darwin":
        roots.extend([
            home / "Library" / "Application Support" / "Google" / "Chrome" / "Default" / "Extensions",
            home / "Library" / "Application Support" / "Microsoft Edge" / "Default" / "Extensions",
        ])
    else:
        roots.extend([
            home / ".config" / "google-chrome" / "Default" / "Extensions",
            home / ".config" / "chromium" / "Default" / "Extensions",
            home / ".config" / "microsoft-edge" / "Default" / "Extensions",
        ])
    return [path for path in roots if path.exists()]


def scan_browser_extensions(root: Path | None = None) -> list[Finding]:
    findings: list[Finding] = []
    for base in browser_roots(root):
        for manifest in base.rglob("manifest.json"):
            try:
                data = json.loads(manifest.read_text(encoding="utf-8", errors="replace"))
            except (json.JSONDecodeError, OSError):
                findings.append(Finding(
                    type=FindingType.IMMUNE_PATROL,
                    severity=Severity.MEDIUM,
                    target=str(manifest),
                    message="browser extension manifest could not be parsed",
                    recommendation="Review this extension manually and remove it if it is unknown.",
                ))
                continue
            permissions = set(data.get("permissions", [])) | set(data.get("host_permissions", []))
            risky = sorted(permission for permission in permissions if permission in RISKY_PERMISSIONS or permission == "<all_urls>")
            if risky:
                findings.append(Finding(
                    type=FindingType.IMMUNE_PATROL,
                    severity=Severity.MEDIUM,
                    target=str(manifest),
                    message="browser extension requests sensitive permissions",
                    recommendation="Confirm this extension is trusted. Remove unknown extensions with broad permissions.",
                    detail=", ".join(risky[:12]),
                ))
    return findings

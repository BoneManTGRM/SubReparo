from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import __version__

INSTALLER_SCHEMA = "subreparo.installers.v1"
INSTALLER_MANIFEST = Path(".subreparo") / "installer_manifest.json"
VALID_PLATFORMS = ("windows", "macos", "linux")


def _platform_entry(name: str) -> dict[str, Any]:
    artifacts = {
        "windows": ["scripts/install-subreparo-immune.ps1", "packaging/windows/README.md"],
        "macos": ["scripts/install-subreparo-immune.sh", "packaging/macos/README.md"],
        "linux": ["scripts/install-subreparo-immune.sh", "packaging/linux/README.md"],
    }
    return {
        "platform": name,
        "status": "packaging_scaffold_ready",
        "artifacts": artifacts[name],
        "entrypoints": [
            "subreparo-immune",
            "subreparo-monitor",
            "subreparo-cortex",
            "subreparo-alerts",
            "subreparo-tray",
        ],
        "safety": {
            "local_install": True,
            "publish_step_included": False,
            "manual_review_before_release": True,
        },
    }


def build_installer_manifest(platforms: list[str] | None = None) -> dict[str, Any]:
    selected = list(platforms or VALID_PLATFORMS)
    unknown = [item for item in selected if item not in VALID_PLATFORMS]
    if unknown:
        raise ValueError(f"Unsupported platform(s): {', '.join(unknown)}")
    return {
        "schema": INSTALLER_SCHEMA,
        "version": __version__,
        "platform_count": len(selected),
        "platforms": [_platform_entry(name) for name in selected],
        "release_gate": {
            "tests_required": True,
            "manual_review_required": True,
            "signed_artifacts_required_before_public_release": True,
        },
    }


def write_installer_manifest(root: Path, platforms: list[str] | None = None) -> Path:
    root = root.resolve()
    path = root / INSTALLER_MANIFEST
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_installer_manifest(platforms), indent=2, sort_keys=True), encoding="utf-8")
    return path

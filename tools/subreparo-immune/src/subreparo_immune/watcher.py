from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from .setup_wizard import load_setup_profile

SCHEMA = "subreparo.watch_plan.v1"


def native_watchdog_available() -> bool:
    try:
        import watchdog.observers  # type: ignore[import-not-found]  # noqa: F401
    except ImportError:
        return False
    return True


def _existing_or_planned(path: Path) -> dict[str, Any]:
    return {
        "path": str(path.expanduser()),
        "exists": path.expanduser().exists(),
        "recursive": True,
        "events": ["created", "modified", "deleted", "moved"],
    }


def default_watch_targets(root: Path) -> list[dict[str, Any]]:
    root = root.resolve()
    home = Path.home()
    temp = Path(tempfile.gettempdir())
    targets = [
        {"kind": "project", **_existing_or_planned(root)},
        {"kind": "downloads", **_existing_or_planned(home / "Downloads")},
        {"kind": "desktop", **_existing_or_planned(home / "Desktop")},
        {"kind": "documents", **_existing_or_planned(home / "Documents")},
        {"kind": "temp", **_existing_or_planned(temp)},
        {"kind": "browser_downloads", **_existing_or_planned(home / "Downloads")},
    ]
    for candidate in (Path("/Volumes"), Path("/media"), Path("/mnt")):
        targets.append({"kind": "removable", **_existing_or_planned(candidate)})
    for archive_folder in (home / "Downloads", root):
        targets.append({
            "kind": "archive_extraction",
            **_existing_or_planned(archive_folder),
            "archive_suffixes": [".zip", ".tar", ".gz", ".tgz", ".7z", ".rar"],
        })
    targets.append({
        "kind": "process",
        "path": "process-table",
        "exists": True,
        "recursive": False,
        "events": ["new_process", "changed_command_line"],
    })
    return targets


def build_watch_plan(root: Path) -> dict[str, Any]:
    root = root.resolve()
    profile = load_setup_profile(root)
    if profile:
        profile_targets = [
            {"kind": "profile", **_existing_or_planned(Path(item).expanduser())}
            for item in profile.watched_paths
        ]
        targets = profile_targets + [item for item in default_watch_targets(root) if item["kind"] != "project"]
    else:
        targets = default_watch_targets(root)
    backend = "native_watchdog" if native_watchdog_available() else "polling_fallback"
    return {
        "schema": SCHEMA,
        "backend": backend,
        "native_available": backend == "native_watchdog",
        "targets": targets,
        "safety": {
            "local_only": True,
            "non_destructive": True,
            "alert_only_by_default": True,
        },
    }

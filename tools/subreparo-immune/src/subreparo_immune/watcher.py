from __future__ import annotations

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


def build_watch_plan(root: Path) -> dict[str, Any]:
    root = root.resolve()
    profile = load_setup_profile(root)
    watched_paths = profile.watched_paths if profile else (str(root),)
    backend = "native_watchdog" if native_watchdog_available() else "polling_fallback"
    targets = []
    for item in watched_paths:
        path = Path(item).expanduser()
        targets.append({
            "path": str(path),
            "exists": path.exists(),
            "recursive": True,
            "events": ["created", "modified", "deleted", "moved"],
        })
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

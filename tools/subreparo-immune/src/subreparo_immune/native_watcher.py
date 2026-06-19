from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .watcher import build_watch_plan, native_watchdog_available

WATCH_ALERTS_PATH = Path(".subreparo") / "watch_alerts.jsonl"
SCHEMA = "subreparo.native_watcher.v1"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class WatchAlert:
    event_type: str
    path: str
    source: str
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def append_watch_alert(root: Path, alert: WatchAlert) -> None:
    path = root.resolve() / WATCH_ALERTS_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(alert.to_dict(), sort_keys=True) + "\n")


def build_native_watcher_status(root: Path) -> dict[str, Any]:
    plan = build_watch_plan(root)
    return {
        "schema": SCHEMA,
        "native_available": native_watchdog_available(),
        "backend": plan["backend"],
        "target_count": len(plan.get("targets", [])),
        "alert_path": str(root.resolve() / WATCH_ALERTS_PATH),
        "local_only": True,
        "non_destructive": True,
    }


def make_alert(event_type: str, path: Path, source: str = "native_watcher") -> WatchAlert:
    return WatchAlert(
        event_type=event_type,
        path=str(path),
        source=source,
        created_at=now(),
    )


def start_native_observer(root: Path):
    if not native_watchdog_available():
        return None
    from watchdog.events import FileSystemEventHandler  # type: ignore[import-not-found]
    from watchdog.observers import Observer  # type: ignore[import-not-found]

    class SubReparoEventHandler(FileSystemEventHandler):
        def on_any_event(self, event):  # noqa: ANN001
            append_watch_alert(root, make_alert(str(event.event_type), Path(str(event.src_path))))

    observer = Observer()
    handler = SubReparoEventHandler()
    for target in build_watch_plan(root).get("targets", []):
        if not isinstance(target, dict) or target.get("kind") == "process":
            continue
        if not target.get("exists"):
            continue
        path = Path(str(target.get("path", ""))).expanduser()
        if path.exists() and path.is_dir():
            observer.schedule(handler, str(path), recursive=bool(target.get("recursive", True)))
    observer.start()
    return observer

from __future__ import annotations

import json
import platform
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

NOTIFICATION_LOG_PATH = Path(".subreparo") / "notifications.jsonl"
SCHEMA = "subreparo.notification.v1"


@dataclass(frozen=True)
class Notification:
    created_at: str
    level: str
    title: str
    message: str
    channel: str = "console_fallback"
    delivered: bool = False
    dry_run: bool = True

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["schema"] = SCHEMA
        return data


def native_channel() -> str:
    system = platform.system().lower()
    if system == "windows":
        return "windows_toast_planned"
    if system == "darwin":
        return "macos_notification_center_planned"
    if system == "linux":
        return "linux_desktop_notification_planned"
    return "console_fallback"


def create_notification(title: str, message: str, level: str = "info", dry_run: bool = True) -> Notification:
    return Notification(
        created_at=datetime.now(timezone.utc).isoformat(),
        level=level,
        title=title,
        message=message,
        channel=native_channel(),
        delivered=False,
        dry_run=dry_run,
    )


def write_notification(root: Path, notification: Notification) -> Path:
    path = root.resolve() / NOTIFICATION_LOG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(notification.to_dict(), sort_keys=True) + "\n")
    return path

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Notification:
    created_at: str
    level: str
    title: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def create_notification(title: str, message: str, level: str = "info") -> Notification:
    return Notification(
        created_at=datetime.now(timezone.utc).isoformat(),
        level=level,
        title=title,
        message=message,
    )


def write_notification(root: Path, notification: Notification) -> Path:
    state = root.resolve() / ".subreparo"
    state.mkdir(parents=True, exist_ok=True)
    path = state / "notifications.jsonl"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(str(notification.to_dict()) + "\n")
    return path

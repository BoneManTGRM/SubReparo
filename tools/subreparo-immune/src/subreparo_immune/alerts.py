from __future__ import annotations

import json
import platform
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ALERT_SCHEMA = "subreparo.native_alerts.v1"
ALERT_INBOX = Path(".subreparo") / "native_alerts.jsonl"
WATCH_ALERTS = Path(".subreparo") / "watch_alerts.jsonl"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class NativeAlertPlan:
    title: str
    message: str
    severity: str
    source: str
    target: str
    created_at: str
    delivery_mode: str = "local_preview"
    approval_required_for_native_emit: bool = True
    native_backend: str = "platform_notification"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def read_jsonl(path: Path, *, limit: int | None = None) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    lines = [line for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()]
    selected = lines[-limit:] if limit is not None else lines
    for line in selected:
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            value = {"unreadable": line}
        if isinstance(value, dict):
            rows.append(value)
        else:
            rows.append({"value": value})
    return rows


def native_backend_name() -> str:
    system = platform.system().lower()
    if system == "darwin":
        return "macos_user_notification"
    if system == "windows":
        return "windows_toast_notification"
    if system == "linux":
        return "linux_desktop_notification"
    return "console_notification"


def alert_from_event(event: dict[str, Any]) -> NativeAlertPlan:
    severity = str(event.get("severity") or "info")
    event_type = str(event.get("type") or event.get("event_type") or "local_alert")
    target = str(event.get("target") or event.get("path") or "local")
    message = str(event.get("message") or event.get("recommendation") or f"{event_type} observed at {target}")
    title = f"SubReparo {severity.upper()} alert"
    return NativeAlertPlan(
        title=title,
        message=message,
        severity=severity,
        source=event_type,
        target=target,
        created_at=str(event.get("created_at") or event.get("observed_at") or utc_now()),
        native_backend=native_backend_name(),
    )


def build_native_alert_report(root: Path, *, limit: int = 10) -> dict[str, Any]:
    root = root.resolve()
    watch_events = read_jsonl(root / WATCH_ALERTS, limit=limit)
    plans = [alert_from_event(event).to_dict() for event in watch_events]
    inbox = read_jsonl(root / ALERT_INBOX, limit=limit)
    return {
        "schema": ALERT_SCHEMA,
        "platform": platform.system() or "unknown",
        "native_emit_default": "disabled",
        "safety": {
            "local_only": True,
            "native_emit_is_preview_only": True,
            "requires_operator_approval_for_native_emit": True,
        },
        "pending_plan_count": len(plans),
        "inbox_count": len(inbox),
        "plans": plans,
        "recent_inbox": inbox,
    }


def append_alert_inbox(root: Path, plans: list[dict[str, Any]]) -> Path:
    root = root.resolve()
    path = root / ALERT_INBOX
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for plan in plans:
            record = dict(plan)
            record["recorded_at"] = utc_now()
            record["status"] = "queued_local_only"
            handle.write(json.dumps(record, sort_keys=True) + "\n")
    return path

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

from .alerts import ALERT_INBOX, read_jsonl

TRAY_SCHEMA = "subreparo.desktop_tray.v1"
TRAY_MANIFEST = Path(".subreparo") / "tray_manifest.json"

MENU_ITEMS = [
    {"id": "open_dashboard", "label": "Open Control Center"},
    {"id": "doctor", "label": "Run Doctor"},
    {"id": "monitor_once", "label": "Monitor Once"},
    {"id": "alerts", "label": "Review Alerts"},
    {"id": "approvals", "label": "Review Approvals"},
]


def optional_tray_backend_available() -> bool:
    return importlib.util.find_spec("pystray") is not None


def build_tray_manifest(root: Path, *, dashboard_url: str = "http://127.0.0.1:8765") -> dict[str, Any]:
    root = root.resolve()
    alert_count = len(read_jsonl(root / ALERT_INBOX))
    return {
        "schema": TRAY_SCHEMA,
        "dashboard_url": dashboard_url,
        "backend": {
            "mode": "headless_manifest",
            "optional_pystray_available": optional_tray_backend_available(),
            "starts_gui_by_default": False,
        },
        "status": {
            "alert_inbox_count": alert_count,
            "state_dir_present": (root / ".subreparo").exists(),
            "dashboard_localhost_only": True,
        },
        "menu_items": MENU_ITEMS,
        "safety": {
            "local_only": True,
            "passive_status_by_default": True,
            "high_impact_actions_route_to_approval_queue": True,
        },
    }


def write_tray_manifest(root: Path, *, dashboard_url: str = "http://127.0.0.1:8765") -> Path:
    root = root.resolve()
    path = root / TRAY_MANIFEST
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_tray_manifest(root, dashboard_url=dashboard_url)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path

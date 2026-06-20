from __future__ import annotations

import secrets
import socket
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class MobilePreviewPlan:
    host: str
    port: int
    token: str
    local_ip: str
    phone_url: str
    safety_notes: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["safety_notes"] = list(self.safety_notes)
        return data


def detect_local_ip() -> str:
    """Return the likely LAN IP without sending application data."""
    fallback = "127.0.0.1"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(0.2)
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except OSError:
        return fallback


def build_mobile_preview_plan(port: int = 8765, token: str | None = None) -> MobilePreviewPlan:
    chosen_token = token or secrets.token_urlsafe(18)
    local_ip = detect_local_ip()
    return MobilePreviewPlan(
        host="0.0.0.0",
        port=port,
        token=chosen_token,
        local_ip=local_ip,
        phone_url=f"http://{local_ip}:{port}/?token={chosen_token}",
        safety_notes=(
            "Use only on a trusted same-Wi-Fi network.",
            "Do not port-forward this dashboard to the public internet.",
            "Stop the preview with Ctrl+C when finished.",
        ),
    )

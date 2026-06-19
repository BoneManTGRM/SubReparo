from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .network_scan import scan_network

IPV4 = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")


def firewall_suggestions(root: Path | None = None) -> dict[str, Any]:
    suggestions: list[dict[str, str]] = []
    seen: set[str] = set()
    for finding in scan_network():
        match = IPV4.search(finding.target)
        if not match:
            continue
        ip = match.group(0)
        if ip in seen:
            continue
        seen.add(ip)
        suggestions.append({
            "ip": ip,
            "reason": finding.message,
            "linux_ufw": f"sudo ufw deny out to {ip}",
            "windows_netsh": f"netsh advfirewall firewall add rule name=\"SubReparo block {ip}\" dir=out action=block remoteip={ip}",
            "macos_pf_note": f"Add a pf rule to block outbound traffic to {ip} after review.",
        })
    return {"suggestions": suggestions}

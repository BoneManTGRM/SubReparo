from __future__ import annotations

import platform
import re
import subprocess
from dataclasses import dataclass

from .models import Finding, FindingType, Severity

IPV4 = re.compile(r"(?P<ip>\d{1,3}(?:\.\d{1,3}){3})(?::(?P<port>\d+))?")
COMMON_LOCAL_PREFIXES = ("127.", "10.", "192.168.", "172.16.", "172.17.", "172.18.", "172.19.", "172.20.", "172.21.", "172.22.", "172.23.", "172.24.", "172.25.", "172.26.", "172.27.", "172.28.", "172.29.", "172.30.", "172.31.", "0.")
RISKY_PORTS = {23, 4444, 5555, 6666, 6667, 8081, 9001, 31337}


@dataclass(frozen=True)
class ConnectionSnapshot:
    proto: str
    local: str
    remote: str
    state: str
    process: str | None = None


def _run_command(command: list[str]) -> str:
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=8,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return completed.stdout or ""


def list_connections() -> list[ConnectionSnapshot]:
    system = platform.system().lower()
    if system == "windows":
        output = _run_command(["netstat", "-ano"])
    else:
        output = _run_command(["netstat", "-an"])
        if not output.strip():
            output = _run_command(["ss", "-tunap"])
    return _parse_netstat(output)


def _parse_netstat(output: str) -> list[ConnectionSnapshot]:
    rows: list[ConnectionSnapshot] = []
    for line in output.splitlines():
        text = line.strip()
        if not text or not text.lower().startswith(("tcp", "udp")):
            continue
        parts = text.split()
        if len(parts) < 4:
            continue
        proto = parts[0]
        local = parts[1] if len(parts) > 1 else ""
        remote = parts[2] if len(parts) > 2 else ""
        state = parts[3] if len(parts) > 3 else ""
        process = parts[-1] if len(parts) > 4 else None
        rows.append(ConnectionSnapshot(proto=proto, local=local, remote=remote, state=state, process=process))
    return rows


def _remote_port(remote: str) -> int | None:
    match = IPV4.search(remote)
    if not match or not match.group("port"):
        return None
    try:
        return int(match.group("port"))
    except ValueError:
        return None


def _remote_ip(remote: str) -> str | None:
    match = IPV4.search(remote)
    return match.group("ip") if match else None


def scan_network(connections: list[ConnectionSnapshot] | None = None) -> list[Finding]:
    findings: list[Finding] = []
    for conn in connections if connections is not None else list_connections():
        remote_ip = _remote_ip(conn.remote)
        port = _remote_port(conn.remote)
        if not remote_ip or remote_ip.startswith(COMMON_LOCAL_PREFIXES):
            continue
        target = f"{conn.proto} {conn.local} -> {conn.remote}"
        if port in RISKY_PORTS:
            findings.append(Finding(
                type=FindingType.IMMUNE_PATROL,
                severity=Severity.MEDIUM,
                target=target,
                message="connection uses uncommon high-risk port",
                recommendation="Confirm the process and destination are expected before trusting this connection.",
                detail=conn.process,
            ))
        elif conn.state.upper() in {"ESTABLISHED", "ESTAB"} and port not in {80, 443, 53, 123}:
            findings.append(Finding(
                type=FindingType.IMMUNE_PATROL,
                severity=Severity.LOW,
                target=target,
                message="external connection on non-standard port",
                recommendation="Review if this connection is unexpected or repeated.",
                detail=conn.process,
            ))
    return findings

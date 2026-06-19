from __future__ import annotations

import platform
import re
import subprocess
from dataclasses import dataclass

from .models import Finding, FindingType, Severity

ENCODED_COMMAND = re.compile(r"(?i)(powershell|pwsh).{0,120}(-enc|-encodedcommand)")
HIDDEN_COMMAND = re.compile(r"(?i)(-windowstyle\s+hidden|wscript|cscript|mshta)")
REMOTE_RUN = re.compile(r"(?i)(curl|wget|iwr|invoke-webrequest).{0,160}(bash|sh|powershell|pwsh|cmd)")
RISKY_LOCATION = re.compile(r"(?i)(appdata|temp|tmp|downloads|public|programdata|/tmp/|/var/tmp/)")
SCRIPT_LAUNCH = re.compile(r"(?i)(\.ps1|\.vbs|\.jse|\.js|\.bat|\.cmd|\.sh|\.py)")
BINARY_LAUNCH = re.compile(r"(?i)(\.exe|\.scr|\.com|\.dll|\.so|\.dylib)(?:\s|$)")
SHELL_OR_LOADER = re.compile(r"(?i)(powershell|pwsh|cmd\.exe|/bin/sh|/bin/bash|bash\s+-c|sh\s+-c|wscript|cscript|mshta|rundll32|regsvr32|curl|wget)")
RISKY_PARENTS = re.compile(r"(?i)(winword|excel|powerpnt|outlook|acrord|chrome|msedge|firefox|safari|teams|slack)")


@dataclass(frozen=True)
class ProcessSnapshot:
    pid: str
    ppid: str
    command: str


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


def list_processes() -> list[ProcessSnapshot]:
    system = platform.system().lower()
    if system == "windows":
        output = _run_command(["wmic", "process", "get", "ProcessId,ParentProcessId,CommandLine", "/FORMAT:CSV"])
        return _parse_wmic(output)
    output = _run_command(["ps", "-eo", "pid=,ppid=,args="])
    return _parse_ps(output)


def _parse_ps(output: str) -> list[ProcessSnapshot]:
    rows: list[ProcessSnapshot] = []
    for line in output.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        parts = stripped.split(None, 2)
        if len(parts) < 3:
            continue
        rows.append(ProcessSnapshot(pid=parts[0], ppid=parts[1], command=parts[2]))
    return rows


def _parse_wmic(output: str) -> list[ProcessSnapshot]:
    rows: list[ProcessSnapshot] = []
    for line in output.splitlines()[1:]:
        if not line.strip():
            continue
        parts = line.split(",")
        if len(parts) < 4:
            continue
        command = ",".join(parts[1:-2]).strip()
        ppid = parts[-2].strip()
        pid = parts[-1].strip()
        rows.append(ProcessSnapshot(pid=pid, ppid=ppid, command=command))
    return rows


def _parent_command(process: ProcessSnapshot, by_pid: dict[str, ProcessSnapshot]) -> str:
    parent = by_pid.get(process.ppid)
    return parent.command if parent else ""


def scan_processes(processes: list[ProcessSnapshot] | None = None) -> list[Finding]:
    findings: list[Finding] = []
    process_rows = processes if processes is not None else list_processes()
    by_pid = {process.pid: process for process in process_rows}
    for process in process_rows:
        command = process.command
        parent_command = _parent_command(process, by_pid)
        target = f"pid={process.pid};ppid={process.ppid}"
        if ENCODED_COMMAND.search(command):
            findings.append(Finding(
                type=FindingType.IMMUNE_PATROL,
                severity=Severity.HIGH,
                target=target,
                message="running process uses encoded shell command",
                recommendation="Review the process command line. Encoded command lines should be treated as suspicious until verified.",
                detail=command[:240],
            ))
        if REMOTE_RUN.search(command):
            findings.append(Finding(
                type=FindingType.IMMUNE_PATROL,
                severity=Severity.HIGH,
                target=target,
                message="running process appears to download and execute content",
                recommendation="Stop and review the process if it was not intentionally started by the user.",
                detail=command[:240],
            ))
        if HIDDEN_COMMAND.search(command):
            findings.append(Finding(
                type=FindingType.IMMUNE_PATROL,
                severity=Severity.MEDIUM,
                target=target,
                message="running process uses hidden or script-host behavior",
                recommendation="Confirm this process belongs to a trusted application.",
                detail=command[:240],
            ))
        if SCRIPT_LAUNCH.search(command) and RISKY_LOCATION.search(command):
            findings.append(Finding(
                type=FindingType.IMMUNE_PATROL,
                severity=Severity.MEDIUM,
                target=target,
                message="script process launched from commonly abused location",
                recommendation="Review the script origin and isolate it if it is unexpected.",
                detail=command[:240],
            ))
        if BINARY_LAUNCH.search(command) and RISKY_LOCATION.search(command):
            findings.append(Finding(
                type=FindingType.IMMUNE_PATROL,
                severity=Severity.MEDIUM,
                target=target,
                message="unknown binary appears to run from commonly abused location",
                recommendation="Confirm the binary publisher and origin before trusting this process.",
                detail=command[:240],
            ))
        if parent_command and RISKY_PARENTS.search(parent_command) and SHELL_OR_LOADER.search(command):
            findings.append(Finding(
                type=FindingType.IMMUNE_PATROL,
                severity=Severity.HIGH,
                target=target,
                message="unusual parent-child process relationship observed",
                recommendation="Review why an application process launched a shell, script host, or network loader.",
                detail=f"parent={parent_command[:160]} child={command[:160]}",
            ))
    return findings

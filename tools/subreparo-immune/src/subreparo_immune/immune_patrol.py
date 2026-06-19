from __future__ import annotations

import hashlib
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .models import Finding, FindingType, Severity

EXCLUDED_DIRS = {
    ".git",
    ".subreparo",
    "node_modules",
    "target",
    "dist",
    "build",
    "__pycache__",
    ".venv",
    "venv",
}

SCRIPT_SUFFIXES = {".ps1", ".bat", ".cmd", ".vbs", ".js", ".jse", ".sh", ".py", ".php", ".rb", ".pl"}
BINARY_SUFFIXES = {".exe", ".dll", ".scr", ".com", ".so", ".dylib", ".jar", ".apk", ".bin"}
PERSISTENCE_NAMES = {"autorun.inf", "launchd.plist", "crontab", "startup.bat"}

TEXT_PATTERNS: list[tuple[str, re.Pattern[str], Severity, str]] = [
    (
        "encoded shell command",
        re.compile(r"(?i)(powershell|pwsh).{0,80}(-enc|-encodedcommand)"),
        Severity.HIGH,
        "Review this script before running it. Encoded commands are often used to hide behavior.",
    ),
    (
        "download and run pattern",
        re.compile(r"(?i)(curl|wget|iwr|invoke-webrequest).{0,120}(bash|sh|powershell|pwsh|cmd)"),
        Severity.HIGH,
        "Do not run remote code directly. Download, inspect, hash, and verify first.",
    ),
    (
        "hidden window execution",
        re.compile(r"(?i)(-windowstyle\s+hidden|wscript\.shell|start-process).{0,120}(-hidden|hidden)"),
        Severity.MEDIUM,
        "Review hidden execution behavior and confirm it is expected.",
    ),
    (
        "startup persistence path",
        re.compile(r"(?i)(startup|runonce|currentversion\\run|launchagents|systemd|crontab)"),
        Severity.MEDIUM,
        "Review startup or scheduled execution behavior and confirm it is expected.",
    ),
]


@dataclass(frozen=True)
class PatrolFile:
    path: Path
    relative: str
    size: int
    sha256: str


def iter_project_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 128), b""):
            digest.update(chunk)
    return digest.hexdigest()


def shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    total = len(data)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def inspect_text(path: Path, relative: str) -> list[Finding]:
    findings: list[Finding] = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return findings
    for line_no, line in enumerate(text.splitlines(), start=1):
        for label, pattern, severity, recommendation in TEXT_PATTERNS:
            if pattern.search(line):
                findings.append(Finding(
                    type=FindingType.IMMUNE_PATROL,
                    severity=severity,
                    target=f"{relative}:{line_no}",
                    message=label,
                    recommendation=recommendation,
                    detail=line.strip()[:180],
                ))
    return findings


def inspect_binary(path: Path, relative: str) -> list[Finding]:
    findings: list[Finding] = []
    try:
        sample = path.read_bytes()[:1024 * 256]
        size = path.stat().st_size
    except OSError:
        return findings
    entropy = shannon_entropy(sample)
    if path.suffix.lower() in BINARY_SUFFIXES:
        findings.append(Finding(
            type=FindingType.IMMUNE_PATROL,
            severity=Severity.MEDIUM,
            target=relative,
            message="executable or binary file present",
            recommendation="Confirm this binary is expected, signed, and from a trusted source before running it.",
            detail=f"size={size}; sha256={file_hash(path)}; entropy={entropy:.3f}",
        ))
    if size > 0 and entropy >= 7.6 and path.suffix.lower() in BINARY_SUFFIXES | SCRIPT_SUFFIXES:
        findings.append(Finding(
            type=FindingType.IMMUNE_PATROL,
            severity=Severity.HIGH,
            target=relative,
            message="high-entropy executable content",
            recommendation="Treat this as suspicious until reviewed. Keep it isolated and verify its origin.",
            detail=f"size={size}; sha256={file_hash(path)}; entropy={entropy:.3f}",
        ))
    return findings


def patrol(root: Path) -> list[Finding]:
    root = root.resolve()
    findings: list[Finding] = []
    for path in iter_project_files(root):
        relative = str(path.relative_to(root))
        lower_name = path.name.lower()
        suffix = path.suffix.lower()
        if lower_name in PERSISTENCE_NAMES:
            findings.append(Finding(
                type=FindingType.IMMUNE_PATROL,
                severity=Severity.MEDIUM,
                target=relative,
                message="startup or persistence-related file name",
                recommendation="Confirm this file is intentional and review what it starts automatically.",
            ))
        if suffix in SCRIPT_SUFFIXES:
            findings.extend(inspect_text(path, relative))
        if suffix in BINARY_SUFFIXES:
            findings.extend(inspect_binary(path, relative))
    return findings

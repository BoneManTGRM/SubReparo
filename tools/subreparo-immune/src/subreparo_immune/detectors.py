from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .models import Finding, FindingType, Severity

EXCLUDED_DIRS = {
    ".git", ".hg", ".svn", ".subreparo", "node_modules", "dist", "build",
    "target", "__pycache__", ".venv", "venv",
}

TEXT_SUFFIXES = {
    ".py", ".rs", ".js", ".ts", ".tsx", ".jsx", ".json", ".toml", ".yaml",
    ".yml", ".md", ".txt", ".html", ".css", ".go", ".java", ".sh", ".env",
}

LOCAL_ONLY_NAMES = {".env", ".env.local", ".env.production", ".npmrc", "secrets.json"}
DEPENDENCY_FILES = {"package.json", "requirements.txt", "pyproject.toml", "Cargo.toml", "go.mod"}

PATTERNS: list[tuple[str, re.Pattern[str], Severity, str]] = [
    (
        "local value assignment",
        re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*=\s*['\"][^'\"]{8,}['\"]"),
        Severity.HIGH,
        "Move local values to approved local configuration and keep only safe examples in shared files.",
    ),
    (
        "private material header",
        re.compile(r"-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----"),
        Severity.CRITICAL,
        "Remove private material from shared project files and verify local-only handling.",
    ),
    (
        "instruction boundary phrase",
        re.compile(r"(?i)ignore (all )?(previous|prior|above) instructions"),
        Severity.MEDIUM,
        "Treat imported text as data only; do not let it control tools or project policy.",
    ),
]


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.is_file():
            files.append(path)
    return files


def scan_project(root: Path) -> list[Finding]:
    root = root.resolve()
    findings: list[Finding] = []
    for path in iter_files(root):
        relative = str(path.relative_to(root))
        if path.name in LOCAL_ONLY_NAMES:
            findings.append(Finding(
                type=FindingType.LOCAL_FILE,
                severity=Severity.HIGH,
                target=relative,
                message=f"Local-only file present: {path.name}",
                recommendation="Confirm it is excluded from shared outputs and create a safe example if needed.",
            ))
        if path.name in DEPENDENCY_FILES:
            findings.append(Finding(
                type=FindingType.DEPENDENCY_REVIEW,
                severity=Severity.LOW,
                target=relative,
                message="Dependency manifest found.",
                recommendation="Run the package manager audit command and record the result before release.",
            ))
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in LOCAL_ONLY_NAMES:
            continue
        try:
            if path.stat().st_size > 1_000_000:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            for label, pattern, severity, recommendation in PATTERNS:
                if pattern.search(line):
                    findings.append(Finding(
                        type=FindingType.CONTENT_PATTERN,
                        severity=severity,
                        target=f"{relative}:{line_no}",
                        message=label,
                        recommendation=recommendation,
                        detail=line.strip()[:160],
                    ))
    return findings


def scan_git(root: Path) -> list[Finding]:
    git_dir = root / ".git"
    if not git_dir.exists():
        return []
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return [Finding(
            type=FindingType.GIT_REVIEW,
            severity=Severity.LOW,
            target=str(root),
            message="Could not read git status.",
            recommendation="Review repository status manually.",
        )]
    changes = [line for line in result.stdout.splitlines() if line.strip()]
    if not changes:
        return []
    return [Finding(
        type=FindingType.GIT_REVIEW,
        severity=Severity.LOW,
        target=str(root),
        message=f"Git working tree has {len(changes)} changed item(s).",
        recommendation="Review local changes before release or deployment.",
    )]


def check_website(url: str, timeout_seconds: int = 10) -> list[Finding]:
    request = Request(url, headers={"User-Agent": "SubReparo-Immune/0.2"})
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            status = int(response.status)
            if 200 <= status < 400:
                return []
            message = f"HTTP {status}"
    except HTTPError as error:
        message = f"HTTP {error.code}"
    except URLError as error:
        message = str(error.reason)
    except TimeoutError:
        message = "request timed out"
    return [Finding(
        type=FindingType.WEBSITE_RESPONSE,
        severity=Severity.MEDIUM,
        target=url,
        message=f"Website did not return a normal response: {message}",
        recommendation="Review hosting, DNS, deployment, and application logs, then recheck.",
    )]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

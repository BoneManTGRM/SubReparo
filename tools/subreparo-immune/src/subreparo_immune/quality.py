from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class QualityCheck:
    name: str
    command: list[str]
    return_code: int
    passed: bool
    stdout: str
    stderr: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _run(command: list[str], cwd: Path, timeout: int = 120) -> QualityCheck:
    try:
        completed = subprocess.run(
            command,
            cwd=str(cwd),
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        return QualityCheck(
            name=" ".join(command),
            command=command,
            return_code=completed.returncode,
            passed=completed.returncode == 0,
            stdout=completed.stdout[-4000:],
            stderr=completed.stderr[-4000:],
        )
    except FileNotFoundError as exc:
        return QualityCheck(
            name=" ".join(command),
            command=command,
            return_code=127,
            passed=False,
            stdout="",
            stderr=str(exc),
        )
    except subprocess.TimeoutExpired as exc:
        return QualityCheck(
            name=" ".join(command),
            command=command,
            return_code=124,
            passed=False,
            stdout=(exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else "",
            stderr=(exc.stderr or "")[-4000:] if isinstance(exc.stderr, str) else "Timed out",
        )


def default_quality_commands(project_root: Path) -> list[list[str]]:
    tool_root = project_root / "tools" / "subreparo-immune"
    if tool_root.exists():
        return [
            [sys.executable, "-m", "compileall", "src", "tests"],
            [sys.executable, "-m", "pytest", "-q"],
        ]
    return [[sys.executable, "-m", "compileall", "."]]


def run_quality(project_root: Path) -> dict[str, Any]:
    project_root = project_root.resolve()
    tool_root = project_root / "tools" / "subreparo-immune"
    cwd = tool_root if tool_root.exists() else project_root
    checks = [_run(command, cwd=cwd) for command in default_quality_commands(project_root)]
    payload = {
        "schema": "subreparo.quality.v1",
        "project_root": str(project_root),
        "working_directory": str(cwd),
        "passed": all(check.passed for check in checks),
        "checks": [check.to_dict() for check in checks],
    }
    state = project_root / ".subreparo"
    state.mkdir(parents=True, exist_ok=True)
    (state / "quality_report.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return payload

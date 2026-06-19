from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .immune_patrol import patrol
from .models import Finding, Severity
from .quarantine import stage_file


@dataclass(frozen=True)
class WatchAlert:
    created_at: str
    severity: str
    target: str
    message: str
    recommendation: str
    staged_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def finding_key(finding: Finding) -> str:
    return f"{finding.type.value}|{finding.severity.value}|{finding.target}|{finding.message}"


def target_path(root: Path, finding: Finding) -> Path | None:
    raw = finding.target.split(":", 1)[0]
    path = (root / raw).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return None
    return path if path.exists() and path.is_file() else None


def should_stage(finding: Finding) -> bool:
    return finding.severity in {Severity.HIGH, Severity.CRITICAL}


def append_alert(state_dir: Path, alert: WatchAlert) -> None:
    state_dir.mkdir(parents=True, exist_ok=True)
    path = state_dir / "watch_alerts.jsonl"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(alert.to_dict(), sort_keys=True) + "\n")


def scan_once(root: Path, known: set[str], apply_quarantine: bool = False) -> list[WatchAlert]:
    root = root.resolve()
    state_dir = root / ".subreparo"
    alerts: list[WatchAlert] = []
    for finding in patrol(root):
        key = finding_key(finding)
        if key in known:
            continue
        known.add(key)
        staged_path: str | None = None
        if apply_quarantine and should_stage(finding):
            file_path = target_path(root, finding)
            if file_path is not None:
                record = stage_file(root, file_path, reason=finding.message, state_dir=state_dir)
                staged_path = record.staged_path
        alert = WatchAlert(
            created_at=now(),
            severity=finding.severity.value,
            target=finding.target,
            message=finding.message,
            recommendation=finding.recommendation,
            staged_path=staged_path,
        )
        append_alert(state_dir, alert)
        alerts.append(alert)
    return alerts


def watch(root: Path, interval_seconds: int = 10, apply_quarantine: bool = False) -> None:
    root = root.resolve()
    known = {finding_key(finding) for finding in patrol(root)}
    print(f"SubReparo Immune Watch started for {root}")
    print(f"Interval: {interval_seconds}s")
    print("Mode: quarantine enabled" if apply_quarantine else "Mode: alert only")
    while True:
        alerts = scan_once(root, known, apply_quarantine=apply_quarantine)
        for alert in alerts:
            print(f"[{alert.severity.upper()}] {alert.message} at {alert.target}")
            print(f"  {alert.recommendation}")
            if alert.staged_path:
                print(f"  Staged: {alert.staged_path}")
        time.sleep(interval_seconds)

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from .timeline import build_timeline


def risk_trends(root: Path) -> dict[str, Any]:
    by_day: Counter[str] = Counter()
    by_severity: Counter[str] = Counter()
    by_type: Counter[str] = Counter()
    for event in build_timeline(root):
        day = str(event.get("created_at", ""))[:10] or "unknown"
        by_day[day] += 1
        data = event.get("data", {})
        finding = data.get("finding", {}) if isinstance(data, dict) else {}
        severity = finding.get("severity")
        category = finding.get("type")
        if severity:
            by_severity[severity] += 1
        if category:
            by_type[category] += 1
    return {
        "events_by_day": dict(sorted(by_day.items())),
        "findings_by_severity": dict(sorted(by_severity.items())),
        "findings_by_type": dict(sorted(by_type.items())),
    }

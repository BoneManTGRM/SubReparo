from __future__ import annotations

from collections import Counter
from typing import Any

from .models import Finding


def summarize_findings(findings: list[Finding]) -> dict[str, Any]:
    by_level = Counter(finding.severity.value for finding in findings)
    by_type = Counter(finding.type.value for finding in findings)
    return {
        "total": len(findings),
        "by_severity": dict(sorted(by_level.items())),
        "by_type": dict(sorted(by_type.items())),
    }


def top_targets(findings: list[Finding], limit: int = 10) -> list[dict[str, Any]]:
    counts = Counter(finding.target.split(":", 1)[0] for finding in findings)
    return [{"target": target, "count": count} for target, count in counts.most_common(limit)]

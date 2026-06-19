from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .feedback import FeedbackState, matches_false_positive
from .models import Finding, Severity

TRUST_REPORT_PATH = Path(".subreparo") / "trust_report.json"
SCHEMA = "subreparo.trust_report.v1"

SEVERITY_PENALTY = {
    Severity.INFO: 0,
    Severity.LOW: 10,
    Severity.MEDIUM: 30,
    Severity.HIGH: 55,
    Severity.CRITICAL: 80,
}


@dataclass(frozen=True)
class TrustScore:
    scope: str
    target: str
    score: int
    finding_count: int
    max_severity: str
    status: str
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "scope": self.scope,
            "target": self.target,
            "score": self.score,
            "finding_count": self.finding_count,
            "max_severity": self.max_severity,
            "status": self.status,
            "reasons": list(self.reasons),
        }


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _raw_target(target: str) -> str:
    return target.split(":", 1)[0]


def _folder_target(target: str) -> str | None:
    raw = _raw_target(target)
    path = Path(raw)
    parent = str(path.parent)
    if parent in {"", "."}:
        return None
    return parent


def _domain_target(target: str) -> str | None:
    parsed = urlparse(target)
    if parsed.hostname:
        return parsed.hostname
    raw = _raw_target(target)
    if "/" in raw or "\\" in raw:
        return None
    if "." in raw and " " not in raw:
        return raw.lower()
    return None


def _max_severity(findings: list[Finding]) -> Severity:
    order = [Severity.INFO, Severity.LOW, Severity.MEDIUM, Severity.HIGH, Severity.CRITICAL]
    return max((finding.severity for finding in findings), key=order.index, default=Severity.INFO)


def _status(score: int, finding_count: int) -> str:
    if finding_count == 0:
        return "trusted"
    if score >= 85:
        return "trusted"
    if score >= 65:
        return "watch"
    if score >= 40:
        return "review"
    return "isolate_or_review"


def _score_group(scope: str, target: str, findings: list[Finding]) -> TrustScore:
    max_severity = _max_severity(findings)
    penalty = max((SEVERITY_PENALTY[finding.severity] for finding in findings), default=0)
    repeated_penalty = min(max(len(findings) - 1, 0) * 5, 15)
    score = max(0, 100 - penalty - repeated_penalty)
    reasons = tuple(f"{finding.severity.value}:{finding.type.value}" for finding in findings[:6])
    return TrustScore(
        scope=scope,
        target=target,
        score=score,
        finding_count=len(findings),
        max_severity=max_severity.value,
        status=_status(score, len(findings)),
        reasons=reasons,
    )


def build_trust_report_from_findings(
    root: Path,
    findings: list[Finding],
    feedback: FeedbackState | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    active_findings = [
        finding for finding in findings if feedback is None or not matches_false_positive(finding, feedback)
    ]
    file_groups: dict[str, list[Finding]] = defaultdict(list)
    folder_groups: dict[str, list[Finding]] = defaultdict(list)
    domain_groups: dict[str, list[Finding]] = defaultdict(list)

    for finding in active_findings:
        file_groups[finding.target].append(finding)
        folder = _folder_target(finding.target)
        if folder:
            folder_groups[folder].append(finding)
        domain = _domain_target(finding.target)
        if domain:
            domain_groups[domain].append(finding)

    file_scores = [_score_group("file", target, group) for target, group in sorted(file_groups.items())]
    folder_scores = [_score_group("folder", target, group) for target, group in sorted(folder_groups.items())]
    domain_scores = [_score_group("domain", target, group) for target, group in sorted(domain_groups.items())]
    all_scores = file_scores + folder_scores + domain_scores
    average = round(sum(item.score for item in all_scores) / len(all_scores), 2) if all_scores else 100.0

    return {
        "schema": SCHEMA,
        "generated_at": now(),
        "project_root": str(root),
        "average_trust": average,
        "active_finding_count": len(active_findings),
        "suppressed_false_positive_count": len(findings) - len(active_findings),
        "file_scores": [item.to_dict() for item in file_scores],
        "folder_scores": [item.to_dict() for item in folder_scores],
        "domain_scores": [item.to_dict() for item in domain_scores],
    }


def write_trust_report(root: Path, findings: list[Finding], feedback: FeedbackState | None = None) -> dict[str, Any]:
    report = build_trust_report_from_findings(root, findings, feedback=feedback)
    path = root.resolve() / TRUST_REPORT_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report

from __future__ import annotations

from pathlib import Path

from subreparo_immune.feedback import mark_false_positive
from subreparo_immune.models import Finding, FindingType, Severity
from subreparo_immune.policy import add_false_positive_target, apply_policy
from subreparo_immune.trust import build_trust_report_from_findings


def _finding(target: str = "scripts/build.py") -> Finding:
    return Finding(
        type=FindingType.IMMUNE_PATROL,
        severity=Severity.HIGH,
        target=target,
        message="startup entry points to a script or executable",
        recommendation="Confirm this startup item is expected.",
    )


def test_policy_false_positive_target_suppresses_matching_findings(tmp_path: Path) -> None:
    policy = add_false_positive_target("safe/*.py", tmp_path / "policy.json")

    findings = apply_policy([_finding("safe/tool.py")], policy)

    assert findings == []
    assert "safe/*.py" in policy.false_positive_targets
    assert "safe/*.py" in policy.trusted_targets


def test_feedback_false_positive_suppresses_trust_report_findings(tmp_path: Path) -> None:
    finding = _finding()
    feedback = mark_false_positive(finding.target, path=tmp_path / "feedback.json")

    report = build_trust_report_from_findings(tmp_path, [finding], feedback=feedback)

    assert report["active_finding_count"] == 0
    assert report["suppressed_false_positive_count"] == 1
    assert report["file_scores"] == []

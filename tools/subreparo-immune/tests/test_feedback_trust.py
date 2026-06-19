from pathlib import Path

from subreparo_immune.feedback import (
    apply_false_positive_feedback,
    load_feedback,
    mark_false_positive,
)
from subreparo_immune.models import Finding, FindingType, Severity
from subreparo_immune.trust import build_trust_report_from_findings, write_trust_report


def finding(target: str, severity: Severity = Severity.HIGH) -> Finding:
    return Finding(
        type=FindingType.IMMUNE_PATROL,
        severity=severity,
        target=target,
        message="test signal",
        recommendation="review locally",
    )


def test_mark_false_positive_filters_matching_finding(tmp_path: Path) -> None:
    feedback_path = tmp_path / ".subreparo" / "feedback.json"
    state = mark_false_positive("src/app.py", "known test fixture", path=feedback_path)

    findings = [finding("src/app.py"), finding("src/other.py")]
    filtered = apply_false_positive_feedback(findings, state)

    assert [item.target for item in filtered] == ["src/other.py"]
    assert load_feedback(feedback_path).false_positives[0].reason == "known test fixture"


def test_trust_report_scores_files_folders_and_domains(tmp_path: Path) -> None:
    findings = [
        finding("src/app.py", Severity.HIGH),
        finding("https://example.com/login", Severity.MEDIUM),
    ]

    report = build_trust_report_from_findings(tmp_path, findings)

    assert report["schema"] == "subreparo.trust_report.v1"
    assert report["active_finding_count"] == 2
    assert any(item["target"] == "src/app.py" for item in report["file_scores"])
    assert any(item["target"] == "src" for item in report["folder_scores"])
    assert any(item["target"] == "example.com" for item in report["domain_scores"])


def test_write_trust_report_persists_json(tmp_path: Path) -> None:
    report = write_trust_report(tmp_path, [finding("src/app.py", Severity.MEDIUM)])
    path = tmp_path / ".subreparo" / "trust_report.json"

    assert path.exists()
    assert report["average_trust"] < 100

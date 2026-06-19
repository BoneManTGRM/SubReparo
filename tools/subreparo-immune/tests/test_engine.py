from pathlib import Path

from subreparo_immune.detectors import scan_project
from subreparo_immune.engine import run_local
from subreparo_immune.models import Finding, FindingType, Severity
from subreparo_immune.scoring import calculate_score


def test_clean_project_scores_high(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("hello\n", encoding="utf-8")
    result = run_local(tmp_path)
    score = result.to_dict()["score"]
    assert score["value"] >= 70
    assert Path(result.report_path).exists()


def test_dependency_file_creates_review_finding(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'x'\n", encoding="utf-8")
    findings = scan_project(tmp_path)
    assert any(f.type == FindingType.DEPENDENCY_REVIEW for f in findings)


def test_score_penalizes_high_findings() -> None:
    findings = [
        Finding(
            type=FindingType.CONTENT_PATTERN,
            severity=Severity.HIGH,
            target="example",
            message="review",
            recommendation="repair",
        )
    ]
    score = calculate_score(findings)
    assert score.value < 100
    assert score.findings == 1

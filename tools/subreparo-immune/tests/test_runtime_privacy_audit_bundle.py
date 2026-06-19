from pathlib import Path

from subreparo_immune.audit import append_audit, verify_audit
from subreparo_immune.incident_bundle import create_bundle
from subreparo_immune.network_scan import ConnectionSnapshot, scan_network
from subreparo_immune.process_scan import ProcessSnapshot, scan_processes
from subreparo_immune.redaction import redact_text
from subreparo_immune.rules import rule_catalog


def test_process_scanner_flags_encoded_command() -> None:
    findings = scan_processes([ProcessSnapshot(pid="1", ppid="0", command="powershell -EncodedCommand AAAA")])
    assert any("encoded" in finding.message for finding in findings)


def test_network_scanner_flags_risky_port() -> None:
    findings = scan_network([ConnectionSnapshot(proto="tcp", local="0.0.0.0:555", remote="8.8.8.8:4444", state="ESTABLISHED")])
    assert any("port" in finding.message for finding in findings)


def test_redaction_removes_email_and_token() -> None:
    redacted = redact_text("user@example.com api_key=supersecretvalue")
    assert "user@example.com" not in redacted
    assert "supersecretvalue" not in redacted


def test_audit_chain_verifies(tmp_path: Path) -> None:
    audit = tmp_path / "audit.jsonl"
    append_audit("one", {"a": 1}, audit)
    append_audit("two", {"b": 2}, audit)
    assert verify_audit(audit)


def test_incident_bundle_uses_safe_files(tmp_path: Path) -> None:
    state = tmp_path / ".subreparo"
    state.mkdir()
    (state / "report.md").write_text("email user@example.com\n", encoding="utf-8")
    bundle = create_bundle(tmp_path)
    assert bundle.exists()


def test_rule_catalog_not_empty() -> None:
    assert len(rule_catalog()) >= 10

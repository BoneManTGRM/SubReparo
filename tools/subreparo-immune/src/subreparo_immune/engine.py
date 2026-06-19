from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .audit import append_audit
from .baseline import compare
from .browser_scan import scan_browser_extensions
from .detectors import check_website, scan_git, scan_project, write_json
from .explain import explain_finding
from .feedback import apply_false_positive_feedback, load_feedback
from .immune_patrol import patrol
from .models import Finding, Severity
from .network_scan import scan_network
from .policy import apply_policy, load_policy
from .process_scan import scan_processes
from .redaction import redact_mapping, redact_text
from .reparodynamics import finding_signal, score_repair
from .scoring import calculate_score
from .shortcut_scan import scan_shortcuts
from .signed_reports import create_report_signature
from .startup_scan import scan_startup
from .trust import build_trust_report_from_findings, write_trust_report

STATE_DIR = Path(".subreparo")
REPORT_PATH = STATE_DIR / "report.md"
LEDGER_PATH = STATE_DIR / "repair_ledger.jsonl"
EXPORT_PATH = STATE_DIR / "chain_export.json"
TRUST_REPORT_PATH = STATE_DIR / "trust_report.json"
SIGNATURE_PATH = STATE_DIR / "report_signature.json"

SEVERITY_STRESS = {
    Severity.INFO: 0.0,
    Severity.LOW: 0.2,
    Severity.MEDIUM: 0.5,
    Severity.HIGH: 0.8,
    Severity.CRITICAL: 1.0,
}


@dataclass(frozen=True)
class EngineResult:
    project: str
    generated_at: str
    findings: list[Finding]
    report_path: str
    ledger_path: str
    export_path: str
    trust_report_path: str
    signature_path: str

    def to_dict(self) -> dict[str, Any]:
        score = calculate_score(self.findings)
        return redact_mapping({
            "project": self.project,
            "generated_at": self.generated_at,
            "score": score.to_dict(),
            "findings": [finding.to_dict() for finding in self.findings],
            "reparodynamics": [repair_metrics(finding) for finding in self.findings],
            "trust": build_trust_report_from_findings(Path(self.project), self.findings),
            "report_path": self.report_path,
            "ledger_path": self.ledger_path,
            "export_path": self.export_path,
            "trust_report_path": self.trust_report_path,
            "signature_path": self.signature_path,
        })


def run_local(project_path: Path, websites: list[str] | None = None) -> EngineResult:
    project_path = project_path.resolve()
    findings = (
        scan_project(project_path)
        + patrol(project_path)
        + compare(project_path)
        + scan_startup(project_path)
        + scan_browser_extensions(project_path)
        + scan_shortcuts(project_path)
        + scan_processes()
        + scan_network()
        + scan_git(project_path)
    )
    policy = load_policy(project_path / ".subreparo" / "policy.json")
    findings = apply_policy(findings, policy)
    for url in websites or []:
        findings.extend(check_website(url))
    feedback = load_feedback(project_path / ".subreparo" / "feedback.json")
    write_trust_report(project_path, findings, feedback=feedback)
    findings = apply_false_positive_feedback(findings, feedback)
    result = EngineResult(
        project=str(project_path),
        generated_at=datetime.now(timezone.utc).isoformat(),
        findings=findings,
        report_path=str(REPORT_PATH),
        ledger_path=str(LEDGER_PATH),
        export_path=str(EXPORT_PATH),
        trust_report_path=str(TRUST_REPORT_PATH),
        signature_path=str(SIGNATURE_PATH),
    )
    write_report(result)
    append_ledger(result)
    write_export(result)
    signature = create_report_signature(project_path)
    append_audit(
        "run_local",
        {
            "project": str(project_path),
            "findings": len(findings),
            "report_signature": signature.get("signature"),
            "signature_type": signature.get("signature_type"),
        },
        project_path / ".subreparo" / "audit.jsonl",
    )
    return result


def repair_metrics(finding: Finding) -> dict[str, Any]:
    stress = SEVERITY_STRESS[finding.severity]
    signal = finding_signal(severity_weight=stress, verified_gain=0.0, energy_cost=1.0)
    score = score_repair(signal)
    return {
        "target": finding.target,
        "type": finding.type.value,
        "signal": signal.to_dict(),
        "score": score.to_dict(),
        "tgrm_phase": score.phase.value,
        "rye": score.rye,
    }


def _trust_report_for_result(result: EngineResult) -> dict[str, Any]:
    return build_trust_report_from_findings(Path(result.project), result.findings)


def _trust_by_target(result: EngineResult) -> dict[str, dict[str, Any]]:
    trust = _trust_report_for_result(result)
    return {item["target"]: item for item in trust.get("file_scores", [])}


def write_report(result: EngineResult) -> None:
    score = calculate_score(result.findings)
    trust = _trust_report_for_result(result)
    lines = [
        "# SubReparo Immune Report",
        "",
        f"Project: `{redact_text(result.project)}`",
        f"Generated: {result.generated_at}",
        "",
        "## Score",
        "",
        f"- Score: **{score.value}/100**",
        f"- Grade: **{score.grade}**",
        f"- Findings: **{score.findings}**",
        f"- Action: {score.action}",
        "",
        "## Trust scoring",
        "",
        f"- Average trust: **{trust.get('average_trust', 100)}**",
        f"- Active findings: **{trust.get('active_finding_count', len(result.findings))}**",
        f"- Trust report: `{result.trust_report_path}`",
        "",
        "Lowest file trust scores:",
    ]
    file_scores = trust.get("file_scores", [])
    if not file_scores:
        lines.append("No low-trust files detected.")
    for item in sorted(file_scores, key=lambda value: value.get("score", 100))[:5]:
        lines.append(
            f"- **{item.get('score')}** `{redact_text(item.get('target', ''))}` "
            f"({item.get('status')})"
        )
    lines.extend([
        "",
        "## Reparodynamics",
        "",
        "SubReparo evaluates findings through TGRM phases and RYE-style repair efficiency metrics.",
        "",
        "## Findings",
        "",
    ])
    trust_by_target = _trust_by_target(result)
    if not result.findings:
        lines.append("No project signals detected.")
    for finding in result.findings:
        metrics = repair_metrics(finding)
        trust_item = trust_by_target.get(finding.target, {})
        lines.append(
            f"- **{finding.severity.value.upper()}** `{finding.type.value}` "
            f"at `{redact_text(finding.target)}`"
        )
        lines.append(f"  - Message: {redact_text(finding.message)}")
        lines.append(f"  - Explanation: {explain_finding(finding)}")
        lines.append(f"  - Recommendation: {redact_text(finding.recommendation)}")
        lines.append(f"  - Trust score: {trust_item.get('score', 'n/a')}")
        lines.append(f"  - TGRM phase: {metrics['tgrm_phase']}")
        lines.append(f"  - RYE: {metrics['rye']}")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_ledger(result: EngineResult) -> None:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    trust_by_target = _trust_by_target(result)
    with LEDGER_PATH.open("a", encoding="utf-8") as handle:
        for finding in result.findings:
            handle.write(json.dumps(redact_mapping({
                "created_at": result.generated_at,
                "project": result.project,
                "finding": finding.to_dict(),
                "reparodynamics": repair_metrics(finding),
                "trust": trust_by_target.get(finding.target),
                "status": "pending",
            }), sort_keys=True) + "\n")


def write_export(result: EngineResult) -> None:
    records = []
    trust_by_target = _trust_by_target(result)
    for index, finding in enumerate(result.findings):
        metrics = repair_metrics(finding)
        trust_item = trust_by_target.get(finding.target, {})
        records.append({
            "local_id": index,
            "category": finding.type.value,
            "severity": finding.severity.value,
            "target": redact_text(finding.target),
            "status": "pending",
            "summary": redact_text(finding.message),
            "tgrm_phase": metrics["tgrm_phase"],
            "rye": metrics["rye"],
            "trust_score": trust_item.get("score"),
            "trust_status": trust_item.get("status"),
        })
    write_json(EXPORT_PATH, {"generated_at": result.generated_at, "records": records})

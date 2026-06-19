from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .detectors import check_website, scan_git, scan_project, write_json
from .immune_patrol import patrol
from .models import Finding, Severity
from .reparodynamics import finding_signal, score_repair
from .scoring import calculate_score

STATE_DIR = Path(".subreparo")
REPORT_PATH = STATE_DIR / "report.md"
LEDGER_PATH = STATE_DIR / "repair_ledger.jsonl"
EXPORT_PATH = STATE_DIR / "chain_export.json"

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

    def to_dict(self) -> dict[str, Any]:
        score = calculate_score(self.findings)
        return {
            "project": self.project,
            "generated_at": self.generated_at,
            "score": score.to_dict(),
            "findings": [finding.to_dict() for finding in self.findings],
            "reparodynamics": [repair_metrics(finding) for finding in self.findings],
            "report_path": self.report_path,
            "ledger_path": self.ledger_path,
            "export_path": self.export_path,
        }


def run_local(project_path: Path, websites: list[str] | None = None) -> EngineResult:
    project_path = project_path.resolve()
    findings = scan_project(project_path) + patrol(project_path) + scan_git(project_path)
    for url in websites or []:
        findings.extend(check_website(url))
    result = EngineResult(
        project=str(project_path),
        generated_at=datetime.now(timezone.utc).isoformat(),
        findings=findings,
        report_path=str(REPORT_PATH),
        ledger_path=str(LEDGER_PATH),
        export_path=str(EXPORT_PATH),
    )
    write_report(result)
    append_ledger(result)
    write_export(result)
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


def write_report(result: EngineResult) -> None:
    score = calculate_score(result.findings)
    lines = [
        "# SubReparo Immune Report",
        "",
        f"Project: `{result.project}`",
        f"Generated: {result.generated_at}",
        "",
        "## Score",
        "",
        f"- Score: **{score.value}/100**",
        f"- Grade: **{score.grade}**",
        f"- Findings: **{score.findings}**",
        f"- Action: {score.action}",
        "",
        "## Reparodynamics",
        "",
        "SubReparo evaluates findings through TGRM phases and RYE-style repair efficiency metrics.",
        "",
        "## Findings",
        "",
    ]
    if not result.findings:
        lines.append("No project signals detected.")
    for finding in result.findings:
        metrics = repair_metrics(finding)
        lines.append(f"- **{finding.severity.value.upper()}** `{finding.type.value}` at `{finding.target}`")
        lines.append(f"  - Message: {finding.message}")
        lines.append(f"  - Recommendation: {finding.recommendation}")
        lines.append(f"  - TGRM phase: {metrics['tgrm_phase']}")
        lines.append(f"  - RYE: {metrics['rye']}")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_ledger(result: EngineResult) -> None:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER_PATH.open("a", encoding="utf-8") as handle:
        for finding in result.findings:
            handle.write(json.dumps({
                "created_at": result.generated_at,
                "project": result.project,
                "finding": finding.to_dict(),
                "reparodynamics": repair_metrics(finding),
                "status": "pending",
            }, sort_keys=True) + "\n")


def write_export(result: EngineResult) -> None:
    records = []
    for index, finding in enumerate(result.findings):
        metrics = repair_metrics(finding)
        records.append({
            "local_id": index,
            "category": finding.type.value,
            "severity": finding.severity.value,
            "target": finding.target,
            "status": "pending",
            "summary": finding.message,
            "tgrm_phase": metrics["tgrm_phase"],
            "rye": metrics["rye"],
        })
    write_json(EXPORT_PATH, {"generated_at": result.generated_at, "records": records})

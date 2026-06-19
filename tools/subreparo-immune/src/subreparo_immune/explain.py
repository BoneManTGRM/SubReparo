from __future__ import annotations

from .models import Finding, Severity

SEVERITY_EXPLANATIONS = {
    Severity.INFO: "Informational signal. It helps build context but does not require immediate action.",
    Severity.LOW: "Low-risk signal. Review when convenient, especially if it appears repeatedly.",
    Severity.MEDIUM: "Medium-risk signal. Review soon and confirm it is expected.",
    Severity.HIGH: "High-risk signal. Isolate or investigate before running or trusting the item.",
    Severity.CRITICAL: "Critical signal. Keep isolated until reviewed and confirmed safe.",
}


def explain_finding(finding: Finding) -> str:
    return SEVERITY_EXPLANATIONS[finding.severity]

from __future__ import annotations

from typing import Any

from .models import Finding, Severity

SEVERITY_DETAILS = {
    Severity.INFO: {
        "risk_band": "informational",
        "impact": "No immediate risk. Useful for context and future comparison.",
        "operator_action": "Record the signal and continue monitoring.",
    },
    Severity.LOW: {
        "risk_band": "low",
        "impact": "Unusual enough to track, but not enough to isolate by itself.",
        "operator_action": "Review during normal maintenance.",
    },
    Severity.MEDIUM: {
        "risk_band": "medium",
        "impact": "Could become harmful when combined with persistence, network access, or unknown origin.",
        "operator_action": "Review source, owner, and recent changes before trusting it.",
    },
    Severity.HIGH: {
        "risk_band": "high",
        "impact": "Likely risky behavior or location that can affect system integrity.",
        "operator_action": "Isolate or disable after review if it is not clearly expected.",
    },
    Severity.CRITICAL: {
        "risk_band": "critical",
        "impact": "Strong signal of dangerous or policy-blocked behavior.",
        "operator_action": "Keep isolated, preserve evidence, and restore only after verification.",
    },
}


def explain_severity(finding: Finding) -> dict[str, Any]:
    detail = SEVERITY_DETAILS[finding.severity]
    return {
        "target": finding.target,
        "severity": finding.severity.value,
        "finding_type": finding.type.value,
        "risk_band": detail["risk_band"],
        "impact": detail["impact"],
        "operator_action": detail["operator_action"],
    }


def severity_sentence(finding: Finding) -> str:
    detail = SEVERITY_DETAILS[finding.severity]
    return f"{detail['risk_band']} risk: {detail['impact']} Action: {detail['operator_action']}"

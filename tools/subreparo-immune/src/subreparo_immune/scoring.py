from __future__ import annotations

from .models import Finding, Score, Severity

WEIGHTS = {
    Severity.INFO: 0,
    Severity.LOW: 3,
    Severity.MEDIUM: 8,
    Severity.HIGH: 18,
    Severity.CRITICAL: 35,
}


def calculate_score(findings: list[Finding]) -> Score:
    penalty = sum(WEIGHTS[f.severity] for f in findings)
    value = max(0, 100 - penalty)
    if value >= 95:
        grade = "S"
        action = "Continue monitoring."
    elif value >= 85:
        grade = "A"
        action = "Minor review recommended."
    elif value >= 70:
        grade = "B"
        action = "Review findings before release."
    elif value >= 50:
        grade = "C"
        action = "Repair and verify before important use."
    else:
        grade = "D"
        action = "Pause important use until reviewed."
    return Score(value=value, grade=grade, findings=len(findings), action=action)

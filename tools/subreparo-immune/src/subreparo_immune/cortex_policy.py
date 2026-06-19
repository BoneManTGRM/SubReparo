from __future__ import annotations

from .cortex_models import ApprovalLevel, CortexDecision, CortexTask

HIGH_IMPACT_TERMS = {
    "spend money",
    "payment",
    "purchase",
    "send email",
    "publish",
    "delete",
    "remove production",
    "production",
    "deploy",
    "legal",
    "medical",
    "financial",
    "share private",
    "external recipient",
}

BLOCKED_TERMS = {
    "hide activity",
    "bypass approval",
    "steal",
    "exfiltrate",
    "credential harvesting",
    "phishing",
    "exploit third party",
    "spread",
    "worm",
}

SAFE_TERMS = {
    "docs",
    "documentation",
    "test",
    "unit test",
    "readme",
    "roadmap",
    "scaffold",
    "local report",
    "safe defensive",
    "dry run",
}


def classify_task(task: CortexTask) -> CortexDecision:
    text = f"{task.title} {task.goal}".lower()

    blocked = next((term for term in BLOCKED_TERMS if term in text), None)
    if blocked:
        return CortexDecision(
            task_title=task.title,
            allowed=False,
            approval_level=ApprovalLevel.BLOCKED,
            reason=f"Blocked term matched: {blocked}",
        )

    high_impact = next((term for term in HIGH_IMPACT_TERMS if term in text), None)
    if high_impact:
        return CortexDecision(
            task_title=task.title,
            allowed=False,
            approval_level=ApprovalLevel.EXPLICIT_APPROVE,
            reason=f"Explicit approval required for high-impact action: {high_impact}",
        )

    safe = next((term for term in SAFE_TERMS if term in text), None)
    if safe:
        return CortexDecision(
            task_title=task.title,
            allowed=True,
            approval_level=ApprovalLevel.SAFE_AUTO,
            reason=f"Safe automation term matched: {safe}",
        )

    return CortexDecision(
        task_title=task.title,
        allowed=False,
        approval_level=ApprovalLevel.REVIEW_FIRST,
        reason="Task should be reviewed before action.",
    )

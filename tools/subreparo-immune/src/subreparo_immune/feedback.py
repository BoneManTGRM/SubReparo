from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import Finding

FEEDBACK_PATH = Path(".subreparo") / "feedback.json"
SCHEMA = "subreparo.feedback.v1"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class FalsePositiveRecord:
    target: str
    reason: str
    created_at: str
    finding_type: str | None = None
    message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FeedbackState:
    false_positives: tuple[FalsePositiveRecord, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": SCHEMA,
            "false_positives": [record.to_dict() for record in self.false_positives],
        }


def default_feedback() -> FeedbackState:
    return FeedbackState(false_positives=())


def load_feedback(path: Path = FEEDBACK_PATH) -> FeedbackState:
    if not path.exists():
        return default_feedback()
    data = json.loads(path.read_text(encoding="utf-8"))
    records = tuple(
        FalsePositiveRecord(
            target=item["target"],
            reason=item.get("reason", "User marked as false positive."),
            created_at=item.get("created_at", now()),
            finding_type=item.get("finding_type"),
            message=item.get("message"),
        )
        for item in data.get("false_positives", [])
        if item.get("target")
    )
    return FeedbackState(false_positives=records)


def save_feedback(state: FeedbackState, path: Path = FEEDBACK_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state.to_dict(), indent=2, sort_keys=True), encoding="utf-8")


def mark_false_positive(
    target: str,
    reason: str = "User marked as false positive.",
    path: Path = FEEDBACK_PATH,
    finding_type: str | None = None,
    message: str | None = None,
) -> FeedbackState:
    state = load_feedback(path)
    remaining = tuple(record for record in state.false_positives if record.target != target)
    next_state = FeedbackState(
        false_positives=remaining
        + (
            FalsePositiveRecord(
                target=target,
                reason=reason,
                created_at=now(),
                finding_type=finding_type,
                message=message,
            ),
        )
    )
    save_feedback(next_state, path)
    return next_state


def false_positive_targets(state: FeedbackState) -> set[str]:
    return {record.target for record in state.false_positives}


def matches_false_positive(finding: Finding, state: FeedbackState) -> bool:
    for record in state.false_positives:
        if record.target != finding.target:
            continue
        if record.finding_type and record.finding_type != finding.type.value:
            continue
        if record.message and record.message != finding.message:
            continue
        return True
    return False


def apply_false_positive_feedback(findings: list[Finding], state: FeedbackState) -> list[Finding]:
    return [finding for finding in findings if not matches_false_positive(finding, state)]

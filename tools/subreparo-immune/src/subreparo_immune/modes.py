from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .models import Severity


@dataclass(frozen=True)
class ModeProfile:
    name: str
    min_severity: Severity
    finding_limit: int
    description: str

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["min_severity"] = self.min_severity.value
        return data


SEVERITY_RANK = {
    Severity.INFO: 0,
    Severity.LOW: 1,
    Severity.MEDIUM: 2,
    Severity.HIGH: 3,
    Severity.CRITICAL: 4,
}

MODES = {
    "simple": ModeProfile("simple", Severity.MEDIUM, 8, "Show the main items that need attention."),
    "family": ModeProfile("family", Severity.HIGH, 5, "Show only high-risk items in plain language."),
    "developer": ModeProfile("developer", Severity.LOW, 20, "Show developer-relevant signals with moderate noise tolerance."),
    "expert": ModeProfile("expert", Severity.INFO, 100, "Show all available findings."),
    "paranoid": ModeProfile("paranoid", Severity.LOW, 100, "Show more signals for aggressive review."),
}


def get_mode(name: str) -> ModeProfile:
    return MODES.get(name, MODES["simple"])


def mode_catalog() -> list[dict[str, Any]]:
    return [profile.to_dict() for profile in MODES.values()]


def filter_for_mode(findings, mode: ModeProfile):
    return [finding for finding in findings if SEVERITY_RANK[finding.severity] >= SEVERITY_RANK[mode.min_severity]][: mode.finding_limit]

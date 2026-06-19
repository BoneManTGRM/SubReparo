from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class Severity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FindingType(str, Enum):
    LOCAL_FILE = "local_file"
    CONTENT_PATTERN = "content_pattern"
    PROJECT_CHANGE = "project_change"
    DEPENDENCY_REVIEW = "dependency_review"
    GIT_REVIEW = "git_review"
    WEBSITE_RESPONSE = "website_response"
    IMMUNE_PATROL = "immune_patrol"
    REPEATED_SIGNAL = "repeated_signal"


@dataclass(frozen=True)
class Finding:
    type: FindingType
    severity: Severity
    target: str
    message: str
    recommendation: str
    detail: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["type"] = self.type.value
        data["severity"] = self.severity.value
        return data


@dataclass(frozen=True)
class Score:
    value: int
    grade: str
    findings: int
    action: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

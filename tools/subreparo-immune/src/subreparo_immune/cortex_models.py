from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class ApprovalLevel(str, Enum):
    SAFE_AUTO = "safe_auto"
    REVIEW_FIRST = "review_first"
    EXPLICIT_APPROVE = "explicit_approve"
    BLOCKED = "blocked"


class CortexTaskStatus(str, Enum):
    PROPOSED = "proposed"
    READY = "ready"
    RUNNING = "running"
    WAITING_APPROVAL = "waiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class CortexRole(str, Enum):
    PLANNER = "planner"
    RESEARCHER = "researcher"
    BUILDER = "builder"
    TESTER = "tester"
    SECURITY_REVIEWER = "security_reviewer"
    DOCUMENTER = "documenter"
    RELEASE_MANAGER = "release_manager"
    MONITOR = "monitor"
    REPAIR_VERIFIER = "repair_verifier"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class CortexTask:
    title: str
    goal: str
    role: CortexRole
    approval_level: ApprovalLevel
    status: CortexTaskStatus = CortexTaskStatus.PROPOSED
    evidence: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=now)
    updated_at: str = field(default_factory=now)
    result: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["role"] = self.role.value
        data["approval_level"] = self.approval_level.value
        data["status"] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CortexTask":
        return cls(
            title=data["title"],
            goal=data["goal"],
            role=CortexRole(data["role"]),
            approval_level=ApprovalLevel(data["approval_level"]),
            status=CortexTaskStatus(data.get("status", CortexTaskStatus.PROPOSED.value)),
            evidence=list(data.get("evidence", [])),
            created_at=data.get("created_at", now()),
            updated_at=data.get("updated_at", now()),
            result=data.get("result"),
        )


@dataclass(frozen=True)
class CortexDecision:
    task_title: str
    allowed: bool
    approval_level: ApprovalLevel
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_title": self.task_title,
            "allowed": self.allowed,
            "approval_level": self.approval_level.value,
            "reason": self.reason,
        }

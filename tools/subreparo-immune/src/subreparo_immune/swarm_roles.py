from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class SwarmRole:
    key: str
    name: str
    mission: str
    tools: tuple[str, ...]
    output: str

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["tools"] = list(self.tools)
        return data


SWARM_ROLES = (
    SwarmRole(
        key="planner",
        name="Planner",
        mission="Break project goals into safe tasks and approval-gated milestones.",
        tools=("quality_gate", "skill_review"),
        output="task plan",
    ),
    SwarmRole(
        key="sentinel",
        name="Sentinel",
        mission="Watch local risk signals and protect the platform from unsafe changes.",
        tools=("scan_project", "immune_patrol", "baseline_diff", "skill_review"),
        output="risk report",
    ),
    SwarmRole(
        key="builder",
        name="Builder",
        mission="Apply safe docs, tests, and local project improvements.",
        tools=("snapshot", "quality_gate"),
        output="change set",
    ),
    SwarmRole(
        key="tester",
        name="Tester",
        mission="Run verification checks and record pass/fail outcomes.",
        tools=("quality_gate",),
        output="quality report",
    ),
    SwarmRole(
        key="reviewer",
        name="Reviewer",
        mission="Review high-impact requests before approval.",
        tools=("skill_review", "quality_gate"),
        output="approval recommendation",
    ),
    SwarmRole(
        key="archivist",
        name="Archivist",
        mission="Maintain local memory, status, outcomes, reports, and snapshots.",
        tools=("snapshot",),
        output="memory record",
    ),
)


def swarm_role_catalog() -> list[dict[str, Any]]:
    return [role.to_dict() for role in SWARM_ROLES]


def get_swarm_role(key: str) -> SwarmRole | None:
    for role in SWARM_ROLES:
        if role.key == key:
            return role
    return None

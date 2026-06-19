from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .swarm_roles import get_swarm_role
from .swarm_tools import get_swarm_tool


@dataclass(frozen=True)
class SwarmRoute:
    task: str
    role: str
    tool_keys: list[str]
    approval_required: bool
    blocked: bool
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def route_swarm_task(task: str) -> SwarmRoute:
    text = task.lower()
    if any(term in text for term in ("delete", "spend", "publish", "send email", "secret")):
        return SwarmRoute(
            task=task,
            role="reviewer",
            tool_keys=[],
            approval_required=True,
            blocked=True,
            reason="High-impact or private-data task requires explicit human review.",
        )

    if any(term in text for term in ("test", "quality", "verify", "ci")):
        role_key = "tester"
        tool_keys = ["quality_gate"]
    elif any(term in text for term in ("scan", "risk", "threat", "patrol", "baseline")):
        role_key = "sentinel"
        tool_keys = ["scan_project", "immune_patrol", "baseline_diff"]
    elif any(term in text for term in ("docs", "readme", "roadmap", "write")):
        role_key = "builder"
        tool_keys = ["snapshot", "quality_gate"]
    elif any(term in text for term in ("plugin", "skill", "addon", "manifest")):
        role_key = "reviewer"
        tool_keys = ["skill_review"]
    else:
        role_key = "planner"
        tool_keys = ["quality_gate"]

    role = get_swarm_role(role_key)
    tools = [get_swarm_tool(key) for key in tool_keys]
    approval_required = any(tool.approval_required for tool in tools if tool is not None)
    return SwarmRoute(
        task=task,
        role=role.key if role else role_key,
        tool_keys=tool_keys,
        approval_required=approval_required,
        blocked=False,
        reason="Task routed to safest matching swarm role and bounded tool set.",
    )

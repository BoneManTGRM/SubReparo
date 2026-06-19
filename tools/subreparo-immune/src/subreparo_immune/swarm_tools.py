from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class SwarmToolRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class SwarmTool:
    key: str
    name: str
    purpose: str
    risk: SwarmToolRisk
    approval_required: bool
    destructive: bool
    command_hint: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["risk"] = self.risk.value
        return data


SWARM_TOOLS = (
    SwarmTool(
        key="scan_project",
        name="Project scanner",
        purpose="Review local project files and configuration signals.",
        risk=SwarmToolRisk.LOW,
        approval_required=False,
        destructive=False,
        command_hint="subreparo-immune run . --json",
    ),
    SwarmTool(
        key="immune_patrol",
        name="Immune patrol",
        purpose="Review suspicious local scripts, binaries, launchers, startup items, and behavior signals.",
        risk=SwarmToolRisk.LOW,
        approval_required=False,
        destructive=False,
        command_hint="subreparo-immune patrol . --json",
    ),
    SwarmTool(
        key="baseline_diff",
        name="Baseline diff",
        purpose="Compare watched files against local integrity memory.",
        risk=SwarmToolRisk.LOW,
        approval_required=False,
        destructive=False,
        command_hint="subreparo-immune diff . --json",
    ),
    SwarmTool(
        key="quality_gate",
        name="Quality gate",
        purpose="Run compile and unit-test checks.",
        risk=SwarmToolRisk.LOW,
        approval_required=False,
        destructive=False,
        command_hint="subreparo-immune quality . --json",
    ),
    SwarmTool(
        key="skill_review",
        name="Safe skill review",
        purpose="Review skill/plugin manifests without executing them.",
        risk=SwarmToolRisk.LOW,
        approval_required=False,
        destructive=False,
        command_hint="python -m subreparo_immune.skills_cli . --json",
    ),
    SwarmTool(
        key="snapshot",
        name="Project snapshot",
        purpose="Create a local archive snapshot before larger changes.",
        risk=SwarmToolRisk.MEDIUM,
        approval_required=False,
        destructive=False,
        command_hint="create_snapshot(path)",
    ),
    SwarmTool(
        key="quarantine_stage",
        name="Quarantine staging",
        purpose="Move high-risk local findings into SubReparo staging for review and restore.",
        risk=SwarmToolRisk.HIGH,
        approval_required=True,
        destructive=False,
        command_hint="subreparo-immune isolate . --apply",
    ),
)


def swarm_tool_catalog() -> list[dict[str, Any]]:
    return [tool.to_dict() for tool in SWARM_TOOLS]


def get_swarm_tool(key: str) -> SwarmTool | None:
    for tool in SWARM_TOOLS:
        if tool.key == key:
            return tool
    return None

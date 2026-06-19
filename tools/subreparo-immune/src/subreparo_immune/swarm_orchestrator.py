from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .swarm_router import route_swarm_task
from .swarm_roles import get_swarm_role
from .swarm_tools import get_swarm_tool

PLAN_PATH = Path(".subreparo") / "swarm_plans.jsonl"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class SwarmPlanStep:
    order: int
    role: str
    tool_key: str
    purpose: str
    approval_required: bool
    destructive: bool
    command_hint: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SwarmPlan:
    created_at: str
    goal: str
    blocked: bool
    approval_required: bool
    reason: str
    primary_role: str
    steps: list[SwarmPlanStep]

    def to_dict(self) -> dict[str, Any]:
        return {
            "created_at": self.created_at,
            "goal": self.goal,
            "blocked": self.blocked,
            "approval_required": self.approval_required,
            "reason": self.reason,
            "primary_role": self.primary_role,
            "steps": [step.to_dict() for step in self.steps],
        }


def build_swarm_plan(goal: str) -> SwarmPlan:
    route = route_swarm_task(goal)
    role = get_swarm_role(route.role)
    steps: list[SwarmPlanStep] = []

    if not route.blocked:
        for index, key in enumerate(route.tool_keys, start=1):
            tool = get_swarm_tool(key)
            if tool is None:
                continue
            steps.append(SwarmPlanStep(
                order=index,
                role=role.key if role else route.role,
                tool_key=tool.key,
                purpose=tool.purpose,
                approval_required=tool.approval_required,
                destructive=tool.destructive,
                command_hint=tool.command_hint,
            ))

    return SwarmPlan(
        created_at=now(),
        goal=goal,
        blocked=route.blocked,
        approval_required=route.approval_required or any(step.approval_required for step in steps),
        reason=route.reason,
        primary_role=route.role,
        steps=steps,
    )


def save_swarm_plan(root: Path, plan: SwarmPlan, path: Path | None = None) -> Path:
    root = root.resolve()
    target = path or root / PLAN_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(plan.to_dict(), sort_keys=True) + "\n")
    return target


def list_swarm_plans(root: Path, path: Path | None = None) -> list[dict[str, Any]]:
    target = path or root.resolve() / PLAN_PATH
    if not target.exists():
        return []
    plans: list[dict[str, Any]] = []
    for line in target.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip():
            plans.append(json.loads(line))
    return plans


def orchestrate_swarm(root: Path, goal: str, save: bool = True) -> dict[str, Any]:
    plan = build_swarm_plan(goal)
    saved_path = str(save_swarm_plan(root, plan)) if save else None
    return {
        "schema": "subreparo.swarm_plan.v1",
        "plan": plan.to_dict(),
        "saved_path": saved_path,
    }

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .detectors import scan_git, scan_project
from .immune_patrol import patrol
from .models import Finding, Severity
from .outcome_records import append_outcome
from .swarm_orchestrator import build_swarm_plan, save_swarm_plan

AGENT_CYCLES_PATH = Path(".subreparo") / "agent_cycles.jsonl"
AGENT_SCARS_PATH = Path(".subreparo") / "agent_scars.jsonl"
REPAIR_LEDGER_PATH = Path(".subreparo") / "repair_ledger.jsonl"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_digest(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class AgentToolUse:
    tool: str
    purpose: str
    approved: bool
    result_summary: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AgentRepairPlan:
    title: str
    description: str
    safe_to_apply: bool
    approval_required: bool
    verification: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AgentCycle:
    created_at: str
    goal: str
    phase: str
    observations: list[str]
    finding_count: int
    highest_severity: str
    plans: list[AgentRepairPlan]
    tool_use: list[AgentToolUse]
    verified: bool
    proof_digest: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "created_at": self.created_at,
            "goal": self.goal,
            "phase": self.phase,
            "observations": self.observations,
            "finding_count": self.finding_count,
            "highest_severity": self.highest_severity,
            "plans": [item.to_dict() for item in self.plans],
            "tool_use": [item.to_dict() for item in self.tool_use],
            "verified": self.verified,
            "proof_digest": self.proof_digest,
        }


def _severity_rank(severity: Severity) -> int:
    order = {
        Severity.INFO: 0,
        Severity.LOW: 1,
        Severity.MEDIUM: 2,
        Severity.HIGH: 3,
        Severity.CRITICAL: 4,
    }
    return order.get(severity, 0)


def highest_severity(findings: list[Finding]) -> str:
    if not findings:
        return Severity.INFO.value
    return max((finding.severity for finding in findings), key=_severity_rank).value


def read_jsonl(path: Path, limit: int = 25) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[-limit:]:
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"unreadable": line})
    return rows


def read_scar_memory(root: Path, limit: int = 25) -> dict[str, Any]:
    root = root.resolve()
    return {
        "schema": "subreparo.agent_scars.v1",
        "repair_ledger_tail": read_jsonl(root / REPAIR_LEDGER_PATH, limit=limit),
        "agent_scars_tail": read_jsonl(root / AGENT_SCARS_PATH, limit=limit),
    }


def append_agent_record(root: Path, relative_path: Path, payload: dict[str, Any]) -> Path:
    target = root.resolve() / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")
    return target


def observe(root: Path) -> tuple[list[Finding], list[AgentToolUse]]:
    root = root.resolve()
    project_findings = scan_project(root)
    patrol_findings = patrol(root)
    git_findings = scan_git(root)
    findings = project_findings + patrol_findings + git_findings
    tool_use = [
        AgentToolUse(
            tool="scan_project",
            purpose="Observe local project structure and configuration.",
            approved=True,
            result_summary=f"{len(project_findings)} project findings.",
        ),
        AgentToolUse(
            tool="immune_patrol",
            purpose="Detect suspicious local scripts and behavior patterns.",
            approved=True,
            result_summary=f"{len(patrol_findings)} immune patrol findings.",
        ),
        AgentToolUse(
            tool="scan_git",
            purpose="Review local git working-tree status.",
            approved=True,
            result_summary=f"{len(git_findings)} git findings.",
        ),
    ]
    return findings, tool_use


def make_repair_plans(goal: str, findings: list[Finding]) -> list[AgentRepairPlan]:
    if not findings:
        return [
            AgentRepairPlan(
                title="No repair needed",
                description="No findings were detected by the current observer set.",
                safe_to_apply=True,
                approval_required=False,
                verification="Run quality gate and compare next agent cycle.",
            )
        ]

    plans: list[AgentRepairPlan] = []
    for finding in findings[:10]:
        high_impact = finding.severity in {Severity.HIGH, Severity.CRITICAL}
        plans.append(
            AgentRepairPlan(
                title=f"Repair plan for {finding.target}",
                description=finding.recommendation or finding.message,
                safe_to_apply=not high_impact,
                approval_required=high_impact,
                verification="Re-run observe/detect cycle and quality gate after change.",
            )
        )
    return plans


def run_agent_cycle(root: Path, goal: str = "self-heal project", apply_safe_repairs: bool = False) -> dict[str, Any]:
    root = root.resolve()
    findings, tool_use = observe(root)
    severity = highest_severity(findings)
    observations = [finding.message for finding in findings[:25]]
    plans = make_repair_plans(goal, findings)
    swarm_plan = build_swarm_plan(goal)
    save_swarm_plan(root, swarm_plan)

    verified = not findings or all(plan.safe_to_apply for plan in plans)
    phase = "VERIFY" if verified else "REVIEW_REQUIRED"
    cycle_payload = {
        "created_at": utc_now(),
        "goal": goal,
        "phase": phase,
        "observations": observations,
        "finding_count": len(findings),
        "highest_severity": severity,
        "plans": [plan.to_dict() for plan in plans],
        "tool_use": [tool.to_dict() for tool in tool_use],
        "verified": verified,
        "swarm_plan": swarm_plan.to_dict(),
        "apply_safe_repairs_requested": apply_safe_repairs,
        "applied_repairs": [],
    }
    digest = stable_digest(cycle_payload)
    cycle = AgentCycle(
        created_at=cycle_payload["created_at"],
        goal=goal,
        phase=phase,
        observations=observations,
        finding_count=len(findings),
        highest_severity=severity,
        plans=plans,
        tool_use=tool_use,
        verified=verified,
        proof_digest=digest,
    )
    append_agent_record(root, AGENT_CYCLES_PATH, cycle.to_dict())
    append_agent_record(root, AGENT_SCARS_PATH, {
        "created_at": cycle.created_at,
        "goal": goal,
        "phase": phase,
        "highest_severity": severity,
        "finding_count": len(findings),
        "proof_digest": digest,
    })
    append_outcome(
        root=root,
        title="agent_cycle",
        status="verified" if verified else "review_required",
        details={"goal": goal, "proof_digest": digest, "finding_count": len(findings)},
    )
    return {
        "schema": "subreparo.immune_agent_cycle.v1",
        "cycle": cycle.to_dict(),
        "scar_memory": read_scar_memory(root, limit=10),
        "swarm_plan": swarm_plan.to_dict(),
        "note": "Prototype loop plans and records repairs. High-impact changes remain approval-gated.",
    }

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

SCHEMA = "subreparo.agent_components.v1"

MINIMAL_AGENT_INGREDIENTS = (
    "external_knowledge",
    "tools",
    "prompting",
)


@dataclass(frozen=True)
class AgentComponent:
    key: str
    name: str
    purpose: str
    implementation_level: str
    local_artifacts: tuple[str, ...]
    safety_boundary: str
    approval_required_for: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["local_artifacts"] = list(self.local_artifacts)
        data["approval_required_for"] = list(self.approval_required_for)
        return data


AGENT_COMPONENTS = (
    AgentComponent(
        key="llm_brain",
        name="LLM brain",
        purpose="Reason over local findings, policy, memory, and repair plans.",
        implementation_level="registered_not_connected",
        local_artifacts=("src/subreparo_immune/agent_components.py",),
        safety_boundary=(
            "No external model call is made by this registry. Any live LLM connector must be "
            "explicitly configured, local-first where possible, and approval-gated."
        ),
        approval_required_for=("external model calls", "sharing private project context"),
    ),
    AgentComponent(
        key="prompting",
        name="Prompting and instructions",
        purpose="Constrain Cortex tasks with defensive scope, approval policy, and safe work rules.",
        implementation_level="implemented",
        local_artifacts=(
            "src/subreparo_immune/cortex_policy.py",
            "src/subreparo_immune/cortex_planner.py",
        ),
        safety_boundary="Prompting must preserve the defensive-only and review-first boundaries.",
    ),
    AgentComponent(
        key="memory",
        name="Memory",
        purpose="Remember tasks, approvals, outcomes, quality reports, snapshots, and scar history.",
        implementation_level="implemented",
        local_artifacts=(
            "src/subreparo_immune/cortex_memory.py",
            "src/subreparo_immune/outcome_records.py",
        ),
        safety_boundary="Memory is local JSON/JSONL state under .subreparo by default.",
    ),
    AgentComponent(
        key="external_knowledge",
        name="External knowledge",
        purpose="Ground decisions in local docs, reports, manifests, rule catalogs, and safe lookups.",
        implementation_level="implemented",
        local_artifacts=(
            "README.md",
            "src/subreparo_immune/rule_catalog.py",
            "src/subreparo_immune/sbom.py",
        ),
        safety_boundary="Raw private files stay local; chain exports and shared records should be digests only.",
    ),
    AgentComponent(
        key="tools",
        name="Tools",
        purpose="Use bounded local tools for scan, patrol, baseline, quarantine, reports, and dashboard.",
        implementation_level="implemented",
        local_artifacts=(
            "src/subreparo_immune/cli.py",
            "src/subreparo_immune/quarantine.py",
            "src/subreparo_immune/dashboard.py",
        ),
        safety_boundary="Tools must remain non-destructive unless an explicit approved action is requested.",
    ),
)


def _artifact_present(root: Path, artifact: str) -> bool:
    candidates = (
        root / artifact,
        root / "tools" / "subreparo-immune" / artifact,
    )
    return any(candidate.exists() for candidate in candidates)


def build_agent_component_report(root: Path) -> dict[str, Any]:
    root = root.resolve()
    components: list[dict[str, Any]] = []
    for component in AGENT_COMPONENTS:
        artifacts = [
            {"path": artifact, "present": _artifact_present(root, artifact)}
            for artifact in component.local_artifacts
        ]
        artifact_present = any(item["present"] for item in artifacts)
        component_payload = component.to_dict()
        component_payload["artifacts"] = artifacts
        component_payload["artifact_present"] = artifact_present
        component_payload["operational"] = (
            component.implementation_level == "implemented" and artifact_present
        )
        components.append(component_payload)

    return {
        "schema": SCHEMA,
        "minimal_agent_ingredients": list(MINIMAL_AGENT_INGREDIENTS),
        "component_count": len(components),
        "registered_count": len(components),
        "operational_count": sum(1 for item in components if item["operational"]),
        "components": components,
        "safety_model": {
            "local_first": True,
            "defensive_only": True,
            "approval_gated_high_impact_actions": True,
            "raw_private_data_shared_by_default": False,
        },
    }

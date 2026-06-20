from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

FACTORY_DIR = Path(".subreparo") / "factory"
REGISTRY_PATH = FACTORY_DIR / "agent_registry.jsonl"


class AgentRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKED = "blocked"


SAFE_PERMISSIONS = {
    "read_project",
    "read_subreparo_state",
    "write_subreparo_state",
    "write_reports",
}

REVIEW_PERMISSIONS = {
    "write_project",
    "network_read",
    "external_message",
    "publish_public",
}

BLOCKED_PERMISSIONS = {
    "delete_data",
    "spend_money",
    "read_secrets",
    "shell_write",
    "credential_access",
}


@dataclass(frozen=True)
class AgentBlueprint:
    key: str
    name: str
    purpose: str
    category: str
    default_tools: tuple[str, ...]
    default_permissions: tuple[str, ...]
    memory_policy: str
    approval_policy: str
    test_plan: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["default_tools"] = list(self.default_tools)
        data["default_permissions"] = list(self.default_permissions)
        data["test_plan"] = list(self.test_plan)
        return data


BLUEPRINTS: dict[str, AgentBlueprint] = {
    "code_review": AgentBlueprint(
        key="code_review",
        name="Code Review Agent",
        purpose="Review project changes, detect risky patterns, and produce safe review notes.",
        category="engineering",
        default_tools=("scan_project", "scan_git", "quality_gate"),
        default_permissions=("read_project", "read_subreparo_state", "write_reports"),
        memory_policy="Store review summaries, finding categories, and verification outcomes only.",
        approval_policy="No code changes. Suggestions only unless explicitly upgraded.",
        test_plan=("manifest validates", "permissions are low risk", "report output is deterministic"),
    ),
    "test_builder": AgentBlueprint(
        key="test_builder",
        name="Test Builder Agent",
        purpose="Suggest and scaffold tests for project code under approval control.",
        category="engineering",
        default_tools=("scan_project", "quality_gate", "snapshot"),
        default_permissions=("read_project", "write_project", "read_subreparo_state", "write_reports"),
        memory_policy="Store test gaps, generated test summaries, and pass/fail outcomes.",
        approval_policy="Writing tests requires review before apply.",
        test_plan=("manifest validates", "write permission requires review", "quality gate is included"),
    ),
    "docs_writer": AgentBlueprint(
        key="docs_writer",
        name="Documentation Agent",
        purpose="Draft README, setup guides, changelogs, and operator notes.",
        category="documentation",
        default_tools=("scan_project", "skill_review"),
        default_permissions=("read_project", "write_project", "write_reports"),
        memory_policy="Store doc requests, generated section summaries, and user-approved versions.",
        approval_policy="Draft first; apply edits only after approval.",
        test_plan=("manifest validates", "doc output exists", "write permission requires review"),
    ),
    "website_monitor": AgentBlueprint(
        key="website_monitor",
        name="Website Monitor Agent",
        purpose="Check website availability and summarize response health.",
        category="monitoring",
        default_tools=("website_response", "quality_gate"),
        default_permissions=("network_read", "read_subreparo_state", "write_reports"),
        memory_policy="Store status summaries, timestamps, and response categories.",
        approval_policy="Network reads only. No network writes.",
        test_plan=("manifest validates", "network_read requires review", "report output is deterministic"),
    ),
    "report_generator": AgentBlueprint(
        key="report_generator",
        name="Report Generator Agent",
        purpose="Generate structured local reports from SubReparo state.",
        category="reporting",
        default_tools=("status_report", "timeline", "risk_trends"),
        default_permissions=("read_subreparo_state", "write_reports"),
        memory_policy="Store report hashes, report types, and generated timestamps.",
        approval_policy="Read local state and write reports only.",
        test_plan=("manifest validates", "report command works", "no external permissions"),
    ),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return cleaned or "custom-agent"


def list_blueprints() -> list[dict[str, Any]]:
    return [item.to_dict() for item in BLUEPRINTS.values()]


def build_agent_manifest(blueprint_key: str, name: str | None = None, purpose: str | None = None) -> dict[str, Any]:
    blueprint = BLUEPRINTS.get(blueprint_key)
    if blueprint is None:
        raise ValueError(f"Unknown blueprint: {blueprint_key}")
    agent_name = name or blueprint.name
    return {
        "schema": "subreparo.agent_manifest.v1",
        "id": slugify(agent_name),
        "name": agent_name,
        "blueprint": blueprint.key,
        "purpose": purpose or blueprint.purpose,
        "category": blueprint.category,
        "tools": list(blueprint.default_tools),
        "permissions": list(blueprint.default_permissions),
        "memory_policy": blueprint.memory_policy,
        "approval_policy": blueprint.approval_policy,
        "test_plan": list(blueprint.test_plan),
        "created_at": utc_now(),
        "status": "draft",
    }


def review_agent_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    permissions = set(manifest.get("permissions", []))
    blocked = sorted(permissions & BLOCKED_PERMISSIONS)
    review = sorted(permissions & REVIEW_PERMISSIONS)
    unknown = sorted(permissions - SAFE_PERMISSIONS - REVIEW_PERMISSIONS - BLOCKED_PERMISSIONS)
    if blocked:
        risk = AgentRisk.BLOCKED
        approved = False
        reason = "Blocked permissions present."
    elif unknown:
        risk = AgentRisk.HIGH
        approved = False
        reason = "Unknown permissions require security review."
    elif review:
        risk = AgentRisk.MEDIUM
        approved = False
        reason = "Review permissions present; human approval required."
    else:
        risk = AgentRisk.LOW
        approved = True
        reason = "Low-risk permissions only."
    return {
        "schema": "subreparo.agent_review.v1",
        "agent_id": manifest.get("id"),
        "approved_for_registry": approved,
        "risk": risk.value,
        "reason": reason,
        "blocked_permissions": blocked,
        "review_permissions": review,
        "unknown_permissions": unknown,
    }


def scaffold_agent(root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    root = root.resolve()
    agent_id = manifest["id"]
    target_dir = root / ".subreparo" / "factory" / "agents" / agent_id
    target_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = target_dir / "agent.json"
    readme_path = target_dir / "README.md"
    tests_path = target_dir / "test_plan.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    readme_path.write_text(
        f"# {manifest['name']}\n\n{manifest['purpose']}\n\n"
        f"Blueprint: `{manifest['blueprint']}`\n\n"
        f"Status: `{manifest['status']}`\n\n"
        "This is a SubReparo Factory scaffold. Review permissions before enabling the agent.\n",
        encoding="utf-8",
    )
    tests_path.write_text(json.dumps({"test_plan": manifest.get("test_plan", [])}, indent=2), encoding="utf-8")
    return {
        "schema": "subreparo.agent_scaffold.v1",
        "agent_id": agent_id,
        "directory": str(target_dir),
        "files": [str(manifest_path), str(readme_path), str(tests_path)],
    }


def register_agent(root: Path, manifest: dict[str, Any], review: dict[str, Any] | None = None) -> dict[str, Any]:
    root = root.resolve()
    review_payload = review or review_agent_manifest(manifest)
    registry_path = root / REGISTRY_PATH
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "schema": "subreparo.agent_registry_record.v1",
        "created_at": utc_now(),
        "manifest": manifest,
        "review": review_payload,
        "registered": bool(review_payload.get("approved_for_registry")),
    }
    with registry_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    return record


def list_registered_agents(root: Path, limit: int = 50) -> list[dict[str, Any]]:
    path = root.resolve() / REGISTRY_PATH
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[-limit:]:
        if not line.strip():
            continue
        rows.append(json.loads(line))
    return rows


def create_agent_from_blueprint(root: Path, blueprint_key: str, name: str | None = None, purpose: str | None = None, register: bool = False) -> dict[str, Any]:
    manifest = build_agent_manifest(blueprint_key, name=name, purpose=purpose)
    review = review_agent_manifest(manifest)
    scaffold = scaffold_agent(root, manifest)
    registry = register_agent(root, manifest, review) if register else None
    return {
        "schema": "subreparo.agent_factory_result.v1",
        "manifest": manifest,
        "review": review,
        "scaffold": scaffold,
        "registry": registry,
    }

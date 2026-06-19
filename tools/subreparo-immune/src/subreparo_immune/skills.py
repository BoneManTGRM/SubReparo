from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any


class SkillRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKED = "blocked"


PERMISSION_RISK = {
    "read_project": SkillRisk.LOW,
    "write_project": SkillRisk.MEDIUM,
    "read_subreparo_state": SkillRisk.LOW,
    "write_subreparo_state": SkillRisk.MEDIUM,
    "network_read": SkillRisk.MEDIUM,
    "network_write": SkillRisk.HIGH,
    "shell_read": SkillRisk.HIGH,
    "shell_write": SkillRisk.BLOCKED,
    "secrets_read": SkillRisk.BLOCKED,
    "external_message": SkillRisk.HIGH,
    "publish_public": SkillRisk.HIGH,
    "spend_money": SkillRisk.BLOCKED,
    "delete_data": SkillRisk.BLOCKED,
}

REQUIRED_FIELDS = {"name", "version", "description", "permissions"}


@dataclass(frozen=True)
class SkillManifest:
    name: str
    version: str
    description: str
    permissions: list[str]
    entrypoint: str | None = None
    author: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SkillReview:
    path: str
    valid: bool
    risk: SkillRisk
    messages: list[str]
    manifest: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["risk"] = self.risk.value
        return data


def load_manifest(path: Path) -> SkillManifest:
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = REQUIRED_FIELDS - set(data)
    if missing:
        raise ValueError(f"Missing required skill manifest fields: {', '.join(sorted(missing))}")
    permissions = data["permissions"]
    if not isinstance(permissions, list) or not all(isinstance(item, str) for item in permissions):
        raise ValueError("Skill permissions must be a list of strings.")
    return SkillManifest(
        name=str(data["name"]),
        version=str(data["version"]),
        description=str(data["description"]),
        permissions=permissions,
        entrypoint=str(data["entrypoint"]) if data.get("entrypoint") is not None else None,
        author=str(data["author"]) if data.get("author") is not None else None,
    )


def _max_risk(permissions: list[str]) -> SkillRisk:
    order = [SkillRisk.LOW, SkillRisk.MEDIUM, SkillRisk.HIGH, SkillRisk.BLOCKED]
    risk = SkillRisk.LOW
    for permission in permissions:
        current = PERMISSION_RISK.get(permission, SkillRisk.HIGH)
        if order.index(current) > order.index(risk):
            risk = current
    return risk


def review_manifest(path: Path) -> SkillReview:
    try:
        manifest = load_manifest(path)
    except (json.JSONDecodeError, ValueError) as exc:
        return SkillReview(path=str(path), valid=False, risk=SkillRisk.BLOCKED, messages=[str(exc)], manifest=None)

    messages: list[str] = []
    for permission in manifest.permissions:
        if permission not in PERMISSION_RISK:
            messages.append(f"Unknown permission defaults to high risk: {permission}")
        elif PERMISSION_RISK[permission] == SkillRisk.BLOCKED:
            messages.append(f"Blocked permission requested: {permission}")
        elif PERMISSION_RISK[permission] == SkillRisk.HIGH:
            messages.append(f"High-impact permission requested: {permission}")

    risk = _max_risk(manifest.permissions)
    valid = risk != SkillRisk.BLOCKED
    if not manifest.entrypoint:
        messages.append("No entrypoint declared. Skill can be cataloged but not executed.")
    return SkillReview(path=str(path), valid=valid, risk=risk, messages=messages, manifest=manifest.to_dict())


def review_skill_directory(root: Path) -> dict[str, Any]:
    root = root.resolve()
    manifests = sorted(root.rglob("skill.json")) + sorted(root.rglob("subreparo-skill.json"))
    reviews = [review_manifest(path) for path in manifests]
    return {
        "schema": "subreparo.skills.review.v1",
        "root": str(root),
        "skill_count": len(reviews),
        "blocked_count": sum(1 for review in reviews if review.risk == SkillRisk.BLOCKED),
        "high_risk_count": sum(1 for review in reviews if review.risk == SkillRisk.HIGH),
        "reviews": [review.to_dict() for review in reviews],
    }

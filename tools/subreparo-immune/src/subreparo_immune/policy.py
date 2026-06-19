from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .models import Finding, FindingType, Severity

POLICY_PATH = Path(".subreparo") / "policy.json"


@dataclass(frozen=True)
class LocalPolicy:
    allowed_hashes: set[str]
    blocked_hashes: set[str]
    ignored_targets: set[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed_hashes": sorted(self.allowed_hashes),
            "blocked_hashes": sorted(self.blocked_hashes),
            "ignored_targets": sorted(self.ignored_targets),
        }


def default_policy() -> LocalPolicy:
    return LocalPolicy(allowed_hashes=set(), blocked_hashes=set(), ignored_targets=set())


def load_policy(path: Path = POLICY_PATH) -> LocalPolicy:
    if not path.exists():
        return default_policy()
    data = json.loads(path.read_text(encoding="utf-8"))
    return LocalPolicy(
        allowed_hashes=set(data.get("allowed_hashes", [])),
        blocked_hashes=set(data.get("blocked_hashes", [])),
        ignored_targets=set(data.get("ignored_targets", [])),
    )


def save_policy(policy: LocalPolicy, path: Path = POLICY_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(policy.to_dict(), indent=2, sort_keys=True), encoding="utf-8")


def initialize_policy(path: Path = POLICY_PATH) -> Path:
    if not path.exists():
        save_policy(default_policy(), path)
    return path


def apply_policy(findings: list[Finding], policy: LocalPolicy) -> list[Finding]:
    filtered: list[Finding] = []
    for finding in findings:
        if finding.target in policy.ignored_targets:
            continue
        detail = finding.detail or ""
        blocked = next((value for value in policy.blocked_hashes if value and value in detail), None)
        allowed = next((value for value in policy.allowed_hashes if value and value in detail), None)
        if blocked:
            filtered.append(Finding(
                type=FindingType.IMMUNE_PATROL,
                severity=Severity.CRITICAL,
                target=finding.target,
                message="local policy blocked hash observed",
                recommendation="Keep this item isolated and review the source before restoring.",
                detail=finding.detail,
            ))
        elif not allowed:
            filtered.append(finding)
    return filtered

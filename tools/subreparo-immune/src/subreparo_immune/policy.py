from __future__ import annotations

import fnmatch
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .models import Finding, FindingType, Severity

POLICY_PATH = Path(".subreparo") / "policy.json"


@dataclass(frozen=True)
class LocalPolicy:
    allowed_hashes: set[str]
    blocked_hashes: set[str]
    ignored_targets: set[str]
    false_positive_targets: set[str] = field(default_factory=set)
    trusted_targets: set[str] = field(default_factory=set)

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed_hashes": sorted(self.allowed_hashes),
            "blocked_hashes": sorted(self.blocked_hashes),
            "ignored_targets": sorted(self.ignored_targets),
            "false_positive_targets": sorted(self.false_positive_targets),
            "trusted_targets": sorted(self.trusted_targets),
        }


def default_policy() -> LocalPolicy:
    return LocalPolicy(
        allowed_hashes=set(),
        blocked_hashes=set(),
        ignored_targets=set(),
        false_positive_targets=set(),
        trusted_targets=set(),
    )


def load_policy(path: Path = POLICY_PATH) -> LocalPolicy:
    if not path.exists():
        return default_policy()
    data = json.loads(path.read_text(encoding="utf-8"))
    return LocalPolicy(
        allowed_hashes=set(data.get("allowed_hashes", [])),
        blocked_hashes=set(data.get("blocked_hashes", [])),
        ignored_targets=set(data.get("ignored_targets", [])),
        false_positive_targets=set(data.get("false_positive_targets", [])),
        trusted_targets=set(data.get("trusted_targets", [])),
    )


def save_policy(policy: LocalPolicy, path: Path = POLICY_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(policy.to_dict(), indent=2, sort_keys=True), encoding="utf-8")


def initialize_policy(path: Path = POLICY_PATH) -> Path:
    if not path.exists():
        save_policy(default_policy(), path)
    return path


def add_allowed_hash(value: str, path: Path = POLICY_PATH) -> LocalPolicy:
    policy = load_policy(path)
    next_policy = LocalPolicy(
        allowed_hashes=policy.allowed_hashes | {value},
        blocked_hashes=policy.blocked_hashes - {value},
        ignored_targets=policy.ignored_targets,
        false_positive_targets=policy.false_positive_targets,
        trusted_targets=policy.trusted_targets,
    )
    save_policy(next_policy, path)
    return next_policy


def add_blocked_hash(value: str, path: Path = POLICY_PATH) -> LocalPolicy:
    policy = load_policy(path)
    next_policy = LocalPolicy(
        allowed_hashes=policy.allowed_hashes - {value},
        blocked_hashes=policy.blocked_hashes | {value},
        ignored_targets=policy.ignored_targets,
        false_positive_targets=policy.false_positive_targets,
        trusted_targets=policy.trusted_targets,
    )
    save_policy(next_policy, path)
    return next_policy


def add_ignored_target(value: str, path: Path = POLICY_PATH) -> LocalPolicy:
    policy = load_policy(path)
    next_policy = LocalPolicy(
        allowed_hashes=policy.allowed_hashes,
        blocked_hashes=policy.blocked_hashes,
        ignored_targets=policy.ignored_targets | {value},
        false_positive_targets=policy.false_positive_targets,
        trusted_targets=policy.trusted_targets,
    )
    save_policy(next_policy, path)
    return next_policy


def add_false_positive_target(value: str, path: Path = POLICY_PATH) -> LocalPolicy:
    policy = load_policy(path)
    next_policy = LocalPolicy(
        allowed_hashes=policy.allowed_hashes,
        blocked_hashes=policy.blocked_hashes,
        ignored_targets=policy.ignored_targets,
        false_positive_targets=policy.false_positive_targets | {value},
        trusted_targets=policy.trusted_targets | {value},
    )
    save_policy(next_policy, path)
    return next_policy


def add_trusted_target(value: str, path: Path = POLICY_PATH) -> LocalPolicy:
    policy = load_policy(path)
    next_policy = LocalPolicy(
        allowed_hashes=policy.allowed_hashes,
        blocked_hashes=policy.blocked_hashes,
        ignored_targets=policy.ignored_targets,
        false_positive_targets=policy.false_positive_targets,
        trusted_targets=policy.trusted_targets | {value},
    )
    save_policy(next_policy, path)
    return next_policy


def target_matches(target: str, patterns: set[str]) -> bool:
    return any(pattern == target or fnmatch.fnmatch(target, pattern) for pattern in patterns)


def apply_policy(findings: list[Finding], policy: LocalPolicy) -> list[Finding]:
    filtered: list[Finding] = []
    for finding in findings:
        if target_matches(finding.target, policy.ignored_targets):
            continue
        if target_matches(finding.target, policy.false_positive_targets):
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

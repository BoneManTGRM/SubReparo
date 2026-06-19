from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class RuleInfo:
    rule_id: str
    version: str
    name: str
    category: str
    description: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


RULES = [
    RuleInfo("SR-PATROL-001", "1.0.0", "Encoded command", "process/script", "Detects encoded shell command usage."),
    RuleInfo("SR-PATROL-002", "1.0.0", "Download and run", "process/script", "Detects direct download-to-execution patterns."),
    RuleInfo("SR-PATROL-003", "1.0.0", "Hidden execution", "process/script", "Detects hidden or script-host execution behavior."),
    RuleInfo("SR-PATROL-004", "1.0.0", "Startup script", "persistence", "Detects scripts or executables in startup locations."),
    RuleInfo("SR-PATROL-005", "1.0.0", "Browser sensitive permissions", "browser", "Detects sensitive browser extension permissions."),
    RuleInfo("SR-PATROL-006", "1.0.0", "Launcher review", "launcher", "Detects risky launcher or shortcut content."),
    RuleInfo("SR-PATROL-007", "1.0.0", "Baseline new watched file", "integrity", "Detects new watched files after baseline."),
    RuleInfo("SR-PATROL-008", "1.0.0", "Baseline changed watched file", "integrity", "Detects changed watched files after baseline."),
    RuleInfo("SR-PATROL-009", "1.0.0", "Process behavior", "runtime", "Detects suspicious running process command lines."),
    RuleInfo("SR-PATROL-010", "1.0.0", "Network review", "runtime", "Detects unusual external connection signals."),
]


def rule_catalog() -> list[dict[str, Any]]:
    return [rule.to_dict() for rule in RULES]

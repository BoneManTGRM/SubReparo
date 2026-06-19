from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .cortex_models import ApprovalLevel, CortexTask

QUEUE_PATH = Path(".subreparo") / "approval_queue.jsonl"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ApprovalRequest:
    created_at: str
    task: dict[str, Any]
    approval_level: str
    reason: str
    status: str = "pending"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def enqueue_approval(task: CortexTask, approval_level: ApprovalLevel, reason: str, path: Path = QUEUE_PATH) -> ApprovalRequest:
    request = ApprovalRequest(
        created_at=now(),
        task=task.to_dict(),
        approval_level=approval_level.value,
        reason=reason,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(request.to_dict(), sort_keys=True) + "\n")
    return request


def list_approvals(path: Path = QUEUE_PATH) -> list[ApprovalRequest]:
    if not path.exists():
        return []
    requests: list[ApprovalRequest] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        requests.append(ApprovalRequest(**json.loads(line)))
    return requests


def pending_approvals(path: Path = QUEUE_PATH) -> list[ApprovalRequest]:
    return [request for request in list_approvals(path) if request.status == "pending"]

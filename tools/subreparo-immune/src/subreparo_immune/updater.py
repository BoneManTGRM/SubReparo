from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import __version__

UPDATE_SCHEMA = "subreparo.update_plan.v1"
UPDATE_PLAN = Path(".subreparo") / "update_plan.json"


def build_update_plan(target_version: str | None = None) -> dict[str, Any]:
    requested = target_version or __version__
    is_current = requested == __version__
    return {
        "schema": UPDATE_SCHEMA,
        "current_version": __version__,
        "target_version": requested,
        "status": "current" if is_current else "approval_required",
        "auto_apply_default": False,
        "network_lookup_default": False,
        "steps": [
            "review release notes",
            "run local tests",
            "build package artifact",
            "verify report signatures",
            "apply only after operator approval",
        ],
        "safety": {
            "dry_run_by_default": True,
            "requires_manual_approval": True,
            "does_not_replace_running_installation": True,
        },
    }


def write_update_plan(root: Path, target_version: str | None = None) -> Path:
    root = root.resolve()
    path = root / UPDATE_PLAN
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(build_update_plan(target_version), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return path

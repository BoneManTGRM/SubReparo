from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SETUP_PROFILE_PATH = Path(".subreparo") / "setup_profile.json"
SCHEMA = "subreparo.setup_profile.v1"
VALID_MODES = {"simple", "expert", "paranoid", "developer", "family"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class SetupProfile:
    mode: str
    watched_paths: tuple[str, ...]
    dashboard_host: str
    dashboard_port: int
    local_only: bool
    scan_on_start: bool
    approval_gate_high_impact: bool
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["schema"] = SCHEMA
        data["watched_paths"] = list(self.watched_paths)
        return data


def default_watched_paths(root: Path) -> tuple[str, ...]:
    root = root.resolve()
    candidates = [root]
    home = Path.home()
    for name in ("Downloads", "Desktop", "Documents"):
        path = home / name
        if path.exists():
            candidates.append(path)
    return tuple(str(path) for path in candidates)


def create_setup_profile(
    root: Path,
    mode: str = "simple",
    watched_paths: list[str] | None = None,
    dashboard_host: str = "127.0.0.1",
    dashboard_port: int = 8765,
) -> SetupProfile:
    if mode not in VALID_MODES:
        raise ValueError(f"Unknown setup mode: {mode}")
    if dashboard_host not in {"127.0.0.1", "localhost"}:
        raise ValueError("Setup keeps the dashboard bound to localhost by default.")
    root = root.resolve()
    paths = tuple(watched_paths) if watched_paths else default_watched_paths(root)
    profile = SetupProfile(
        mode=mode,
        watched_paths=paths,
        dashboard_host=dashboard_host,
        dashboard_port=dashboard_port,
        local_only=True,
        scan_on_start=True,
        approval_gate_high_impact=True,
        created_at=now(),
    )
    state = root / ".subreparo"
    state.mkdir(parents=True, exist_ok=True)
    (state / "setup_profile.json").write_text(
        json.dumps(profile.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return profile


def load_setup_profile(root: Path) -> SetupProfile | None:
    path = root.resolve() / SETUP_PROFILE_PATH
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return SetupProfile(
        mode=data.get("mode", "simple"),
        watched_paths=tuple(data.get("watched_paths", [])),
        dashboard_host=data.get("dashboard_host", "127.0.0.1"),
        dashboard_port=int(data.get("dashboard_port", 8765)),
        local_only=bool(data.get("local_only", True)),
        scan_on_start=bool(data.get("scan_on_start", True)),
        approval_gate_high_impact=bool(data.get("approval_gate_high_impact", True)),
        created_at=data.get("created_at", now()),
    )

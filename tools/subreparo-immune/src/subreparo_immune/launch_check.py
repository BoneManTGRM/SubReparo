from __future__ import annotations

from pathlib import Path
from typing import Any


def build_launch_check(root: Path) -> dict[str, Any]:
    root = root.resolve()
    scripts = {
        "unix": root / "scripts" / "start-subreparo-control-center.sh",
        "macos_double_click": root / "scripts" / "start-subreparo-control-center.command",
        "windows_cmd": root / "scripts" / "start-subreparo-control-center.cmd",
    }
    docs = {
        "launch_guide": root / "subreparo" / "docs" / "CONTROL_CENTER_LAUNCH.md",
        "desktop_vision": root / "subreparo" / "docs" / "DESKTOP_APP_VISION.md",
    }
    return {
        "schema": "subreparo.control_center_launch_check.v1",
        "url": "http://127.0.0.1:8765",
        "localhost_only": True,
        "scripts": {
            name: {
                "path": str(path.relative_to(root)),
                "present": path.exists(),
            }
            for name, path in scripts.items()
        },
        "docs": {
            name: {
                "path": str(path.relative_to(root)),
                "present": path.exists(),
            }
            for name, path in docs.items()
        },
        "manual_commands": [
            "cd tools/subreparo-immune",
            "python -m pip install -e .",
            "cd ../..",
            "subreparo-immune dashboard",
        ],
    }

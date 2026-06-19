from __future__ import annotations

import argparse
import json
from pathlib import Path

from .installer_manifest import VALID_PLATFORMS, build_installer_manifest, write_installer_manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="subreparo-installer", description="Show SubReparo installer packaging manifest.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--platform", choices=("all",) + VALID_PLATFORMS, default="all")
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def selected_platforms(value: str) -> list[str] | None:
    if value == "all":
        return None
    return [value]


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.path).resolve()
    platforms = selected_platforms(args.platform)
    payload = build_installer_manifest(platforms)
    if args.write_manifest:
        payload["written_to"] = str(write_installer_manifest(root, platforms))
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("SubReparo Installer Manifest")
        print("============================")
        print(f"Version: {payload['version']}")
        print(f"Platforms: {payload['platform_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

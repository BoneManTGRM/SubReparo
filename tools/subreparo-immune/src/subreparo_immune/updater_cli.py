from __future__ import annotations

import argparse
import json
from pathlib import Path

from .updater import build_update_plan, write_update_plan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="subreparo-updater",
        description="Show SubReparo update plan scaffold.",
    )
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--target-version")
    parser.add_argument("--write-plan", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.path).resolve()
    payload = build_update_plan(args.target_version)
    if args.write_plan:
        payload["written_to"] = str(write_update_plan(root, args.target_version))
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("SubReparo Update Plan")
        print("=====================")
        print(f"Current: {payload['current_version']}")
        print(f"Target: {payload['target_version']}")
        print(f"Status: {payload['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

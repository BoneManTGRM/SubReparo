from __future__ import annotations

import argparse
import json
from pathlib import Path

from .fleet_dashboard import build_fleet_dashboard, write_fleet_dashboard


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="subreparo-fleet",
        description="Show local SubReparo fleet dashboard scaffold.",
    )
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--write-dashboard", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.path).resolve()
    payload = build_fleet_dashboard(root)
    if args.write_dashboard:
        payload["written_to"] = str(write_fleet_dashboard(root))
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("SubReparo Fleet Dashboard")
        print("=========================")
        print(f"Nodes: {payload['totals']['nodes']}")
        print(f"Alerts: {payload['totals']['alerts']}")
        print(f"Approvals: {payload['totals']['approvals']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

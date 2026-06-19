from __future__ import annotations

import argparse
import json
from pathlib import Path

from .alerts import append_alert_inbox, build_native_alert_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="subreparo-alerts",
        description="Show local SubReparo alert plans.",
    )
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--write-inbox", action="store_true", help="Save previewed alert plans in local state.")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.path).resolve()
    payload = build_native_alert_report(root, limit=args.limit)
    if args.write_inbox and payload["plans"]:
        path = append_alert_inbox(root, list(payload["plans"]))
        payload["written_to"] = str(path)

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("SubReparo Alerts")
        print("===============")
        print(f"Platform: {payload['platform']}")
        print(f"Pending plans: {payload['pending_plan_count']}")
        print(f"Inbox records: {payload['inbox_count']}")
        print("Local preview mode is the default.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

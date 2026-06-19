from __future__ import annotations

import argparse
import json
from pathlib import Path

from .tray_app import build_tray_manifest, write_tray_manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="subreparo-tray",
        description="Show SubReparo desktop tray manifest.",
    )
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--dashboard-url", default="http://127.0.0.1:8765")
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.path).resolve()
    payload = build_tray_manifest(root, dashboard_url=args.dashboard_url)
    if args.write_manifest:
        path = write_tray_manifest(root, dashboard_url=args.dashboard_url)
        payload["written_to"] = str(path)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("SubReparo Tray")
        print("==============")
        print(f"Dashboard: {payload['dashboard_url']}")
        print(f"Menu items: {len(payload['menu_items'])}")
        print(f"Alert inbox records: {payload['status']['alert_inbox_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

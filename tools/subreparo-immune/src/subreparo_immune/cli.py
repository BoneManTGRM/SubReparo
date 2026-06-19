from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import run_local


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="subreparo-immune",
        description="Local-first repair-memory engine for SubReparo.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run SubReparo checks once.")
    run_parser.add_argument("path", nargs="?", default=".")
    run_parser.add_argument("--website", action="append", default=[])
    run_parser.add_argument("--json", action="store_true")

    init_parser = subparsers.add_parser("init", help="Initialize local SubReparo state.")
    init_parser.add_argument("path", nargs="?", default=".")

    return parser


def command_run(args: argparse.Namespace) -> int:
    result = run_local(Path(args.path), websites=args.website)
    payload = result.to_dict()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        score = payload["score"]
        print(f"SubReparo score: {score['value']}/100 ({score['grade']})")
        print(f"Findings: {score['findings']}")
        print(f"Action: {score['action']}")
        print(f"Report: {payload['report_path']}")
        print(f"Export: {payload['export_path']}")
    return 0 if payload["score"]["value"] >= 70 else 2


def command_init(args: argparse.Namespace) -> int:
    root = Path(args.path)
    state = root / ".subreparo"
    state.mkdir(parents=True, exist_ok=True)
    (state / "README.md").write_text(
        "# SubReparo local state\n\nThis folder stores local reports, ledger entries, and chain export payloads.\n",
        encoding="utf-8",
    )
    print(f"Initialized SubReparo local state at {state}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "run":
        return command_run(args)
    if args.command == "init":
        return command_init(args)
    parser.error(f"Unknown command: {args.command}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

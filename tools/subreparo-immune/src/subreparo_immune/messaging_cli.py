from __future__ import annotations

import argparse
import json

from .messaging_connectors import build_message_plan, messaging_status


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="subreparo-messaging",
        description="Inspect Telegram/WhatsApp connector readiness and build approval-gated message plans.",
    )
    parser.add_argument("--status", action="store_true", help="Show connector configuration status.")
    parser.add_argument("--plan-message", action="store_true", help="Build a message plan without sending.")
    parser.add_argument("--channel", choices=["telegram", "whatsapp"])
    parser.add_argument("--recipient")
    parser.add_argument("--text")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.plan_message:
        if not args.channel or not args.recipient or not args.text:
            payload = {
                "allowed": False,
                "reason": "--channel, --recipient, and --text are required for --plan-message.",
            }
            exit_code = 2
        else:
            payload = build_message_plan(args.channel, args.recipient, args.text)
            exit_code = 0 if payload.get("allowed") else 2
    else:
        payload = messaging_status()
        exit_code = 0

    print(json.dumps(payload, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

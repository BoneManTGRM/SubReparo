from __future__ import annotations

import argparse
import json

from .dashboard import serve
from .mobile_preview import build_mobile_preview_plan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="subreparo-mobile-preview",
        description="Start a token-gated same-Wi-Fi preview for phone or tablet viewing.",
    )
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--token", help="Optional custom token. If omitted, a random token is generated.")
    parser.add_argument("--json", action="store_true", help="Print the preview plan and exit without starting the server.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    plan = build_mobile_preview_plan(port=args.port, token=args.token)
    if args.json:
        print(json.dumps(plan.to_dict(), indent=2, sort_keys=True))
        return 0

    print("SubReparo mobile preview")
    print("========================")
    print(f"Open this on your iPhone: {plan.phone_url}")
    print("")
    for note in plan.safety_notes:
        print(f"- {note}")
    print("")
    serve(host=plan.host, port=plan.port, mobile_preview=True, token=plan.token)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

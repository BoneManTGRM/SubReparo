from __future__ import annotations

import argparse
import json

from .modes import mode_catalog


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="subreparo-modes", description="Show SubReparo user mode profiles.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = mode_catalog()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("SubReparo modes")
        print("===============")
        for mode in payload:
            print(f"- {mode['name']}: {mode['description']} min={mode['min_severity']} limit={mode['finding_limit']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

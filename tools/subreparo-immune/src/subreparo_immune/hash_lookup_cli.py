from __future__ import annotations

import argparse
import json
from pathlib import Path

from .hash_lookup import build_hash_lookup


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="subreparo-hash-lookup",
        description="Create a hash-only lookup export for local review.",
    )
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--suffix", action="append", default=[], help="Limit hashing to this file suffix.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    suffixes = {item.lower() if item.startswith(".") else f".{item.lower()}" for item in args.suffix}
    payload = build_hash_lookup(Path(args.path), suffixes=suffixes or None)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

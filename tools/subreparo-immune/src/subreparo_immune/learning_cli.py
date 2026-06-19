from __future__ import annotations

import argparse
import json
from pathlib import Path

from .learning_profile import build_learning_profile


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="subreparo-learning",
        description="Build a local per-device learning profile.",
    )
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    payload = build_learning_profile(Path(args.path))
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

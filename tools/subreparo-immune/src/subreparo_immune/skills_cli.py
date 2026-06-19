from __future__ import annotations

import argparse
import json
from pathlib import Path

from .skills import review_manifest, review_skill_directory


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="subreparo-skills", description="Review SubReparo skill/plugin manifests without executing them.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--manifest", help="Review one skill manifest file.")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.manifest:
        review = review_manifest(Path(args.manifest))
        payload = review.to_dict()
        exit_code = 0 if review.valid else 2
    else:
        payload = review_skill_directory(Path(args.path))
        exit_code = 0 if payload["blocked_count"] == 0 else 2

    print(json.dumps(payload, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

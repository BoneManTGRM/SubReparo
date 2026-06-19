from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from .baseline import compare
from .immune_patrol import patrol
from .scoring import calculate_score


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="subreparo-monitor", description="Continuously monitor local SubReparo signals.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--interval", type=int, default=10)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--once", action="store_true")
    return parser


def signal_key(item: dict[str, str]) -> str:
    return f"{item.get('severity')}|{item.get('type')}|{item.get('target')}|{item.get('message')}"


def run_once(root: Path) -> dict[str, object]:
    findings = patrol(root) + compare(root)
    score = calculate_score(findings)
    return {
        "score": score.to_dict(),
        "findings": [finding.to_dict() for finding in findings],
    }


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.path).resolve()
    seen: set[str] = set()

    while True:
        payload = run_once(root)
        findings = payload["findings"]
        new_items = [item for item in findings if signal_key(item) not in seen]
        for item in findings:
            seen.add(signal_key(item))

        if args.json:
            print(json.dumps({"new_findings": new_items, "score": payload["score"]}, indent=2, sort_keys=True))
        else:
            if new_items:
                print("SubReparo monitor detected new items")
                for item in new_items:
                    print(f"- [{item['severity'].upper()}] {item['message']} at {item['target']}")
                    print(f"  {item['recommendation']}")
            else:
                print("SubReparo monitor: no new items")
        if args.once:
            return 0
        time.sleep(max(5, args.interval))


if __name__ == "__main__":
    raise SystemExit(main())

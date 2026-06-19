from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from .baseline import compare
from .immune_patrol import patrol
from .process_scan import scan_processes
from .scoring import calculate_score
from .watcher import build_watch_plan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="subreparo-monitor", description="Continuously monitor local SubReparo signals.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--interval", type=int, default=10)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--all-targets", action="store_true", help="Monitor configured watch-plan targets.")
    return parser


def signal_key(item: dict[str, str]) -> str:
    return f"{item.get('severity')}|{item.get('type')}|{item.get('target')}|{item.get('message')}"


def _target_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    seen: set[str] = set()
    for target in build_watch_plan(root).get("targets", []):
        if not isinstance(target, dict) or target.get("kind") == "process":
            continue
        if not target.get("exists"):
            continue
        path = Path(str(target.get("path", ""))).expanduser()
        if not path.exists() or not path.is_dir():
            continue
        key = str(path.resolve())
        if key not in seen:
            seen.add(key)
            paths.append(path)
    return paths


def run_once(root: Path, all_targets: bool = False) -> dict[str, object]:
    findings = patrol(root) + compare(root)
    monitored_targets: list[dict[str, Any]] = []
    if all_targets:
        for target in _target_paths(root):
            monitored_targets.append({"path": str(target), "kind": "filesystem"})
            findings.extend(patrol(target))
        monitored_targets.append({"path": "process-table", "kind": "process"})
        findings.extend(scan_processes())
    score = calculate_score(findings)
    return {
        "score": score.to_dict(),
        "findings": [finding.to_dict() for finding in findings],
        "monitored_targets": monitored_targets,
    }


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.path).resolve()
    seen: set[str] = set()

    while True:
        payload = run_once(root, all_targets=args.all_targets)
        findings = payload["findings"]
        new_items = [item for item in findings if signal_key(item) not in seen]
        for item in findings:
            seen.add(signal_key(item))

        if args.json:
            print(json.dumps({
                "new_findings": new_items,
                "score": payload["score"],
                "monitored_targets": payload["monitored_targets"],
            }, indent=2, sort_keys=True))
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

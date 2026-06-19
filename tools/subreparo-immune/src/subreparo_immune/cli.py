from __future__ import annotations

import argparse
import json
from pathlib import Path

from .baseline import compare, write_baseline
from .dashboard import serve
from .engine import run_local
from .immune_patrol import patrol
from .models import Severity
from .quarantine import list_records, restore_all, restore_record, stage_file
from .scoring import calculate_score
from .swarm import flatten, run_swarm


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

    doctor_parser = subparsers.add_parser("doctor", help="Run a user-friendly full local review.")
    doctor_parser.add_argument("path", nargs="?", default=".")
    doctor_parser.add_argument("--website", action="append", default=[])
    doctor_parser.add_argument("--json", action="store_true")

    patrol_parser = subparsers.add_parser("patrol", help="Inspect local files for suspicious immune signals.")
    patrol_parser.add_argument("path", nargs="?", default=".")
    patrol_parser.add_argument("--json", action="store_true")

    baseline_parser = subparsers.add_parser("baseline", help="Create a local integrity baseline.")
    baseline_parser.add_argument("path", nargs="?", default=".")

    diff_parser = subparsers.add_parser("diff", help="Compare current files against the local baseline.")
    diff_parser.add_argument("path", nargs="?", default=".")
    diff_parser.add_argument("--json", action="store_true")

    isolate_parser = subparsers.add_parser("isolate", help="Move high-risk local findings into SubReparo staging.")
    isolate_parser.add_argument("path", nargs="?", default=".")
    isolate_parser.add_argument("--apply", action="store_true", help="Apply staging. Without this flag, only prints the plan.")
    isolate_parser.add_argument("--json", action="store_true")

    q_parser = subparsers.add_parser("quarantine", help="List or restore staged files.")
    q_parser.add_argument("path", nargs="?", default=".")
    q_parser.add_argument("--restore-index", type=int)
    q_parser.add_argument("--restore-all", action="store_true")
    q_parser.add_argument("--json", action="store_true")

    review_parser = subparsers.add_parser("review", help="Run all local analyzer groups.")
    review_parser.add_argument("path", nargs="?", default=".")
    review_parser.add_argument("--website", action="append", default=[])
    review_parser.add_argument("--json", action="store_true")

    dashboard_parser = subparsers.add_parser("dashboard", help="Start the local dashboard.")
    dashboard_parser.add_argument("--host", default="127.0.0.1")
    dashboard_parser.add_argument("--port", type=int, default=8765)

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


def command_doctor(args: argparse.Namespace) -> int:
    result = run_local(Path(args.path), websites=args.website)
    payload = result.to_dict()
    score = payload["score"]
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("SubReparo Doctor")
        print("================")
        print(f"Score: {score['value']}/100 ({score['grade']})")
        print(f"Findings: {score['findings']}")
        print(f"Action: {score['action']}")
        print("")
        if payload["findings"]:
            print("Top findings:")
            for finding in payload["findings"][:8]:
                print(f"- [{finding['severity'].upper()}] {finding['type']} at {finding['target']}")
                print(f"  {finding['recommendation']}")
        else:
            print("No project signals detected.")
        print("")
        print(f"Report: {payload['report_path']}")
        print("Dashboard: subreparo-immune dashboard")
    return 0 if score["value"] >= 70 else 2


def command_patrol(args: argparse.Namespace) -> int:
    findings = patrol(Path(args.path))
    score = calculate_score(findings)
    payload = {"score": score.to_dict(), "findings": [finding.to_dict() for finding in findings]}
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("SubReparo Immune Patrol")
        print("=======================")
        print(f"Score: {score.value}/100 ({score.grade})")
        print(f"Findings: {score.findings}")
        for finding in findings[:12]:
            print(f"- [{finding.severity.value.upper()}] {finding.message} at {finding.target}")
            print(f"  {finding.recommendation}")
    return 0 if score.value >= 70 else 2


def command_baseline(args: argparse.Namespace) -> int:
    path = write_baseline(Path(args.path))
    print(f"SubReparo baseline saved at {path}")
    return 0


def command_diff(args: argparse.Namespace) -> int:
    findings = compare(Path(args.path))
    score = calculate_score(findings)
    payload = {"score": score.to_dict(), "findings": [finding.to_dict() for finding in findings]}
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("SubReparo Baseline Diff")
        print("=======================")
        print(f"Score: {score.value}/100 ({score.grade})")
        print(f"Findings: {score.findings}")
        for finding in findings[:12]:
            print(f"- [{finding.severity.value.upper()}] {finding.message} at {finding.target}")
            print(f"  {finding.recommendation}")
    return 0 if score.value >= 70 else 2


def _file_from_finding(root: Path, target: str) -> Path | None:
    raw = target.split(":", 1)[0]
    candidate = (root / raw).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate if candidate.exists() and candidate.is_file() else None


def command_isolate(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    findings = [finding for finding in patrol(root) if finding.severity in {Severity.HIGH, Severity.CRITICAL}]
    actions = []
    for finding in findings:
        path = _file_from_finding(root, finding.target)
        if path is None:
            actions.append({"target": finding.target, "status": "manual_review", "reason": finding.message})
            continue
        if args.apply:
            record = stage_file(root, path, reason=finding.message, state_dir=root / ".subreparo")
            actions.append({"target": finding.target, "status": "staged", "staged_path": record.staged_path})
        else:
            actions.append({"target": finding.target, "status": "planned", "reason": finding.message})
    if args.json:
        print(json.dumps({"actions": actions}, indent=2, sort_keys=True))
    else:
        print("SubReparo Isolation Plan" if not args.apply else "SubReparo Isolation Applied")
        print("========================")
        if not actions:
            print("No high-risk local findings found.")
        for action in actions:
            print(f"- {action['status']}: {action['target']}")
            if "staged_path" in action:
                print(f"  Staged at: {action['staged_path']}")
    return 0


def command_quarantine(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    state_dir = root / ".subreparo"
    if args.restore_all:
        restored = restore_all(root, state_dir=state_dir)
        payload = {"restored": [record.to_dict() for record in restored]}
    elif args.restore_index is not None:
        record = restore_record(root, args.restore_index, state_dir=state_dir)
        payload = {"restored": [record.to_dict()]}
    else:
        records = list_records(state_dir)
        payload = {"records": [record.to_dict() for record in records]}

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif "records" in payload:
        print("SubReparo Quarantine")
        print("====================")
        if not payload["records"]:
            print("No staged files found.")
        for index, record in enumerate(payload["records"]):
            print(f"[{index}] {record['staged_path']}")
            print(f"  Original: {record['original_path']}")
            print(f"  Reason: {record['reason']}")
    else:
        print("SubReparo restore complete")
        for record in payload["restored"]:
            print(f"- Restored: {record['original_path']}")
    return 0


def command_review(args: argparse.Namespace) -> int:
    results = run_swarm(Path(args.path), websites=args.website)
    findings = flatten(results)
    score = calculate_score(findings)
    payload = {
        "score": score.to_dict(),
        "analyzers": [result.to_dict() for result in results],
        "findings": [finding.to_dict() for finding in findings],
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("SubReparo Review")
        print("================")
        print(f"Score: {score.value}/100 ({score.grade})")
        print(f"Findings: {score.findings}")
        for result in results:
            print(f"- {result.analyzer}: {len(result.findings)} finding(s)")
    return 0 if score.value >= 70 else 2


def command_dashboard(args: argparse.Namespace) -> int:
    serve(host=args.host, port=args.port)
    return 0


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
    if args.command == "doctor":
        return command_doctor(args)
    if args.command == "patrol":
        return command_patrol(args)
    if args.command == "baseline":
        return command_baseline(args)
    if args.command == "diff":
        return command_diff(args)
    if args.command == "isolate":
        return command_isolate(args)
    if args.command == "quarantine":
        return command_quarantine(args)
    if args.command == "review":
        return command_review(args)
    if args.command == "dashboard":
        return command_dashboard(args)
    if args.command == "init":
        return command_init(args)
    parser.error(f"Unknown command: {args.command}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

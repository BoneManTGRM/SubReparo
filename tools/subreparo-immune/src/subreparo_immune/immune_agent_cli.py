from __future__ import annotations

import argparse
import json
from pathlib import Path

from .agent_core import read_scar_memory, run_agent_cycle
from .agent_proofs import build_agent_proof_export, write_agent_proof_export
from .clawdbot_backend import handle_clawdbot_goal


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="subreparo-immune-agent",
        description="Run the SubReparo Immune agent core prototype.",
    )
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--cycle", help="Run one observe-detect-plan-repair-verify cycle for a goal.")
    parser.add_argument("--scars", action="store_true", help="Show scar and ledger memory.")
    parser.add_argument("--proof", action="store_true", help="Show latest proof export payload.")
    parser.add_argument("--write-proof", action="store_true", help="Write latest proof export payload.")
    parser.add_argument("--bot-backend", help="Return a bot/frontend backend payload for a goal.")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.path).resolve()
    if args.cycle:
        payload = run_agent_cycle(root, goal=args.cycle)
    elif args.scars:
        payload = read_scar_memory(root)
    elif args.write_proof:
        path = write_agent_proof_export(root)
        payload = {"path": str(path), "proof": build_agent_proof_export(root)}
    elif args.proof:
        payload = build_agent_proof_export(root)
    elif args.bot_backend:
        payload = handle_clawdbot_goal(root, args.bot_backend)
    else:
        payload = {
            "message": "Use --cycle, --scars, --proof, --write-proof, or --bot-backend.",
            "commands": [
                "python -m subreparo_immune.immune_agent_cli . --cycle 'self-heal project' --json",
                "python -m subreparo_immune.immune_agent_cli . --scars --json",
                "python -m subreparo_immune.immune_agent_cli . --proof --json",
                "python -m subreparo_immune.immune_agent_cli . --bot-backend 'self-heal project' --json",
            ],
        }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

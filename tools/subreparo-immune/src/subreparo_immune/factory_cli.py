from __future__ import annotations

import argparse
import json
from pathlib import Path

from .agent_factory import (
    build_agent_manifest,
    create_agent_from_blueprint,
    list_blueprints,
    list_registered_agents,
    review_agent_manifest,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="subreparo-factory",
        description="Create reviewed SubReparo agent manifests and local scaffolds.",
    )
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--blueprints", action="store_true", help="List available agent blueprints.")
    parser.add_argument("--manifest", help="Build a manifest for a blueprint without writing files.")
    parser.add_argument("--create", help="Create a local scaffold for a blueprint.")
    parser.add_argument("--name", help="Override the agent name.")
    parser.add_argument("--purpose", help="Override the agent purpose.")
    parser.add_argument("--register", action="store_true", help="Add a reviewed record to the local registry.")
    parser.add_argument("--registry", action="store_true", help="List local registry records.")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.path).resolve()
    if args.blueprints:
        payload = {"blueprints": list_blueprints()}
    elif args.manifest:
        manifest = build_agent_manifest(args.manifest, name=args.name, purpose=args.purpose)
        payload = {"manifest": manifest, "review": review_agent_manifest(manifest)}
    elif args.create:
        payload = create_agent_from_blueprint(
            root,
            args.create,
            name=args.name,
            purpose=args.purpose,
            register=args.register,
        )
    elif args.registry:
        payload = {"registry": list_registered_agents(root)}
    else:
        payload = {
            "message": "Use --blueprints, --manifest, --create, or --registry.",
            "commands": [
                "subreparo-factory . --blueprints --json",
                "subreparo-factory . --manifest code_review --json",
                "subreparo-factory . --create code_review --register --json",
                "subreparo-factory . --registry --json",
            ],
        }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

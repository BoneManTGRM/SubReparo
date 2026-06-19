from __future__ import annotations

import argparse
import json
from pathlib import Path

from .dependency_risk import scan_dependency_risk
from .sbom import generate_sbom, write_sbom


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="subreparo-sbom", description="Generate SubReparo SBOM-style inventory.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--output")
    parser.add_argument("--risk", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    root = Path(args.path)
    if args.risk:
        findings = scan_dependency_risk(root)
        payload = {"findings": [finding.to_dict() for finding in findings]}
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if not findings else 2

    if args.output:
        target = write_sbom(root, output=Path(args.output))
        print(f"SubReparo SBOM saved at {target}")
    else:
        payload = generate_sbom(root)
        if args.json:
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print(f"SubReparo SBOM components: {payload['component_count']}")
            for component in payload["components"]:
                print(f"- {component['ecosystem']} {component['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

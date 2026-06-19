from __future__ import annotations

import argparse
import json
from pathlib import Path

from .quarantine import list_records, remove_staged_record, restore_all, restore_record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="subreparo-quarantine", description="Manage SubReparo staged files.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--restore-index", type=int)
    parser.add_argument("--restore-all", action="store_true")
    parser.add_argument("--remove-index", type=int, help="Remove a staged file from SubReparo staging only.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    root = Path(args.path).resolve()
    state = root / ".subreparo"
    if args.restore_all:
        payload = {"restored": [record.to_dict() for record in restore_all(root, state_dir=state)]}
    elif args.restore_index is not None:
        payload = {"restored": [restore_record(root, args.restore_index, state_dir=state).to_dict()]}
    elif args.remove_index is not None:
        payload = {"removed_from_staging": [remove_staged_record(root, args.remove_index, state_dir=state).to_dict()]}
    else:
        payload = {"records": [record.to_dict() for record in list_records(state)]}

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

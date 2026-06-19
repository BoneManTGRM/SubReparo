from __future__ import annotations

import argparse
import json
from pathlib import Path

from .network_memory import build_network_memory


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="subreparo-network-memory",
        description="Summarize local domain and network observation memory.",
    )
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = build_network_memory(Path(args.path))
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

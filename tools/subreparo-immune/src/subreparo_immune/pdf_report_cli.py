from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pdf_report import create_pdf_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="subreparo-pdf-report",
        description="Create a local PDF copy of the SubReparo markdown report.",
    )
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = create_pdf_report(Path(args.path))
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

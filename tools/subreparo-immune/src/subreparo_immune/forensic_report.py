from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .redaction import redact_text

FORENSIC_REPORT_PATH = Path(".subreparo") / "forensic_report.md"
SCHEMA = "subreparo.forensic_report.v1"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read(path: Path, fallback: str = "Not available.") -> str:
    if not path.exists():
        return fallback
    return path.read_text(encoding="utf-8", errors="replace")


def _tail_jsonl(path: Path, limit: int = 10) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    lines = [line for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()]
    for line in lines[-limit:]:
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"unreadable": line})
    return rows


def build_forensic_report(root: Path) -> dict[str, Any]:
    root = root.resolve()
    state = root / ".subreparo"
    generated_at = now()
    report = _read(state / "report.md")
    trust = _read(state / "trust_report.json")
    signature = _read(state / "report_signature.json")
    audit_tail = _tail_jsonl(state / "audit.jsonl")
    ledger_tail = _tail_jsonl(state / "repair_ledger.jsonl")

    lines = [
        "# SubReparo Expert Forensic Report",
        "",
        f"Generated: {generated_at}",
        f"Project: `{redact_text(str(root))}`",
        "",
        "## Scope",
        "",
        "This report is local-first and defensive. It summarizes local SubReparo evidence without destructive action.",
        "",
        "## Executive summary source",
        "",
        "```markdown",
        redact_text(report[:6000]),
        "```",
        "",
        "## Trust report",
        "",
        "```json",
        redact_text(trust[:6000]),
        "```",
        "",
        "## Report signature",
        "",
        "```json",
        redact_text(signature[:4000]),
        "```",
        "",
        "## Recent repair ledger records",
        "",
        "```json",
        redact_text(json.dumps(ledger_tail, indent=2, sort_keys=True)[:6000]),
        "```",
        "",
        "## Recent audit records",
        "",
        "```json",
        redact_text(json.dumps(audit_tail, indent=2, sort_keys=True)[:6000]),
        "```",
        "",
        "## Handling notes",
        "",
        "- Preserve `.subreparo` evidence before making high-impact changes.",
        "- Use quarantine restore instead of deletion when possible.",
        "- Submit only digests or summaries to chain-backed records.",
    ]
    state.mkdir(parents=True, exist_ok=True)
    path = state / "forensic_report.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "schema": SCHEMA,
        "generated_at": generated_at,
        "path": str(path),
        "audit_records_included": len(audit_tail),
        "ledger_records_included": len(ledger_tail),
    }

from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from .redaction import redact_text

SAFE_FILES = {
    "report.md": "report.md",
    "chain_export.json": "chain_export.json",
    "repair_ledger.jsonl": "repair_ledger.jsonl",
    "quarantine_manifest.jsonl": "quarantine_manifest.jsonl",
    "audit.jsonl": "audit.jsonl",
    "watch_alerts.jsonl": "watch_alerts.jsonl",
}


def create_bundle(root: Path, output: Path | None = None) -> Path:
    root = root.resolve()
    state = root / ".subreparo"
    bundle = output or state / "incident_bundle.zip"
    bundle.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(bundle, "w", ZIP_DEFLATED) as archive:
        for filename, archive_name in SAFE_FILES.items():
            path = state / filename
            if not path.exists() or not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            archive.writestr(archive_name, redact_text(text))
    return bundle

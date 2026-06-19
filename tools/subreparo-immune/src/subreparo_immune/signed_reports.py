from __future__ import annotations

import hashlib
import hmac
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SIGNATURE_PATH = Path(".subreparo") / "report_signature.json"
SCHEMA = "subreparo.report_signature.v1"
DEFAULT_ARTIFACTS = (
    ".subreparo/report.md",
    ".subreparo/chain_export.json",
    ".subreparo/repair_ledger.jsonl",
    ".subreparo/quality_report.json",
    ".subreparo/trust_report.json",
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_manifest(root: Path) -> list[dict[str, Any]]:
    root = root.resolve()
    rows: list[dict[str, Any]] = []
    for artifact in DEFAULT_ARTIFACTS:
        path = root / artifact
        rows.append({
            "path": artifact,
            "present": path.exists(),
            "sha256": sha256_file(path),
        })
    return rows


def _canonical_payload(manifest: list[dict[str, Any]]) -> bytes:
    return json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8")


def create_report_signature(
    root: Path,
    key_env_name: str = "SUBREPARO_REPORT_SIGNING_KEY",
) -> dict[str, Any]:
    root = root.resolve()
    manifest = artifact_manifest(root)
    payload = _canonical_payload(manifest)
    key = os.environ.get(key_env_name)
    if key:
        signature_type = "hmac_sha256"
        signature = hmac.new(key.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    else:
        signature_type = "sha256_manifest"
        signature = hashlib.sha256(payload).hexdigest()
    result = {
        "schema": SCHEMA,
        "generated_at": now(),
        "signature_type": signature_type,
        "signature": signature,
        "key_env_name": key_env_name,
        "signing_key_present": bool(key),
        "artifacts": manifest,
    }
    path = root / SIGNATURE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return result


def verify_report_signature(
    root: Path,
    key_env_name: str = "SUBREPARO_REPORT_SIGNING_KEY",
) -> dict[str, Any]:
    root = root.resolve()
    path = root / SIGNATURE_PATH
    if not path.exists():
        return {"schema": SCHEMA, "valid": False, "reason": "signature file missing"}
    stored = json.loads(path.read_text(encoding="utf-8"))
    current_manifest = artifact_manifest(root)
    payload = _canonical_payload(current_manifest)
    signature_type = stored.get("signature_type", "sha256_manifest")
    key = os.environ.get(key_env_name)
    if signature_type == "hmac_sha256":
        if not key:
            return {"schema": SCHEMA, "valid": False, "reason": "HMAC key missing"}
        expected = hmac.new(key.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    else:
        expected = hashlib.sha256(payload).hexdigest()
    return {
        "schema": SCHEMA,
        "valid": hmac.compare_digest(expected, stored.get("signature", "")),
        "signature_type": signature_type,
        "expected": expected,
        "observed": stored.get("signature"),
        "artifacts": current_manifest,
    }

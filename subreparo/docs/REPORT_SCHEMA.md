# SubReparo Report Schema

SubReparo reports are local-first. Raw private files are not uploaded by default.

## Engine JSON shape

```json
{
  "project": "<redacted project path>",
  "generated_at": "2026-01-01T00:00:00+00:00",
  "score": {
    "value": 85,
    "grade": "A",
    "findings": 2,
    "action": "Review medium and high signals."
  },
  "findings": [
    {
      "type": "immune_patrol",
      "severity": "high",
      "target": "relative/path/or/runtime-target",
      "message": "plain language signal",
      "recommendation": "plain language next step",
      "detail": "optional redacted detail"
    }
  ],
  "reparodynamics": [
    {
      "target": "same target",
      "type": "immune_patrol",
      "tgrm_phase": "detect",
      "rye": 0.0
    }
  ],
  "report_path": ".subreparo/report.md",
  "ledger_path": ".subreparo/repair_ledger.jsonl",
  "export_path": ".subreparo/chain_export.json"
}
```

## Local state files

- `.subreparo/report.md` human-readable report.
- `.subreparo/repair_ledger.jsonl` append-style repair event ledger.
- `.subreparo/chain_export.json` chain-facing export payload.
- `.subreparo/quarantine_manifest.jsonl` staged file manifest.
- `.subreparo/audit.jsonl` hash-chained local audit log.
- `.subreparo/sbom.json` SBOM-style dependency manifest inventory.

## Privacy expectations

Reports and bundles should redact home paths, emails, token-like secrets, and private key blocks before sharing.

# SBOM and Dependency Risk

SubReparo now includes a local SBOM-style manifest export and dependency risk review.

## Commands

```bash
subreparo-sbom . --json
subreparo-sbom . --output .subreparo/sbom.json
subreparo-sbom . --risk
```

## SBOM output

The SBOM-style export is not a full CycloneDX or SPDX document yet. It is a local manifest inventory with:

- schema name;
- generated timestamp;
- component count;
- manifest path;
- ecosystem;
- SHA-256 digest.

## Current dependency risk rules

- Unpinned Python requirements are flagged.
- `package.json` install lifecycle scripts are flagged for review.

This is local-first and does not upload manifests by default.

# Basic SubReparo Immune Run

```bash
cd tools/subreparo-immune
python -m pip install -e .
subreparo-immune init .
subreparo-immune run .
```

Expected output:

```text
SubReparo score: 70+/100
Findings: <number>
Action: <recommendation>
Report: .subreparo/report.md
Export: .subreparo/chain_export.json
```

Open:

```text
.subreparo/report.md
.subreparo/chain_export.json
```

The export payload is the future bridge input for `pallet-reparodynamics`.

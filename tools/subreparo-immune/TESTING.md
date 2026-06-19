# SubReparo Immune Testing

CI checks:

```bash
python -m compileall src tests
pytest -q
```

Smoke commands:

```bash
subreparo-immune init <tmpdir>
subreparo-immune rules --json
subreparo-immune policy <tmpdir> --json
subreparo-immune inventory <tmpdir> --json
subreparo-immune audit <tmpdir>
subreparo-modes --json
subreparo-cortex <tmpdir> --plan --json
subreparo-cortex <tmpdir> --next --json
subreparo-monitor <tmpdir> --once --json
subreparo-sbom <tmpdir> --json
```

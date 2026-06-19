# Contributing to SubReparo

SubReparo-specific contributions should keep the system local-first, safe, and useful before chain integration.

## Good first areas

- Improve docs and examples.
- Add tests for `tools/subreparo-immune`.
- Add detector coverage.
- Improve report output.
- Add pallet tests and benchmarks.
- Help wire `pallet-reparodynamics` into a local SDK runtime.

## Privacy and safety

Do not add features that publish raw private project files, private logs, customer data, credentials, or local-only records.

SubReparo should store safe summaries and digests when data crosses system boundaries.

## Development

```bash
cd tools/subreparo-immune
python -m pip install -e . pytest ruff mypy build
ruff check src tests
mypy src
pytest
python -m build
```

## Pull requests

Include:

- what changed;
- why it matters;
- how it was tested;
- any privacy or safety implications.

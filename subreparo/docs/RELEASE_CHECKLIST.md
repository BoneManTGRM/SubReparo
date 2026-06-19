# SubReparo Release Checklist

## Python package

```bash
cd tools/subreparo-immune
python -m pip install -e . pytest ruff mypy build twine
ruff check src tests
mypy src
pytest
python -m build
python -m twine check dist/*
```

## Documentation

- README updated.
- Examples updated.
- Changelog updated.
- Roadmap updated.
- Safety/privacy notes reviewed.

## GitHub repository

Recommended topics:

```text
subreparo
reparodynamics
polkadot-sdk
substrate
frame
self-healing
ai-agents
repair-memory
software-resilience
```

Recommended badges:

- CI status
- Python version
- license
- package version after PyPI release

## Chain side

Before any public chain release:

- pallet tests;
- benchmarks;
- runtime integration;
- storage growth review;
- origin checks;
- external review.

## Community launch

Share only after the local MVP is easy to install and test.

Target communities:

- Polkadot SDK / Substrate developers;
- AI-agent builders;
- software resilience/self-healing communities;
- local-first developer tool communities.

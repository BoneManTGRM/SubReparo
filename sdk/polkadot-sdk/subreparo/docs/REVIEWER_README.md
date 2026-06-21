# SubReparo Reviewer README

SubReparo is currently a Polkadot SDK/Substrate runtime modification scaffold for bounded TGRM repair.

## Review order

1. Read `README.md` at repo root.
2. Read `subreparo/docs/SDK_TGRM_RUNTIME_PLAN.md`.
3. Review pallet code under:

```text
sdk/polkadot-sdk/frame/subreparo
sdk/polkadot-sdk/frame/subreparo-controller
sdk/polkadot-sdk/frame/subreparo-finality-backoff
```

4. Review integration docs:

```text
sdk/polkadot-sdk/subreparo/docs/WORKSPACE_INTEGRATION.md
sdk/polkadot-sdk/subreparo/docs/RUNTIME_EXAMPLE_WIRING.md
sdk/polkadot-sdk/subreparo/docs/OBSERVABILITY.md
sdk/polkadot-sdk/subreparo/docs/VERIFICATION_CHECKLIST.md
```

5. Run harness:

```bash
python subreparo/harness/tgrm_vs_baseline.py --csv subreparo/harness/tgrm_vs_baseline.csv
python -m pytest subreparo/harness
```

## Current status

```text
scaffold: yes
runtime concept: yes
mock tests: drafted
benchmark stubs: drafted
weights stubs: drafted
live cargo verification: still needed
production readiness: no
```

## Claim boundary

Acceptable claim:

```text
SubReparo is a research/prototype SDK runtime scaffold implementing bounded Reparodynamics/TGRM repair concepts.
```

Do not claim:

```text
production-ready runtime
validated performance improvement
Polkadot replacement
autonomous security system
```

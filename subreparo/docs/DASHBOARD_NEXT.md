# Dashboard Next

The dashboard already shows report, alerts, quarantine, ledger count, and chain export preview.

Attempted next dashboard expansion:

- risk trends section;
- timeline section;
- richer local state overview.

The connector blocked the direct dashboard update during this batch, so the supporting backend modules were shipped first:

- `timeline.py`
- `trends.py`
- `modes.py`
- `sbom.py`
- `dependency_risk.py`

Next safe dashboard step is to add the trends and timeline sections in a smaller patch.

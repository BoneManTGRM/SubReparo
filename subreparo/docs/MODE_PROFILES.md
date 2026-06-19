# SubReparo Mode Profiles

SubReparo supports user-facing review modes so the same engine can serve different users.

## Modes

- `simple`: main items that need attention.
- `family`: high-risk items only, suitable for non-technical users.
- `developer`: developer-relevant signals with moderate noise tolerance.
- `expert`: all available findings.
- `paranoid`: aggressive review mode with more signals.

Current mode definitions live in:

```text
tools/subreparo-immune/src/subreparo_immune/modes.py
```

Command:

```bash
subreparo-modes
subreparo-modes --json
```

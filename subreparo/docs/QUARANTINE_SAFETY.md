# Quarantine Safety Model

SubReparo uses staged isolation first.

## Safety rules

- Active files are not permanently removed directly.
- High-risk findings can be moved into `.subreparo/quarantine`.
- Staged files can be restored by index.
- Staged files can be removed from staging after review.
- Staged-file removal is restricted to files inside `.subreparo`.

## Commands

```bash
subreparo-immune isolate .
subreparo-immune isolate . --apply
subreparo-quarantine .
subreparo-quarantine . --restore-index 0
subreparo-quarantine . --remove-index 0
```

This keeps false-positive recovery possible while still removing suspicious files from active paths.

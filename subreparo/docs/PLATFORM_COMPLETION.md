# SubReparo Platform Completion Layer

This layer records final local platform commands.

```bash
subreparo-alerts . --json
subreparo-tray . --json
subreparo-installer . --json
subreparo-updater . --json
subreparo-fleet . --json
```

## Coverage

- Desktop tray manifest.
- Alert planning and local alert inbox records.
- Platform package metadata.
- Dry-run update plan.
- Local fleet dashboard manifest.

The commands are local-first and preview-oriented. Larger release steps stay review-gated.

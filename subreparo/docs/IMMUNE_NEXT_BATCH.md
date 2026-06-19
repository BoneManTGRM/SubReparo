# Immune Next Batch

This batch expands SubReparo from a project scanner into a stronger local defensive product path.

## Added capabilities

1. Startup and persistence review.
2. Cron, systemd, LaunchAgent, and Startup-folder coverage where present.
3. Browser extension manifest review.
4. Launcher and shortcut review.
5. Local policy file for allowed hashes, blocked hashes, and ignored targets.
6. Policy filtering in the engine.
7. Standalone monitor entry point.
8. Quarantine visibility in the dashboard.
9. Monitor-alert visibility in the dashboard.
10. Severity explanations in reports.

## New commands

```bash
subreparo-monitor . --once
subreparo-monitor . --interval 10
```

Existing commands still apply:

```bash
subreparo-immune doctor .
subreparo-immune patrol .
subreparo-immune isolate . --apply
subreparo-immune quarantine .
subreparo-immune baseline .
subreparo-immune diff .
subreparo-immune dashboard
```

## Policy file

The local policy file is:

```text
.subreparo/policy.json
```

Shape:

```json
{
  "allowed_hashes": [],
  "blocked_hashes": [],
  "ignored_targets": []
}
```

SubReparo remains local-first. It does not upload private files by default.

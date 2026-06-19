# Notifications

SubReparo includes a local notification stub for future tray/desktop integration.

Current implementation:

```text
tools/subreparo-immune/src/subreparo_immune/notifications.py
```

It creates local notification records and writes them to `.subreparo/notifications.jsonl`.

The implementation does not invoke OS-level notification APIs yet. That keeps this stage portable and safe for CI.

Future work:

- Windows toast notifications;
- macOS notification center;
- Linux desktop notifications;
- tray status icon;
- user-configurable alert thresholds.

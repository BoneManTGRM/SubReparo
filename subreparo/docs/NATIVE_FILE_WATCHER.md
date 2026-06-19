# Native File Watcher

SubReparo now has an alert-only native file watcher path for local directories.

## Purpose

The native watcher is meant to observe local file-system events and surface them to the user without taking automatic repair action.

It supports:

- created files;
- modified files;
- deleted files;
- moved files;
- executable or persistence-capable file highlighting;
- configured watch-plan targets;
- safe fallback when the optional native dependency is not installed.

## Install optional native watcher support

```bash
cd tools/subreparo-immune
python -m pip install -e ".[native-watch]"
```

The optional dependency is `watchdog`. SubReparo does not require it for the base CLI.

## Run a short native watch session

```bash
subreparo-monitor . --native-watch --duration 15
```

JSON output:

```bash
subreparo-monitor . --native-watch --duration 15 --json
```

Watch all configured file targets:

```bash
subreparo-monitor . --native-watch --all-targets --duration 30 --json
```

## Polling snapshot fallback

When native watcher support is unavailable, SubReparo returns a structured fallback payload instead of failing. The fallback is intentionally metadata-only and does not read file contents.

Snapshot fields include:

- relative path;
- file size;
- modified time;
- suffix.

The snapshot does not include raw content, file hashes, or external lookups.

## Safety boundary

The watcher is:

- local-only;
- non-destructive;
- alert-only by default;
- metadata-only in fallback mode;
- not a background service installer;
- not an auto-repair mechanism.

High-impact action remains outside the watcher. Use patrol, baseline diff, quarantine preview, and approval-gated repair flows before making changes.

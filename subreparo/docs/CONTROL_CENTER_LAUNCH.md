# Launch SubReparo Control Center

SubReparo currently opens as a local web dashboard.

It is not public and does not expose a remote service by default. The dashboard binds to localhost:

```text
http://127.0.0.1:8765
```

## macOS / Linux

From the repository root:

```bash
bash scripts/start-subreparo-control-center.sh
```

Then open:

```text
http://127.0.0.1:8765
```

## macOS double-click launcher

The repo also includes:

```text
scripts/start-subreparo-control-center.command
```

On macOS, make it executable once:

```bash
chmod +x scripts/start-subreparo-control-center.command
```

Then double-click it from Finder.

## Windows command launcher

From Command Prompt at the repository root:

```cmd
scripts\start-subreparo-control-center.cmd
```

Then open:

```text
http://127.0.0.1:8765
```

## Manual launch

```bash
cd tools/subreparo-immune
python -m pip install -e .
cd ../..
subreparo-immune dashboard
```

Then open:

```text
http://127.0.0.1:8765
```

## Launch readiness check

After installing the package:

```bash
subreparo-launch-check . --json
```

This reports whether the local launch scripts and launch docs are present.

## What you can see now

The Control Center includes:

```text
Overview
Cortex
Immune Agent
Swarms
Agent components
Protection
Reports
```

The Immune Agent tab shows:

```text
agent cycles
scar memory
repair ledger tail
latest proof export
```

The Swarms tab shows:

```text
live swarm map
swarm role/tool metrics
saved swarm plans
role and tool catalog
```

## Current limitation

This is the first local dashboard version, not a packaged desktop app yet.

The desktop-app target remains:

```text
Windows installer
macOS app bundle
Linux package
background service
tray icon
notifications
```

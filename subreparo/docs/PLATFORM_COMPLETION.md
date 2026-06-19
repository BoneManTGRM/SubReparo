# SubReparo Platform Completion Layer

This layer closes the remaining 100-point product roadmap items without adding destructive behavior.

## Desktop tray layer

`subreparo-tray . --json` returns a local desktop tray manifest with dashboard status, alert inbox counts, and safe menu labels. It does not start a GUI by default.

## Native alert layer

`subreparo-alerts . --json` converts local watcher records into local alert plans. Alert plans are preview-first and can be saved to `.subreparo/native_alerts.jsonl` with `--write-inbox`.

## Package manifest layer

`subreparo-installer . --json` returns Windows, macOS, and Linux package metadata for the existing local helpers and console entry points.

## Update plan layer

`subreparo-updater . --json` returns a local update plan. It is dry-run by default and marks non-current target versions as approval-required.

## Fleet dashboard layer

`subreparo-fleet . --json` returns a local fleet dashboard manifest. It summarizes node state from `.subreparo` metadata and does not collect raw file content.

## Safety model

- Local-first by default.
- No raw private file content in fleet summaries.
- Release and update actions require manual approval.

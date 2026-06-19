# SubReparo Roadmap

## Current position

SubReparo is a promising early system: bio-inspired repair memory for AI/software plus a Polkadot SDK path for on-chain repair records.

The product is intentionally local-first. The chain should prove and remember verified repair summaries, not replace the local engine.

## Latest completed platform batch

- Added desktop tray manifest support through `subreparo-tray`.
- Added local native alert planning and alert inbox records through `subreparo-alerts`.
- Added Windows, macOS, and Linux installer packaging manifests through `subreparo-installer`.
- Added dry-run update planning through `subreparo-updater`.
- Added a local fleet dashboard manifest through `subreparo-fleet`.
- Added tests and CI smoke coverage for the final platform commands.
- Completed the remaining open roadmap items as safe scaffolds with manual approval gates for high-impact release or update actions.

## Phase 1: Local-first MVP

- Package `tools/subreparo-immune` for PyPI.
- Add tests, type checks, CI, and release workflow.
- Keep reports, ledger, and chain export local by default.
- Add examples and screenshots.
- Improve detector coverage.

## Phase 2: Better detection

- Git integration.
- Dependency manifest review.
- Static code review hooks.
- AI-agent project review.
- Website health checks.
- Config and deployment review.
- Recurring-signal learning memory.

## Phase 3: Safe repair workflow

- Approval queue.
- Safe repair suggestions.
- Local backups before approved changes.
- Verification checks after repair.
- False positive handling.
- Recurring issue escalation.

## Phase 4: Polkadot SDK runtime

- Wire `pallet-reparodynamics` into an SDK runtime.
- Submit first local repair event.
- Update repair status on-chain.
- Query repair storage.
- Benchmark and review the pallet.

## Phase 5: Community and release

- Add GitHub topics.
- Add releases and changelog.
- Add contribution guide.
- Add issue templates.
- Publish technical diagrams.
- Share in Polkadot, AI-agent, and self-healing software communities.

## Phase 6: SubReparo network

- Optional shared repair-memory patterns.
- Digest-only proofs.
- Verifier roles.
- Reputation model.
- Chain bridge from local engine exports.

## Non-goals for early versions

- No public token launch.
- No risky automatic changes.
- No raw private project data on-chain.
- No dependency on chain for local value.

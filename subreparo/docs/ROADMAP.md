# SubReparo Roadmap

## Current position

SubReparo is a promising early system: bio-inspired repair memory for AI/software plus a Polkadot SDK path for on-chain repair records.

The product is intentionally local-first. The chain should prove and remember verified repair summaries, not replace the local engine.

## Latest completed platform batch

- Added first-run setup profiles through `subreparo-immune setup`.
- Added false-positive feedback through `subreparo-immune feedback`.
- Added file, folder, and domain trust scoring through `subreparo-immune trust`.
- Surfaced trust scores in markdown reports, append-only ledger records, and chain export payloads.
- Added watcher backend and target planning through `subreparo-immune watch-plan`.
- Added local report integrity signatures through `subreparo-immune sign-report`.
- Converted the local dashboard into tabbed panels for overview, Cortex, agent components, protection, and reports.
- Integrated feedback, trust reports, and report signatures into the main local run flow.
- Added tests and CI smoke coverage for the new platform commands and feedback/trust behavior.

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

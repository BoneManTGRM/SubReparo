# pallet-reparodynamics Security Review Checklist

## Before public use

- Add pallet unit tests.
- Add runtime integration tests.
- Add benchmarks and weights.
- Bound every stored vector.
- Review storage growth and pruning strategy.
- Review origin rules for status updates.
- Decide whether status updates require reporter, verifier, governance, or role-based origin.
- Confirm no raw private data is stored.
- Confirm event payloads are small and bounded.
- Confirm invalid event ids fail safely.

## Threat model

### Data exposure

Risk: users submit private details to chain storage.

Control: the local engine should submit only safe labels, statuses, summaries, and digests.

### Spam/storage growth

Risk: many low-value events increase storage.

Control: add deposits, rate limits, pruning, or governance-controlled parameters before production.

### False verification

Risk: untrusted accounts mark bad repairs as verified.

Control: define a verifier role, reporter-only update flow, or governance/collective process.

### Runtime weight mismatch

Risk: calls undercharge weight.

Control: add benchmarks before public deployment.

## Audit status

Current status: scaffold only. Not audited. Not production-ready.

# SubReparo Storage Versioning

This is a placeholder for the first runtime storage version plan.

## Initial version

```text
StorageVersion = 1
```

## Pallets needing version tracking

```text
pallet-subreparo
pallet-subreparo-controller
pallet-subreparo-finality-backoff
```

## Migration policy

Before any production runtime deployment:

```text
1. Add StorageVersion to each pallet.
2. Add migration tests for every future storage change.
3. Add try-runtime checks.
4. Document storage layout and migration assumptions.
5. Never silently alter repair-history semantics.
```

## Critical state

```text
DriftLevel
EpochIndex
SeenNonces
RepairsPaused
RepairsThisBlock
EpochCooldownRemaining
ConsecutiveBreaches
ControllerNonce
FinalityLag
```

Repair history and nonce semantics should be treated as audit-critical.

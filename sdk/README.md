# SDK Foundation Workspace

This folder is reserved for the Polkadot SDK foundation of SubReparo Chain.

## Important

The full Polkadot SDK source tree is intentionally not committed manually here yet because it contains thousands of files.

Instead, this repository includes scripts and workflow support to pull the active Polkadot SDK source and prepare a SubReparo SDK workspace.

## Target layout after bootstrap

```text
sdk/polkadot-sdk/                  -> active Polkadot SDK source
sdk/polkadot-sdk/frame/reparodynamics/
sdk/polkadot-sdk/tools/subreparo-immune/
sdk/polkadot-sdk/subreparo/docs/
```

## Why this matters

SubReparo needs Polkadot SDK for:

- modern FRAME runtime work;
- pallet integration;
- local node testing;
- benchmarking;
- future parachain path;
- real repair-ledger chain development.

## Bootstrap locally

From the repository root:

```bash
bash scripts/bootstrap-sdk-foundation.sh
```

Windows PowerShell:

```powershell
./scripts/bootstrap-sdk-foundation.ps1
```

## After bootstrap

The next chain milestone is to wire `pallet-reparodynamics` into a selected SDK runtime/template and submit the first local repair event.

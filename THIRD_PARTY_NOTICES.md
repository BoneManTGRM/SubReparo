# Third-Party Notices

This repository contains SubReparo-specific code and references upstream open-source foundations used for SubReparo Chain development.

## Polkadot SDK

SubReparo uses Polkadot SDK as the chain foundation through the SDK workspace path:

```text
sdk/polkadot-sdk
```

Upstream project:

```text
https://github.com/paritytech/polkadot-sdk
```

The Polkadot SDK repository provides the components needed to build on Polkadot, including Substrate, FRAME, Cumulus, and related tooling.

License note:

The Substrate README in Polkadot SDK describes split licensing: Substrate primitives, FRAME, pallets, binaries, and utilities are Apache-2.0, while Substrate client code is GPL-3.0 with a classpath linking exception.

SubReparo-specific additions are kept separate from upstream SDK code where practical:

```text
frame/reparodynamics/
tools/subreparo-immune/
subreparo/docs/
```

## SubReparo-specific additions

SubReparo-specific code and docs are intended to be Apache-2.0 unless a file states otherwise.

## Data boundary

SubReparo should not place raw private project files, logs, customer data, or secrets on-chain.

The chain path should use safe summaries, labels, status values, RYE metrics, TGRM phases, and digests.

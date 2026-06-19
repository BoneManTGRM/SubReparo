# SDK Base

SubReparo V2 uses Polkadot SDK as the chain base.

Clean layout:

```text
sdk/polkadot-sdk/
frame/reparodynamics/
tools/subreparo-immune/
subreparo/docs/
```

Upstream:

```text
https://github.com/paritytech/polkadot-sdk.git
```

Pinned planning commit:

```text
bcafdb3d87eb3756f64bd1e830b0785d17a86812
```

The scripts in `scripts/` prepare a local SDK workspace and copy the SubReparo additions into it.

Next chain milestone: wire `frame/reparodynamics` into a selected SDK runtime/template and run a local node.

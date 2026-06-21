# SubReparo Workspace Integration Notes

These notes show how to wire the SubReparo pallets into a Polkadot SDK workspace.

## Add workspace members

In the SDK root `Cargo.toml`, add:

```toml
[workspace]
members = [
  "frame/subreparo",
  "frame/subreparo-controller",
  "frame/subreparo-finality-backoff",
]
```

If the SDK already has a large workspace list, add the three paths to the existing `members` array instead of replacing it.

## Runtime dependencies

In the target runtime `Cargo.toml`, add:

```toml
pallet-subreparo = { path = "../frame/subreparo", default-features = false }
pallet-subreparo-controller = { path = "../frame/subreparo-controller", default-features = false }
pallet-subreparo-finality-backoff = { path = "../frame/subreparo-finality-backoff", default-features = false }
```

Add to runtime `std` feature:

```toml
"pallet-subreparo/std",
"pallet-subreparo-controller/std",
"pallet-subreparo-finality-backoff/std",
```

Add to runtime `runtime-benchmarks` feature:

```toml
"pallet-subreparo/runtime-benchmarks",
"pallet-subreparo-controller/runtime-benchmarks",
"pallet-subreparo-finality-backoff/runtime-benchmarks",
```

## Build checks

From SDK root:

```bash
cargo check -p pallet-subreparo
cargo check -p pallet-subreparo-controller
cargo check -p pallet-subreparo-finality-backoff
cargo test -p pallet-subreparo
cargo test -p pallet-subreparo-controller
cargo test -p pallet-subreparo-finality-backoff
```

## Benchmark placeholders

The included benchmarking files are stubs. After runtime wiring, run FRAME benchmarks and regenerate production weights before any runtime deployment.

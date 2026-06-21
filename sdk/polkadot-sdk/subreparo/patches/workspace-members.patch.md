# Workspace Members Patch Note

This is a human-readable workspace patch note.

Add these members to the SDK workspace `Cargo.toml`:

```toml
members = [
  "frame/subreparo",
  "frame/subreparo-controller",
  "frame/subreparo-finality-backoff",
]
```

If the workspace already has a large `members` array, append these entries instead of replacing the array.

Then run:

```bash
cargo metadata --no-deps
cargo check -p pallet-subreparo
cargo check -p pallet-subreparo-controller
cargo check -p pallet-subreparo-finality-backoff
```

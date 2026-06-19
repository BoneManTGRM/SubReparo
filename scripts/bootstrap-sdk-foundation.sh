#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SDK_DIR="$ROOT_DIR/sdk/polkadot-sdk"

mkdir -p "$ROOT_DIR/sdk"

if [ ! -d "$SDK_DIR/.git" ]; then
  git clone https://github.com/paritytech/polkadot-sdk.git "$SDK_DIR"
else
  git -C "$SDK_DIR" pull --ff-only
fi

mkdir -p "$SDK_DIR/subreparo"
mkdir -p "$SDK_DIR/tools"

if [ -d "$ROOT_DIR/frame/reparodynamics" ]; then
  mkdir -p "$SDK_DIR/frame/reparodynamics"
  cp -R "$ROOT_DIR/frame/reparodynamics/." "$SDK_DIR/frame/reparodynamics/"
fi

if [ -d "$ROOT_DIR/tools/subreparo-immune" ]; then
  rm -rf "$SDK_DIR/tools/subreparo-immune"
  cp -R "$ROOT_DIR/tools/subreparo-immune" "$SDK_DIR/tools/subreparo-immune"
fi

if [ -d "$ROOT_DIR/subreparo/docs" ]; then
  rm -rf "$SDK_DIR/subreparo/docs"
  cp -R "$ROOT_DIR/subreparo/docs" "$SDK_DIR/subreparo/docs"
fi

cat > "$SDK_DIR/SUBREPARO_FOUNDATION.md" <<'NOTES'
# SubReparo Polkadot SDK Foundation

This SDK workspace was prepared from paritytech/polkadot-sdk and populated with SubReparo additions.

Copied into SDK workspace:

- frame/reparodynamics
- tools/subreparo-immune
- subreparo/docs

Next steps:

1. Add frame/reparodynamics to the SDK workspace.
2. Add pallet-reparodynamics to a selected runtime/template.
3. Configure bounded field sizes.
4. Build the runtime.
5. Run a local node.
6. Submit the first repair event.
7. Connect tools/subreparo-immune chain export payloads to the pallet.

Private raw project data should remain local. Chain records should use safe summaries and digests.
NOTES

echo "Polkadot SDK foundation prepared at: $SDK_DIR"
echo "Next: wire frame/reparodynamics into the selected SDK runtime/template."

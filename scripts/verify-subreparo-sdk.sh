#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "== SubReparo SDK verification =="

if [ -f "subreparo/harness/tgrm_vs_baseline.py" ]; then
  echo "-- Running Python TGRM harness"
  python subreparo/harness/tgrm_vs_baseline.py --csv subreparo/harness/tgrm_vs_baseline.csv
fi

if command -v pytest >/dev/null 2>&1; then
  echo "-- Running Python harness invariant tests"
  python -m pytest subreparo/harness
else
  echo "-- pytest not installed; skipping Python invariant tests"
  echo "   Install with: python -m pip install pytest"
fi

if [ -d "sdk/polkadot-sdk" ] && [ -f "sdk/polkadot-sdk/Cargo.toml" ]; then
  echo "-- Polkadot SDK checkout detected"
  cd sdk/polkadot-sdk
  cargo metadata --no-deps
  cargo check -p pallet-subreparo
  cargo check -p pallet-subreparo-controller
  cargo check -p pallet-subreparo-finality-backoff
  cargo test -p pallet-subreparo
  cargo test -p pallet-subreparo-controller
  cargo test -p pallet-subreparo-finality-backoff
else
  echo "-- Polkadot SDK checkout not initialized; skipping cargo checks"
  echo "   Run: git submodule update --init --recursive"
  echo "   Then rerun: bash scripts/verify-subreparo-sdk.sh"
fi

echo "== Verification script finished =="

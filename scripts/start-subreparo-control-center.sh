#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOL_DIR="$ROOT_DIR/tools/subreparo-immune"

cd "$TOOL_DIR"
python -m pip install -e . >/dev/null
cd "$ROOT_DIR"

echo "Starting SubReparo Control Center..."
echo "Open: http://127.0.0.1:8765"
subreparo-immune dashboard

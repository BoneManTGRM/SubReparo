#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR/tools/subreparo-immune"

python3 -m pip install --upgrade pip
python3 -m pip install -e .

echo "SubReparo Immune installed."
echo "Try: subreparo-immune doctor ."
echo "Try: subreparo-monitor . --once"

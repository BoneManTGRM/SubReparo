$ErrorActionPreference = "Stop"

$RootDir = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location (Join-Path $RootDir "tools/subreparo-immune")

python -m pip install --upgrade pip
python -m pip install -e .

Write-Host "SubReparo Immune installed."
Write-Host "Try: subreparo-immune doctor ."
Write-Host "Try: subreparo-monitor . --once"

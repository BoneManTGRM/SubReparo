$ErrorActionPreference = "Stop"

$RootDir = Resolve-Path (Join-Path $PSScriptRoot "..")
$SdkDir = Join-Path $RootDir "sdk\polkadot-sdk"

New-Item -ItemType Directory -Force -Path (Join-Path $RootDir "sdk") | Out-Null

if (!(Test-Path (Join-Path $SdkDir ".git"))) {
  git clone https://github.com/paritytech/polkadot-sdk.git $SdkDir
} else {
  git -C $SdkDir pull --ff-only
}

New-Item -ItemType Directory -Force -Path (Join-Path $SdkDir "subreparo") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $SdkDir "tools") | Out-Null

$Pallet = Join-Path $RootDir "frame\reparodynamics"
if (Test-Path $Pallet) {
  New-Item -ItemType Directory -Force -Path (Join-Path $SdkDir "frame\reparodynamics") | Out-Null
  Copy-Item -Recurse -Force (Join-Path $Pallet "*") (Join-Path $SdkDir "frame\reparodynamics")
}

$Immune = Join-Path $RootDir "tools\subreparo-immune"
if (Test-Path $Immune) {
  $OutImmune = Join-Path $SdkDir "tools\subreparo-immune"
  if (Test-Path $OutImmune) { Remove-Item -Recurse -Force $OutImmune }
  Copy-Item -Recurse $Immune $OutImmune
}

$Docs = Join-Path $RootDir "subreparo\docs"
if (Test-Path $Docs) {
  $OutDocs = Join-Path $SdkDir "subreparo\docs"
  if (Test-Path $OutDocs) { Remove-Item -Recurse -Force $OutDocs }
  Copy-Item -Recurse $Docs $OutDocs
}

@"
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
"@ | Set-Content -Encoding UTF8 (Join-Path $SdkDir "SUBREPARO_FOUNDATION.md")

Write-Host "Polkadot SDK foundation prepared at: $SdkDir"
Write-Host "Next: wire frame/reparodynamics into the selected SDK runtime/template."

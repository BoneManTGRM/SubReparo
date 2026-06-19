# SubReparo CLI Reference

## Core

```bash
subreparo-immune init .
subreparo-immune doctor .
subreparo-immune run . --json
subreparo-immune patrol .
subreparo-monitor . --once
```

## Baseline and integrity

```bash
subreparo-immune baseline .
subreparo-immune diff .
```

## Isolation and quarantine

```bash
subreparo-immune isolate .
subreparo-immune isolate . --apply
subreparo-quarantine .
subreparo-quarantine . --restore-index 0
subreparo-quarantine . --remove-index 0
```

## Policy

```bash
subreparo-immune policy .
subreparo-immune policy . --allow-hash <sha256>
subreparo-immune policy . --block-hash <sha256>
subreparo-immune policy . --ignore-target <target>
```

## Reports and product views

```bash
subreparo-immune timeline .
subreparo-immune trends .
subreparo-immune inventory .
subreparo-sbom . --json
subreparo-sbom . --risk
subreparo-modes
subreparo-immune bundle .
subreparo-immune audit .
subreparo-immune dashboard
```

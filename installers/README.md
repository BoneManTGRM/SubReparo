# SubReparo Installer Scaffolds

This folder tracks installer packaging direction for Windows, macOS, and Linux.

The current installer layer is a safe scaffold. It does not auto-install services, change startup settings, or enable auto-update behavior.

## Targets

- Windows: future MSI or MSIX packaging.
- macOS: future signed app bundle and pkg or dmg packaging.
- Linux: future deb, rpm, AppImage, and systemd user-service packaging.

## Required gates before release

1. Local tests pass.
2. Package build passes.
3. Installer runs in a disposable VM.
4. Uninstall is verified.
5. Background monitoring remains opt-in.
6. Auto-update remains disabled unless explicitly configured.

# Linux Installer Scaffold

Planned package targets: deb, rpm, AppImage, and optional user-level systemd service.

Current status: scaffold only.

Release requirements:

- package the local CLI and dashboard launcher;
- keep any background service opt-in and user-level by default;
- store reports and evidence under local SubReparo state;
- verify uninstall removes package files without deleting evidence unless explicitly requested.

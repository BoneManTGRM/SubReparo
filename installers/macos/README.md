# macOS Installer Scaffold

Planned package target: signed app bundle with pkg or dmg distribution.

Current status: scaffold only.

Release requirements:

- package the local CLI and dashboard launcher;
- notarize before external distribution;
- keep background monitoring opt-in;
- use user-local state for reports and evidence;
- verify uninstall does not remove local evidence unless explicitly requested.

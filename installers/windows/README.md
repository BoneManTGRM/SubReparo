# Windows Installer Scaffold

Planned package target: MSI or MSIX.

Current status: scaffold only.

Release requirements:

- build `subreparo-immune` wheel;
- install CLI entry points;
- keep monitor and tray startup opt-in;
- write logs under user-local SubReparo state;
- verify uninstall removes installed application files without deleting user evidence under `.subreparo` unless explicitly requested.

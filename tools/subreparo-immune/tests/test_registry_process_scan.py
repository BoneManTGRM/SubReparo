from pathlib import Path

from subreparo_immune.models import Severity
from subreparo_immune.process_scan import ProcessSnapshot, scan_processes
from subreparo_immune.registry_scan import scan_registry_startup


def test_registry_startup_scanner_reads_local_fixture(tmp_path: Path) -> None:
    registry_dir = tmp_path / "registry"
    registry_dir.mkdir()
    (registry_dir / "run.reg").write_text(
        r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run\Updater powershell -enc AAAA",
        encoding="utf-8",
    )

    findings = scan_registry_startup(tmp_path)

    assert findings
    assert findings[0].severity == Severity.HIGH
    assert "registry startup" in findings[0].message


def test_process_scan_flags_parent_child_anomaly() -> None:
    processes = [
        ProcessSnapshot(pid="10", ppid="1", command="chrome.exe"),
        ProcessSnapshot(pid="11", ppid="10", command="powershell -NoProfile"),
    ]

    findings = scan_processes(processes)

    assert any("parent-child" in finding.message for finding in findings)


def test_process_scan_flags_unknown_binary_from_risky_location() -> None:
    processes = [
        ProcessSnapshot(pid="20", ppid="1", command=r"C:\Users\User\AppData\Local\Temp\updater.exe"),
    ]

    findings = scan_processes(processes)

    assert any("unknown binary" in finding.message for finding in findings)

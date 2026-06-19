from pathlib import Path

from subreparo_immune.browser_scan import scan_browser_extensions
from subreparo_immune.policy import LocalPolicy, apply_policy
from subreparo_immune.shortcut_scan import scan_shortcuts
from subreparo_immune.startup_scan import scan_startup
from subreparo_immune.models import Finding, FindingType, Severity


def test_startup_scanner_flags_script(tmp_path: Path) -> None:
    startup = tmp_path / "startup"
    startup.mkdir()
    script = startup / "loader.ps1"
    script.write_text("Write-Host test\n", encoding="utf-8")
    findings = scan_startup(tmp_path)
    assert any(f.severity == Severity.HIGH for f in findings)


def test_browser_scanner_flags_sensitive_permission(tmp_path: Path) -> None:
    ext = tmp_path / "Extensions" / "abc" / "1.0"
    ext.mkdir(parents=True)
    (ext / "manifest.json").write_text('{"permissions":["tabs","cookies"]}', encoding="utf-8")
    findings = scan_browser_extensions(tmp_path)
    assert any("sensitive permissions" in f.message for f in findings)


def test_shortcut_scanner_flags_remote_launcher(tmp_path: Path) -> None:
    launcher = tmp_path / "open.url"
    launcher.write_text("URL=https://example.com/file.exe\n", encoding="utf-8")
    findings = scan_shortcuts(tmp_path)
    assert any(f.severity == Severity.MEDIUM for f in findings)


def test_policy_filters_allowed_hash_detail() -> None:
    finding = Finding(
        type=FindingType.IMMUNE_PATROL,
        severity=Severity.HIGH,
        target="tool.exe",
        message="test",
        recommendation="review",
        detail="sha256=abc123",
    )
    policy = LocalPolicy(allowed_hashes={"abc123"}, blocked_hashes=set(), ignored_targets=set())
    assert apply_policy([finding], policy) == []


def test_policy_escalates_blocked_hash_detail() -> None:
    finding = Finding(
        type=FindingType.IMMUNE_PATROL,
        severity=Severity.LOW,
        target="tool.exe",
        message="test",
        recommendation="review",
        detail="sha256=bad999",
    )
    policy = LocalPolicy(allowed_hashes=set(), blocked_hashes={"bad999"}, ignored_targets=set())
    result = apply_policy([finding], policy)
    assert result[0].severity == Severity.CRITICAL

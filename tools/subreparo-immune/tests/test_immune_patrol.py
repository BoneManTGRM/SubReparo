from pathlib import Path

from subreparo_immune.immune_patrol import patrol
from subreparo_immune.models import FindingType, Severity


def test_patrol_flags_encoded_command(tmp_path: Path) -> None:
    script = tmp_path / "check.ps1"
    script.write_text("powershell -EncodedCommand AAAA\n", encoding="utf-8")
    findings = patrol(tmp_path)
    assert any(f.type == FindingType.IMMUNE_PATROL for f in findings)
    assert any(f.severity == Severity.HIGH for f in findings)


def test_patrol_flags_binary_file(tmp_path: Path) -> None:
    binary = tmp_path / "tool.exe"
    binary.write_bytes(b"MZ" + b"\x00" * 256)
    findings = patrol(tmp_path)
    assert any("binary" in f.message for f in findings)


def test_patrol_ignores_clean_text(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("clean project note\n", encoding="utf-8")
    findings = patrol(tmp_path)
    assert findings == []

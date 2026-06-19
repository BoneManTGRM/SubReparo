from pathlib import Path

from subreparo_immune.quarantine import list_records, restore_record, stage_file


def test_stage_and_restore_file(tmp_path: Path) -> None:
    target = tmp_path / "tool.exe"
    target.write_bytes(b"MZ-test")

    record = stage_file(tmp_path, target, reason="test signal")
    assert not target.exists()
    assert Path(record.staged_path).exists()

    records = list_records(tmp_path / ".subreparo")
    assert len(records) == 1

    restored = restore_record(tmp_path, 0)
    assert restored.original_path == str(target.resolve())
    assert target.exists()
    assert target.read_bytes() == b"MZ-test"


def test_restore_refuses_existing_target(tmp_path: Path) -> None:
    target = tmp_path / "tool.exe"
    target.write_bytes(b"MZ-test")
    stage_file(tmp_path, target, reason="test signal")
    target.write_bytes(b"new")

    try:
        restore_record(tmp_path, 0)
    except FileExistsError:
        pass
    else:
        raise AssertionError("restore should refuse to overwrite an existing active file")

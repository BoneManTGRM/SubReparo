import json
from pathlib import Path

from subreparo_immune.feedback import mark_false_positive
from subreparo_immune.learning_cli import main as learning_main
from subreparo_immune.learning_profile import build_learning_profile


def test_learning_profile_summarizes_repeated_patterns_and_feedback(tmp_path: Path) -> None:
    state = tmp_path / ".subreparo"
    state.mkdir()
    row = {
        "finding": {
            "severity": "medium",
            "type": "immune_patrol",
            "message": "repeated test signal",
        }
    }
    (state / "repair_ledger.jsonl").write_text(
        json.dumps(row) + "\n" + json.dumps(row) + "\n",
        encoding="utf-8",
    )
    mark_false_positive("fixture.py", path=state / "feedback.json")

    payload = build_learning_profile(tmp_path)

    assert payload["schema"] == "subreparo.learning_profile.v1"
    assert payload["device_profile"]["fingerprint"]
    assert payload["repeated_patterns"][0]["count"] == 2
    assert payload["feedback_learning"][0]["target"] == "fixture.py"
    assert (state / "learning_profile.json").exists()


def test_learning_cli_runs_json(tmp_path: Path, capsys) -> None:
    exit_code = learning_main([str(tmp_path), "--json"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "subreparo.learning_profile.v1" in captured.out

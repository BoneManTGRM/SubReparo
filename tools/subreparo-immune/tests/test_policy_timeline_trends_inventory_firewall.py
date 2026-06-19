from pathlib import Path

from subreparo_immune.firewall import firewall_suggestions
from subreparo_immune.inventory import dependency_inventory
from subreparo_immune.policy import add_allowed_hash, add_blocked_hash, add_ignored_target, load_policy
from subreparo_immune.timeline import build_timeline
from subreparo_immune.trends import risk_trends


def test_policy_management_helpers(tmp_path: Path) -> None:
    policy_path = tmp_path / ".subreparo" / "policy.json"
    add_allowed_hash("a", policy_path)
    add_blocked_hash("b", policy_path)
    add_ignored_target("target", policy_path)
    policy = load_policy(policy_path)
    assert "a" in policy.allowed_hashes
    assert "b" in policy.blocked_hashes
    assert "target" in policy.ignored_targets


def test_timeline_reads_ledger(tmp_path: Path) -> None:
    state = tmp_path / ".subreparo"
    state.mkdir()
    (state / "repair_ledger.jsonl").write_text('{"created_at":"2026-01-01T00:00:00Z","finding":{"severity":"high","type":"immune_patrol"}}\n', encoding="utf-8")
    events = build_timeline(tmp_path)
    assert len(events) == 1
    assert events[0]["event_type"] == "finding"


def test_trends_counts_events(tmp_path: Path) -> None:
    state = tmp_path / ".subreparo"
    state.mkdir()
    (state / "repair_ledger.jsonl").write_text('{"created_at":"2026-01-01T00:00:00Z","finding":{"severity":"high","type":"immune_patrol"}}\n', encoding="utf-8")
    trends = risk_trends(tmp_path)
    assert trends["events_by_day"]["2026-01-01"] == 1
    assert trends["findings_by_severity"]["high"] == 1


def test_dependency_inventory_detects_manifest(tmp_path: Path) -> None:
    (tmp_path / "requirements.txt").write_text("pytest\n", encoding="utf-8")
    inventory = dependency_inventory(tmp_path)
    assert inventory["manifest_count"] == 1


def test_firewall_suggestions_shape() -> None:
    result = firewall_suggestions()
    assert "suggestions" in result

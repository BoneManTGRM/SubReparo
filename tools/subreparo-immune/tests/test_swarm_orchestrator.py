from pathlib import Path

from subreparo_immune.swarm_orchestrator import build_swarm_plan, list_swarm_plans, orchestrate_swarm


def test_build_swarm_plan_for_quality_goal() -> None:
    plan = build_swarm_plan("run quality checks")
    assert plan.blocked is False
    assert plan.primary_role == "tester"
    assert any(step.tool_key == "quality_gate" for step in plan.steps)


def test_build_swarm_plan_blocks_high_impact_goal() -> None:
    plan = build_swarm_plan("delete production secrets")
    assert plan.blocked is True
    assert plan.approval_required is True
    assert plan.steps == []


def test_orchestrate_swarm_saves_plan(tmp_path: Path) -> None:
    payload = orchestrate_swarm(tmp_path, "scan risk and patrol baseline")
    assert payload["schema"] == "subreparo.swarm_plan.v1"
    assert payload["saved_path"] is not None
    plans = list_swarm_plans(tmp_path)
    assert len(plans) == 1
    assert plans[0]["primary_role"] == "sentinel"

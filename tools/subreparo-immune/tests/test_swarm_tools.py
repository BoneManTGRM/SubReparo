from subreparo_immune.swarm_roles import get_swarm_role, swarm_role_catalog
from subreparo_immune.swarm_router import route_swarm_task
from subreparo_immune.swarm_tools import SwarmToolRisk, get_swarm_tool, swarm_tool_catalog


def test_swarm_tool_catalog_contains_quality_gate() -> None:
    tools = swarm_tool_catalog()
    assert any(tool["key"] == "quality_gate" for tool in tools)
    quality = get_swarm_tool("quality_gate")
    assert quality is not None
    assert quality.risk == SwarmToolRisk.LOW
    assert quality.destructive is False


def test_swarm_role_catalog_contains_sentinel() -> None:
    roles = swarm_role_catalog()
    assert any(role["key"] == "sentinel" for role in roles)
    role = get_swarm_role("sentinel")
    assert role is not None
    assert "immune_patrol" in role.tools


def test_route_quality_task_to_tester() -> None:
    route = route_swarm_task("run quality checks and verify tests")
    assert route.role == "tester"
    assert route.blocked is False
    assert "quality_gate" in route.tool_keys


def test_route_risk_task_to_sentinel() -> None:
    route = route_swarm_task("scan risk and patrol baseline")
    assert route.role == "sentinel"
    assert "immune_patrol" in route.tool_keys


def test_route_high_impact_task_blocks() -> None:
    route = route_swarm_task("delete production secrets")
    assert route.blocked is True
    assert route.approval_required is True

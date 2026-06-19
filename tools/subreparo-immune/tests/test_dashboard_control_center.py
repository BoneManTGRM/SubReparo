from subreparo_immune.dashboard import (
    render_immune_agent_memory,
    render_immune_agent_proof,
    render_page,
    render_swarm_catalog,
    render_swarm_plans,
)


def test_dashboard_renders_control_center() -> None:
    page = render_page()
    assert "SubReparo Control Center" in page
    assert "Swarms" in page
    assert "Live swarm map" in page
    assert "Pending approvals" in page
    assert "Immune agent core" in page


def test_dashboard_renders_swarm_catalog() -> None:
    catalog = render_swarm_catalog()
    assert "Planner" in catalog
    assert "quality_gate" in catalog


def test_dashboard_renders_empty_swarm_plans() -> None:
    plans = render_swarm_plans()
    assert "No swarm plans found" in plans or "primary_role" in plans


def test_dashboard_renders_immune_agent_sections() -> None:
    memory = render_immune_agent_memory()
    proof = render_immune_agent_proof()
    assert "subreparo.agent_scars.v1" in memory
    assert "subreparo.agent_proof_export.v1" in proof

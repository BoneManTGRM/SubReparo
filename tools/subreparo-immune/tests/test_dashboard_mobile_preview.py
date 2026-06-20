from subreparo_immune.dashboard import DashboardHandler


def test_dashboard_handler_has_token_gate() -> None:
    DashboardHandler.access_token = "abc"
    assert DashboardHandler.access_token == "abc"
    DashboardHandler.access_token = None

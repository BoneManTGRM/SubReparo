from pathlib import Path

from subreparo_immune.dashboard import render_page, render_watch_plan
from subreparo_immune.setup_wizard import create_setup_profile


def test_render_page_includes_tab_controls(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    page = render_page()

    assert "Dashboard tabs" in page
    assert "tab-overview" in page
    assert "tab-cortex" in page
    assert "tab-protection" in page
    assert "panel-reports" in page


def test_dashboard_watch_plan_uses_setup_profile(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    watched = tmp_path / "watched"
    watched.mkdir()
    create_setup_profile(tmp_path, watched_paths=[str(watched)])

    rendered = render_watch_plan()

    assert "subreparo.watch_plan.v1" in rendered
    assert str(watched) in rendered

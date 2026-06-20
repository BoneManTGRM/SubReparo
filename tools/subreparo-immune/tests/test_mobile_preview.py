from subreparo_immune.mobile_preview import build_mobile_preview_plan


def test_mobile_preview_plan_uses_supplied_token(monkeypatch) -> None:
    monkeypatch.setattr("subreparo_immune.mobile_preview.detect_local_ip", lambda: "192.168.1.25")
    plan = build_mobile_preview_plan(port=9999, token="abc")
    assert plan.host == "0.0.0.0"
    assert plan.port == 9999
    assert plan.token == "abc"
    assert plan.local_ip == "192.168.1.25"
    assert plan.phone_url == "http://192.168.1.25:9999/?token=abc"


def test_mobile_preview_plan_generates_token(monkeypatch) -> None:
    monkeypatch.setattr("subreparo_immune.mobile_preview.detect_local_ip", lambda: "192.168.1.25")
    plan = build_mobile_preview_plan()
    assert plan.token
    assert "token=" in plan.phone_url
    assert plan.safety_notes

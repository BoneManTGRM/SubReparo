from subreparo_immune.messaging_connectors import build_message_plan, messaging_status


def test_messaging_status_lists_connectors() -> None:
    payload = messaging_status()
    channels = {item["channel"] for item in payload["connectors"]}
    assert "telegram" in channels
    assert "whatsapp" in channels
    assert payload["safety_model"]["outbound_requires_approval"] is True


def test_message_plan_requires_configuration(monkeypatch) -> None:
    monkeypatch.delenv("SUBREPARO_TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("SUBREPARO_TELEGRAM_ALLOWED_CHAT_IDS", raising=False)
    payload = build_message_plan("telegram", "123", "hello")
    assert payload["allowed"] is False
    assert payload["approval_required"] is True


def test_message_plan_requires_recipient_allowlist(monkeypatch) -> None:
    monkeypatch.setenv("SUBREPARO_TELEGRAM_BOT_TOKEN", "token")
    monkeypatch.setenv("SUBREPARO_TELEGRAM_ALLOWED_CHAT_IDS", "999")
    payload = build_message_plan("telegram", "123", "hello")
    assert payload["allowed"] is False
    assert "allowlist" in payload["reason"]


def test_message_plan_allows_configured_recipient_but_requires_approval(monkeypatch) -> None:
    monkeypatch.setenv("SUBREPARO_TELEGRAM_BOT_TOKEN", "token")
    monkeypatch.setenv("SUBREPARO_TELEGRAM_ALLOWED_CHAT_IDS", "123")
    payload = build_message_plan("telegram", "123", "hello")
    assert payload["allowed"] is True
    assert payload["approval_required"] is True

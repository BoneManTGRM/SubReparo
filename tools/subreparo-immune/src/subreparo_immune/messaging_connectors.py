from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class MessagingChannel(str, Enum):
    TELEGRAM = "telegram"
    WHATSAPP = "whatsapp"


class MessagingAction(str, Enum):
    READ_UPDATES = "read_updates"
    SEND_MESSAGE = "send_message"
    WEBHOOK = "webhook"


@dataclass(frozen=True)
class MessagingConnector:
    channel: MessagingChannel
    name: str
    official_api: str
    env_vars: tuple[str, ...]
    inbound_supported: bool
    outbound_supported: bool
    approval_required_for_outbound: bool
    notes: str

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["channel"] = self.channel.value
        data["env_vars"] = list(self.env_vars)
        data["configured"] = all(bool(os.getenv(item)) for item in self.env_vars)
        data["missing_env_vars"] = [item for item in self.env_vars if not os.getenv(item)]
        return data


CONNECTORS = (
    MessagingConnector(
        channel=MessagingChannel.TELEGRAM,
        name="Telegram Bot API",
        official_api="https://core.telegram.org/bots/api",
        env_vars=("SUBREPARO_TELEGRAM_BOT_TOKEN", "SUBREPARO_TELEGRAM_ALLOWED_CHAT_IDS"),
        inbound_supported=True,
        outbound_supported=True,
        approval_required_for_outbound=True,
        notes="Use a BotFather-created bot token. Restrict allowed chat IDs.",
    ),
    MessagingConnector(
        channel=MessagingChannel.WHATSAPP,
        name="WhatsApp Business Platform / Cloud API",
        official_api="https://developers.facebook.com/docs/whatsapp/cloud-api/",
        env_vars=(
            "SUBREPARO_WHATSAPP_ACCESS_TOKEN",
            "SUBREPARO_WHATSAPP_PHONE_NUMBER_ID",
            "SUBREPARO_WHATSAPP_ALLOWED_RECIPIENTS",
        ),
        inbound_supported=True,
        outbound_supported=True,
        approval_required_for_outbound=True,
        notes="Use Meta's official WhatsApp Business Platform. Do not scrape personal WhatsApp Web.",
    ),
)


def connector_catalog() -> list[dict[str, Any]]:
    return [connector.to_dict() for connector in CONNECTORS]


def get_connector(channel: str) -> MessagingConnector | None:
    normalized = channel.strip().lower()
    for connector in CONNECTORS:
        if connector.channel.value == normalized:
            return connector
    return None


def _allowed_values(env_name: str) -> set[str]:
    raw = os.getenv(env_name, "")
    return {item.strip() for item in raw.split(",") if item.strip()}


def build_message_plan(channel: str, recipient: str, text: str) -> dict[str, Any]:
    connector = get_connector(channel)
    if connector is None:
        return {
            "allowed": False,
            "approval_required": True,
            "reason": f"Unknown messaging channel: {channel}",
        }

    payload = connector.to_dict()
    missing = payload["missing_env_vars"]
    if missing:
        return {
            "channel": connector.channel.value,
            "allowed": False,
            "approval_required": True,
            "reason": "Connector is not configured.",
            "missing_env_vars": missing,
        }

    if connector.channel == MessagingChannel.TELEGRAM:
        allowed = _allowed_values("SUBREPARO_TELEGRAM_ALLOWED_CHAT_IDS")
    else:
        allowed = _allowed_values("SUBREPARO_WHATSAPP_ALLOWED_RECIPIENTS")

    if recipient not in allowed:
        return {
            "channel": connector.channel.value,
            "allowed": False,
            "approval_required": True,
            "reason": "Recipient is not in the explicit allowlist.",
            "recipient": recipient,
        }

    return {
        "channel": connector.channel.value,
        "allowed": True,
        "approval_required": connector.approval_required_for_outbound,
        "reason": "Outbound messaging is configured but must be approved before sending.",
        "recipient": recipient,
        "message_preview": text[:500],
    }


def messaging_status() -> dict[str, Any]:
    return {
        "schema": "subreparo.messaging_connectors.v1",
        "connectors": connector_catalog(),
        "safety_model": {
            "official_apis_only": True,
            "personal_whatsapp_scraping": False,
            "outbound_requires_approval": True,
            "recipient_allowlist_required": True,
            "tokens_from_environment_only": True,
        },
    }

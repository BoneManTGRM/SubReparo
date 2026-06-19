from __future__ import annotations

import os
import re
from pathlib import Path

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?<!\d)(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})(?!\d)")
SSN = re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)")
CREDIT_CARDISH = re.compile(r"(?<!\d)(?:\d[ -]*?){13,19}(?!\d)")
CUSTOMER_ID = re.compile(r"(?i)\b(customer|client|account)[_-]?id\s*[:=]\s*['\"]?[A-Za-z0-9_.-]{4,}")
TOKENISH = re.compile(r"(?i)(api[_-]?key|token|secret|password|passwd|pwd)\s*[:=]\s*['\"]?[^'\"\s]{6,}")
PRIVATE_KEY = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.DOTALL)


def _redact_key_value(match: re.Match[str], replacement: str) -> str:
    return match.group(0).split("=", 1)[0].split(":", 1)[0] + f"={replacement}"


def redact_text(value: str) -> str:
    text = value
    home = str(Path.home())
    if home and home != os.sep:
        text = text.replace(home, "<HOME>")
    text = EMAIL.sub("<EMAIL>", text)
    text = PHONE.sub("<PHONE>", text)
    text = SSN.sub("<SSN>", text)
    text = CREDIT_CARDISH.sub("<CARD_NUMBER>", text)
    text = CUSTOMER_ID.sub(lambda match: _redact_key_value(match, "<CUSTOMER_ID>"), text)
    text = PRIVATE_KEY.sub("<PRIVATE_KEY>", text)
    text = TOKENISH.sub(lambda match: _redact_key_value(match, "<REDACTED>"), text)
    return text


def redact_mapping(value):
    if isinstance(value, dict):
        return {key: redact_mapping(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact_mapping(item) for item in value]
    if isinstance(value, str):
        return redact_text(value)
    return value

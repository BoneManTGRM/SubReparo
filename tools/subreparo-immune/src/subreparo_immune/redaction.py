from __future__ import annotations

import os
import re
from pathlib import Path

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
TOKENISH = re.compile(r"(?i)(api[_-]?key|token|secret|password|passwd|pwd)\s*[:=]\s*['\"]?[^'\"\s]{6,}")
PRIVATE_KEY = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.DOTALL)


def redact_text(value: str) -> str:
    text = value
    home = str(Path.home())
    if home and home != os.sep:
        text = text.replace(home, "<HOME>")
    text = EMAIL.sub("<EMAIL>", text)
    text = PRIVATE_KEY.sub("<PRIVATE_KEY>", text)
    text = TOKENISH.sub(lambda match: match.group(0).split("=", 1)[0].split(":", 1)[0] + "=<REDACTED>", text)
    return text


def redact_mapping(value):
    if isinstance(value, dict):
        return {key: redact_mapping(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact_mapping(item) for item in value]
    if isinstance(value, str):
        return redact_text(value)
    return value

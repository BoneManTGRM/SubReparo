from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

DOMAIN_MEMORY_PATH = Path(".subreparo") / "domain_memory.json"
NETWORK_OBSERVATIONS_PATH = Path(".subreparo") / "network_observations.jsonl"
SCHEMA = "subreparo.network_memory.v1"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _domain(value: str) -> str | None:
    parsed = urlparse(value)
    host = parsed.hostname
    if host:
        return host.lower()
    clean = value.strip().lower()
    if "." in clean and " " not in clean:
        return clean.split("/", 1)[0]
    return None


def read_observations(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"raw": line})
    return rows


def load_memory(path: Path) -> set[str]:
    if not path.exists():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    return set(data.get("known_domains", []))


def build_network_memory(root: Path) -> dict[str, Any]:
    root = root.resolve()
    state = root / ".subreparo"
    observations = read_observations(state / "network_observations.jsonl")
    known = load_memory(state / "domain_memory.json")
    domains: list[str] = []
    dns_statuses: Counter[str] = Counter()
    for item in observations:
        value = str(item.get("domain") or item.get("url") or item.get("remote") or item.get("raw") or "")
        domain = _domain(value)
        if domain:
            domains.append(domain)
        status = item.get("dns_status")
        if status:
            dns_statuses[str(status).lower()] += 1
    counts = Counter(domains)
    new_domains = sorted(set(domains) - known)
    repeated = [
        {"domain": domain, "count": count}
        for domain, count in counts.most_common()
        if count >= 3
    ]
    dns_anomalies = [
        {"status": status, "count": count}
        for status, count in dns_statuses.items()
        if status in {"nxdomain", "servfail", "timeout"} and count >= 3
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": now(),
        "known_domains": sorted(known | set(domains)),
        "new_domains": new_domains,
        "repeated_beaconing_candidates": repeated,
        "dns_anomalies": dns_anomalies,
        "observation_count": len(observations),
    }
    state.mkdir(parents=True, exist_ok=True)
    (state / "domain_memory.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return payload

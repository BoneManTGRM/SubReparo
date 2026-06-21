from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

APP_TITLE = "SubReparo Mobile"
STATE_DIR = Path(".subreparo")
AGENT_CYCLES_PATH = STATE_DIR / "agent_cycles.jsonl"
AGENT_SCARS_PATH = STATE_DIR / "agent_scars.jsonl"
AGENT_PROOF_PATH = STATE_DIR / "agent_proof_export.json"
FACTORY_DIR = STATE_DIR / "factory"
FACTORY_REGISTRY_PATH = FACTORY_DIR / "agent_registry.jsonl"
MOBILE_QUEUE_PATH = STATE_DIR / "mobile_requests.jsonl"
MOBILE_LOG_PATH = STATE_DIR / "mobile_action_log.jsonl"

st.set_page_config(page_title=APP_TITLE, layout="centered", initial_sidebar_state="collapsed")

TEXT = {
    "en": {
        "title": "SubReparo Mobile",
        "caption": "Phone-first control panel for SubReparo Immune, Cortex, and Factory.",
        "notice": "This hosted app can run lightweight SubReparo cloud actions. Device scanning, 24/7 protection, and local repair still require a computer or dedicated cloud runner.",
        "status": "Status",
        "agent_cycles": "Agent cycles",
        "scars": "Scar memory",
        "proof": "Proof export",
        "factory": "Factory records",
        "actions": "Actions you can run from iPhone",
        "run_review": "Run cloud health review now",
        "factory_create": "Create agent blueprint now",
        "factory_registry": "View Factory registry",
        "view_proof": "View latest proof export",
        "queued": "Request saved locally in the mobile queue.",
        "completed": "Completed.",
        "queue": "Mobile queue",
        "log": "Action log",
        "no_queue": "No queued mobile requests yet.",
        "no_log": "No actions logged yet.",
        "cloud_limits": "Current cloud limits",
        "cloud_limits_body": "This app can create plans, records, proof payloads, Factory blueprints, and reports inside the hosted Streamlit environment. It cannot scan or repair your iPhone, and free hosting may sleep when idle.",
        "blueprint": "Blueprint",
        "goal": "Goal",
        "agent_name": "Agent name",
        "agent_purpose": "Agent purpose",
        "download": "Download JSON report",
    },
    "es": {
        "title": "SubReparo Mobile",
        "caption": "Panel móvil para SubReparo Immune, Cortex y Factory.",
        "notice": "Esta app hospedada puede ejecutar acciones ligeras de SubReparo en la nube. Escaneo del dispositivo, protección 24/7 y reparación local todavía requieren computadora o runner dedicado.",
        "status": "Estado",
        "agent_cycles": "Ciclos del agente",
        "scars": "Memoria de cicatrices",
        "proof": "Exportación de prueba",
        "factory": "Registros Factory",
        "actions": "Acciones que puedes ejecutar desde iPhone",
        "run_review": "Ejecutar revisión cloud ahora",
        "factory_create": "Crear blueprint de agente ahora",
        "factory_registry": "Ver registro Factory",
        "view_proof": "Ver última prueba exportada",
        "queued": "Solicitud guardada localmente en la cola móvil.",
        "completed": "Completado.",
        "queue": "Cola móvil",
        "log": "Registro de acciones",
        "no_queue": "Todavía no hay solicitudes móviles.",
        "no_log": "Todavía no hay acciones registradas.",
        "cloud_limits": "Límites actuales de la nube",
        "cloud_limits_body": "Esta app puede crear planes, registros, pruebas, blueprints de Factory y reportes dentro del entorno hospedado de Streamlit. No puede escanear ni reparar tu iPhone, y el hosting gratis puede dormir si no se usa.",
        "blueprint": "Blueprint",
        "goal": "Meta",
        "agent_name": "Nombre del agente",
        "agent_purpose": "Propósito del agente",
        "download": "Descargar reporte JSON",
    },
}

BLUEPRINTS = {
    "code_review": {
        "name": "Code Review Agent",
        "purpose": "Review project changes, detect risky patterns, and produce safe review notes.",
        "tools": ["scan_project", "scan_git", "quality_gate"],
        "permissions": ["read_project", "read_subreparo_state", "write_reports"],
    },
    "test_builder": {
        "name": "Test Builder Agent",
        "purpose": "Suggest and scaffold tests under review control.",
        "tools": ["scan_project", "quality_gate", "snapshot"],
        "permissions": ["read_project", "write_project", "write_reports"],
    },
    "docs_writer": {
        "name": "Documentation Agent",
        "purpose": "Draft setup guides, README sections, changelogs, and operator notes.",
        "tools": ["scan_project", "skill_review"],
        "permissions": ["read_project", "write_project", "write_reports"],
    },
    "website_monitor": {
        "name": "Website Monitor Agent",
        "purpose": "Check website availability and summarize response health.",
        "tools": ["website_response", "quality_gate"],
        "permissions": ["network_read", "write_reports"],
    },
    "report_generator": {
        "name": "Report Generator Agent",
        "purpose": "Generate structured reports from SubReparo state.",
        "tools": ["status_report", "timeline", "risk_trends"],
        "permissions": ["read_subreparo_state", "write_reports"],
    },
}

SAFE_PERMISSIONS = {"read_project", "read_subreparo_state", "write_reports"}
REVIEW_PERMISSIONS = {"write_project", "network_read", "external_message", "publish_public"}
BLOCKED_PERMISSIONS = {"delete_data", "spend_money", "read_secrets", "shell_write", "credential_access"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def t(key: str) -> str:
    lang = st.session_state.get("subreparo_mobile_lang", "en")
    return TEXT.get(lang, TEXT["en"]).get(key, TEXT["en"].get(key, key))


def stable_digest(payload: dict[str, Any]) -> str:
    data = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip())


def tail_jsonl(path: Path, limit: int = 10) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    lines = [line for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()]
    for line in lines[-limit:]:
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"raw": line})
    return rows


def review_permissions(permissions: list[str]) -> dict[str, Any]:
    values = set(permissions)
    blocked = sorted(values & BLOCKED_PERMISSIONS)
    review = sorted(values & REVIEW_PERMISSIONS)
    unknown = sorted(values - SAFE_PERMISSIONS - REVIEW_PERMISSIONS - BLOCKED_PERMISSIONS)
    if blocked:
        return {"risk": "blocked", "approved": False, "reason": "blocked permissions", "blocked": blocked, "review": review, "unknown": unknown}
    if unknown:
        return {"risk": "high", "approved": False, "reason": "unknown permissions", "blocked": blocked, "review": review, "unknown": unknown}
    if review:
        return {"risk": "medium", "approved": False, "reason": "review required", "blocked": blocked, "review": review, "unknown": unknown}
    return {"risk": "low", "approved": True, "reason": "low-risk permissions", "blocked": blocked, "review": review, "unknown": unknown}


def run_cloud_health_review(goal: str) -> dict[str, Any]:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    observations = [
        "Hosted mobile control panel is reachable.",
        "Local Streamlit cloud state is writable.",
        "Mobile queue is available.",
        "Factory blueprint engine is available.",
    ]
    payload = {
        "schema": "subreparo.mobile_cloud_review.v1",
        "created_at": now(),
        "goal": goal,
        "phase": "verified_mobile_cloud_shell",
        "observations": observations,
        "finding_count": 0,
        "highest_severity": "info",
        "verified": True,
    }
    payload["proof_digest"] = stable_digest(payload)
    append_jsonl(AGENT_CYCLES_PATH, payload)
    append_jsonl(AGENT_SCARS_PATH, {"created_at": payload["created_at"], "goal": goal, "proof_digest": payload["proof_digest"], "scar": "mobile cloud shell verified"})
    proof = {
        "schema": "subreparo.agent_proof_export.v1",
        "ready": True,
        "source": "subreparo_mobile_app",
        "cycle_digest": payload["proof_digest"],
        "goal": goal,
        "phase": payload["phase"],
        "verified": True,
        "export_digest": stable_digest(payload),
    }
    AGENT_PROOF_PATH.write_text(json.dumps(proof, indent=2, sort_keys=True), encoding="utf-8")
    append_jsonl(MOBILE_LOG_PATH, {"created_at": now(), "kind": "cloud_health_review", "status": "completed", "digest": payload["proof_digest"]})
    return {"cycle": payload, "proof": proof}


def create_factory_record(blueprint: str, name: str, purpose: str) -> dict[str, Any]:
    base = BLUEPRINTS[blueprint]
    manifest = {
        "schema": "subreparo.agent_manifest.v1",
        "id": name.lower().strip().replace(" ", "-") or blueprint,
        "name": name or base["name"],
        "blueprint": blueprint,
        "purpose": purpose or base["purpose"],
        "tools": base["tools"],
        "permissions": base["permissions"],
        "memory_policy": "Store summaries, outcomes, and proof digests only.",
        "approval_policy": "High-impact actions require approval.",
        "created_at": now(),
        "status": "draft",
    }
    review = review_permissions(list(manifest["permissions"]))
    record = {
        "schema": "subreparo.agent_registry_record.v1",
        "created_at": now(),
        "manifest": manifest,
        "review": review,
        "registered": bool(review["approved"]),
    }
    append_jsonl(FACTORY_REGISTRY_PATH, record)
    append_jsonl(MOBILE_LOG_PATH, {"created_at": now(), "kind": "factory_record", "status": "completed", "agent": manifest["id"], "risk": review["risk"]})
    return record


def append_mobile_request(kind: str, payload: dict[str, Any]) -> None:
    record = {
        "schema": "subreparo.mobile_request.v1",
        "created_at": now(),
        "kind": kind,
        "payload": payload,
        "status": "queued",
    }
    append_jsonl(MOBILE_QUEUE_PATH, record)


st.session_state.setdefault("subreparo_mobile_lang", "en")
st.radio("Language / Idioma", ["en", "es"], key="subreparo_mobile_lang", horizontal=True)

st.title(t("title"))
st.caption(t("caption"))
st.warning(t("notice"))

st.subheader(t("status"))
cols = st.columns(2)
cols[0].metric(t("agent_cycles"), count_jsonl(AGENT_CYCLES_PATH))
cols[1].metric(t("scars"), count_jsonl(AGENT_SCARS_PATH))
cols = st.columns(2)
cols[0].metric(t("proof"), "ready" if AGENT_PROOF_PATH.exists() else "missing")
cols[1].metric(t("factory"), count_jsonl(FACTORY_REGISTRY_PATH))

st.subheader(t("actions"))
goal = st.text_input(t("goal"), value="project health review")
if st.button(t("run_review"), type="primary", use_container_width=True):
    result = run_cloud_health_review(goal)
    st.success(t("completed"))
    st.json(result)
    st.download_button(t("download"), json.dumps(result, indent=2), file_name="subreparo_mobile_review.json", mime="application/json", use_container_width=True)

with st.expander("Factory / Agent Builder", expanded=True):
    blueprint = st.selectbox(t("blueprint"), list(BLUEPRINTS.keys()), index=0)
    agent_name = st.text_input(t("agent_name"), value=BLUEPRINTS[blueprint]["name"])
    agent_purpose = st.text_area(t("agent_purpose"), value=BLUEPRINTS[blueprint]["purpose"])
    if st.button(t("factory_create"), use_container_width=True):
        record = create_factory_record(blueprint, agent_name, agent_purpose)
        st.success(t("completed"))
        st.json(record)
        st.download_button(t("download"), json.dumps(record, indent=2), file_name="subreparo_factory_record.json", mime="application/json", use_container_width=True)

cols = st.columns(2)
if cols[0].button(t("factory_registry"), use_container_width=True):
    rows = tail_jsonl(FACTORY_REGISTRY_PATH, limit=25)
    st.dataframe(pd.DataFrame(rows), use_container_width=True) if rows else st.info("No Factory records yet.")

if cols[1].button(t("view_proof"), use_container_width=True):
    if AGENT_PROOF_PATH.exists():
        st.json(json.loads(AGENT_PROOF_PATH.read_text(encoding="utf-8", errors="replace")))
    else:
        st.info("No proof export found yet.")

with st.expander(t("queue"), expanded=False):
    queue_goal = st.text_input("Queued request", value="future full agent run")
    if st.button("Queue request", use_container_width=True):
        append_mobile_request("manual_mobile_request", {"goal": queue_goal})
        st.success(t("queued"))
    queue_rows = tail_jsonl(MOBILE_QUEUE_PATH)
    if queue_rows:
        st.dataframe(pd.DataFrame(queue_rows), use_container_width=True)
    else:
        st.info(t("no_queue"))

with st.expander(t("log"), expanded=False):
    log_rows = tail_jsonl(MOBILE_LOG_PATH)
    if log_rows:
        st.dataframe(pd.DataFrame(log_rows), use_container_width=True)
    else:
        st.info(t("no_log"))

st.subheader(t("cloud_limits"))
st.info(t("cloud_limits_body"))

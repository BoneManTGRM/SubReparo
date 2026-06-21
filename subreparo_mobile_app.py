from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

APP_TITLE = "SubReparo Mobile"
STATE_DIR = Path(".subreparo")
AGENT_CYCLES_PATH = STATE_DIR / "agent_cycles.jsonl"
AGENT_SCARS_PATH = STATE_DIR / "agent_scars.jsonl"
AGENT_PROOF_PATH = STATE_DIR / "agent_proof_export.json"
FACTORY_REGISTRY_PATH = STATE_DIR / "factory" / "agent_registry.jsonl"

st.set_page_config(page_title=APP_TITLE, layout="centered", initial_sidebar_state="collapsed")

TEXT = {
    "en": {
        "title": "SubReparo Mobile",
        "caption": "Phone-first control panel for SubReparo Immune, Cortex, and Factory.",
        "notice": "This mobile app is a dashboard/control shell. Full local agent execution still needs a computer or cloud runner.",
        "status": "Status",
        "agent_cycles": "Agent cycles",
        "scars": "Scar memory",
        "proof": "Proof export",
        "factory": "Factory records",
        "actions": "Mobile actions",
        "project_review": "Request project health review",
        "factory_plan": "Create agent-factory request",
        "view_proof": "View latest proof export",
        "queued": "Request saved locally in the mobile queue.",
        "queue": "Mobile queue",
        "no_queue": "No queued mobile requests yet.",
        "next": "Next step",
        "next_body": "Deploy this file as a Streamlit app, then open the Streamlit URL on your iPhone. Connect it to a cloud runner later for real execution.",
    },
    "es": {
        "title": "SubReparo Mobile",
        "caption": "Panel móvil para SubReparo Immune, Cortex y Factory.",
        "notice": "Esta app móvil es un panel de control. La ejecución completa del agente todavía necesita una computadora o runner en la nube.",
        "status": "Estado",
        "agent_cycles": "Ciclos del agente",
        "scars": "Memoria de cicatrices",
        "proof": "Exportación de prueba",
        "factory": "Registros Factory",
        "actions": "Acciones móviles",
        "project_review": "Solicitar revisión del proyecto",
        "factory_plan": "Crear solicitud de Agent Factory",
        "view_proof": "Ver última prueba exportada",
        "queued": "Solicitud guardada localmente en la cola móvil.",
        "queue": "Cola móvil",
        "no_queue": "Todavía no hay solicitudes móviles.",
        "next": "Siguiente paso",
        "next_body": "Despliega este archivo como app de Streamlit y abre el URL en tu iPhone. Después se conecta a un runner en la nube para ejecución real.",
    },
}


def t(key: str) -> str:
    lang = st.session_state.get("subreparo_mobile_lang", "en")
    return TEXT.get(lang, TEXT["en"]).get(key, TEXT["en"].get(key, key))


def count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip())


def tail_jsonl(path: Path, limit: int = 10) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    lines = [line for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()]
    for line in lines[-limit:]:
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"raw": line})
    return rows


def append_mobile_request(kind: str, payload: dict) -> None:
    queue_path = STATE_DIR / "mobile_requests.jsonl"
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "schema": "subreparo.mobile_request.v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "kind": kind,
        "payload": payload,
        "status": "queued",
    }
    with queue_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")


st.session_state.setdefault("subreparo_mobile_lang", "en")
lang = st.radio("Language / Idioma", ["en", "es"], key="subreparo_mobile_lang", horizontal=True)

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
project_goal = st.text_input("Goal / Meta", value="project health review")
if st.button(t("project_review"), type="primary", use_container_width=True):
    append_mobile_request("agent_cycle", {"goal": project_goal})
    st.success(t("queued"))

agent_idea = st.text_input("Agent idea / Idea de agente", value="code review agent")
if st.button(t("factory_plan"), use_container_width=True):
    append_mobile_request("agent_factory", {"idea": agent_idea})
    st.success(t("queued"))

if st.button(t("view_proof"), use_container_width=True):
    if AGENT_PROOF_PATH.exists():
        try:
            st.json(json.loads(AGENT_PROOF_PATH.read_text(encoding="utf-8", errors="replace")))
        except json.JSONDecodeError:
            st.code(AGENT_PROOF_PATH.read_text(encoding="utf-8", errors="replace"))
    else:
        st.info("No proof export found yet.")

st.subheader(t("queue"))
queue_rows = tail_jsonl(STATE_DIR / "mobile_requests.jsonl")
if queue_rows:
    st.dataframe(queue_rows, use_container_width=True)
else:
    st.info(t("no_queue"))

st.subheader(t("next"))
st.info(t("next_body"))

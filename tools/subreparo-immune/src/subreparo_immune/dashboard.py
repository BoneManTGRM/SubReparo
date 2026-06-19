from __future__ import annotations

import html
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

from .agent_components import build_agent_component_report
from .approval_queue import pending_approvals
from .quarantine import list_records
from .status_report import build_status_report
from .swarm_orchestrator import list_swarm_plans
from .swarm_roles import swarm_role_catalog
from .swarm_tools import swarm_tool_catalog
from .watcher import build_watch_plan

REPORT_PATH = Path(".subreparo") / "report.md"
EXPORT_PATH = Path(".subreparo") / "chain_export.json"
LEDGER_PATH = Path(".subreparo") / "repair_ledger.jsonl"
ALERTS_PATH = Path(".subreparo") / "watch_alerts.jsonl"
QUALITY_PATH = Path(".subreparo") / "quality_report.json"
TRUST_PATH = Path(".subreparo") / "trust_report.json"
SIGNATURE_PATH = Path(".subreparo") / "report_signature.json"
SETUP_PROFILE_PATH = Path(".subreparo") / "setup_profile.json"
FEEDBACK_PATH = Path(".subreparo") / "feedback.json"
SNAPSHOT_MANIFEST_PATH = Path(".subreparo") / "snapshots" / "snapshot_manifest.jsonl"
STATE_DIR = Path(".subreparo")


def read_text(path: Path, fallback: str) -> str:
    if not path.exists():
        return fallback
    return path.read_text(encoding="utf-8", errors="replace")


def count_lines(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip())


def tail_jsonl(path: Path, limit: int = 8) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    lines = [line for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()]
    for line in lines[-limit:]:
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            row = {"unreadable": line}
        rows.append(row)
    return rows


def render_json_file(path: Path, fallback: str) -> str:
    if not path.exists():
        return fallback
    try:
        payload = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")
    return json.dumps(payload, indent=2, sort_keys=True)


def render_quarantine() -> str:
    records = list_records(STATE_DIR)
    if not records:
        return "No staged files found."
    lines: list[str] = []
    for index, record in enumerate(records):
        lines.append(f"[{index}] {record.staged_path}")
        lines.append(f"  Original: {record.original_path}")
        lines.append(f"  Reason: {record.reason}")
    return "\n".join(lines)


def render_status_report() -> str:
    payload = build_status_report(Path("."))
    return json.dumps(payload, indent=2, sort_keys=True)


def render_agent_components() -> str:
    payload = build_agent_component_report(Path("."))
    return json.dumps(payload, indent=2, sort_keys=True)


def render_watch_plan() -> str:
    payload = build_watch_plan(Path("."))
    return json.dumps(payload, indent=2, sort_keys=True)


def render_approvals() -> str:
    approvals = pending_approvals(STATE_DIR / "approval_queue.jsonl")
    if not approvals:
        return "No pending approvals."
    lines: list[str] = []
    for approval in approvals[:8]:
        task = approval.task
        lines.append(f"- {task.get('title', 'Untitled task')}")
        lines.append(f"  Level: {approval.approval_level}")
        lines.append(f"  Reason: {approval.reason}")
        lines.append(f"  Created: {approval.created_at}")
    return "\n".join(lines)


def render_snapshots() -> str:
    snapshots = tail_jsonl(SNAPSHOT_MANIFEST_PATH, limit=5)
    if not snapshots:
        return "No snapshots found."
    return json.dumps(snapshots, indent=2, sort_keys=True)


def render_swarm_catalog() -> str:
    payload = {"roles": swarm_role_catalog(), "tools": swarm_tool_catalog()}
    return json.dumps(payload, indent=2, sort_keys=True)


def render_swarm_plans() -> str:
    plans = list_swarm_plans(Path("."))
    if not plans:
        return "No swarm plans found. Run `subreparo-cortex . --orchestrate \"run quality checks\" --json`."
    return json.dumps(plans[-10:], indent=2, sort_keys=True)


def render_page() -> str:
    report = html.escape(read_text(REPORT_PATH, "No report found. Run `subreparo-immune run .` first."))
    export = html.escape(read_text(EXPORT_PATH, "No chain export found."))
    alerts = html.escape(read_text(ALERTS_PATH, "No monitor alerts found."))
    quality = html.escape(render_json_file(QUALITY_PATH, "No quality report found. Run `subreparo-immune quality .`."))
    trust = html.escape(render_json_file(TRUST_PATH, "No trust report found. Run `subreparo-immune trust .`."))
    signature = html.escape(render_json_file(SIGNATURE_PATH, "No report signature found. Run `subreparo-immune sign-report .`."))
    setup = html.escape(render_json_file(SETUP_PROFILE_PATH, "No setup profile found. Run `subreparo-immune setup .`."))
    feedback = html.escape(render_json_file(FEEDBACK_PATH, "No feedback file found. Run `subreparo-immune feedback .`."))
    watch_plan = html.escape(render_watch_plan())
    quarantine = html.escape(render_quarantine())
    cortex_status = html.escape(render_status_report())
    agent_components = html.escape(render_agent_components())
    approvals = html.escape(render_approvals())
    snapshots = html.escape(render_snapshots())
    swarm_catalog = html.escape(render_swarm_catalog())
    swarm_plans = html.escape(render_swarm_plans())
    ledger_count = count_lines(LEDGER_PATH)
    alert_count = count_lines(ALERTS_PATH)
    quarantine_count = len(list_records(STATE_DIR))
    status_payload = build_status_report(Path("."))
    component_payload = build_agent_component_report(Path("."))
    swarm_plan_count = len(list_swarm_plans(Path(".")))
    role_count = len(swarm_role_catalog())
    tool_count = len(swarm_tool_catalog())
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SubReparo Control Center</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 0; background: #0f1115; color: #f5f7fb; }}
    header {{ padding: 24px; background: #171b24; border-bottom: 1px solid #2c3342; }}
    main {{ padding: 24px; max-width: 1200px; margin: 0 auto; }}
    .tabs > input {{ position: absolute; opacity: 0; pointer-events: none; }}
    .tab-labels {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 18px; }}
    .tab-labels label {{ cursor: pointer; padding: 10px 14px; background: #171b24; border: 1px solid #2c3342; border-radius: 999px; }}
    .tab-panel {{ display: none; }}
    .panel-grid {{ display: grid; gap: 20px; }}
    .card {{ background: #171b24; border: 1px solid #2c3342; border-radius: 14px; padding: 18px; }}
    pre {{ white-space: pre-wrap; overflow-wrap: anywhere; background: #0b0d12; padding: 14px; border-radius: 10px; }}
    .metric {{ display: inline-block; margin-right: 18px; margin-bottom: 10px; padding: 10px 14px; background: #222838; border-radius: 10px; }}
    .swarm-map {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; margin: 12px 0; }}
    .swarm-node {{ padding: 12px; border: 1px solid #39445c; background: #202638; border-radius: 12px; text-align: center; }}
    #tab-overview:checked ~ .tab-panels #panel-overview,
    #tab-cortex:checked ~ .tab-panels #panel-cortex,
    #tab-swarms:checked ~ .tab-panels #panel-swarms,
    #tab-components:checked ~ .tab-panels #panel-components,
    #tab-protection:checked ~ .tab-panels #panel-protection,
    #tab-reports:checked ~ .tab-panels #panel-reports {{ display: block; }}
  </style>
</head>
<body>
<header>
  <h1>SubReparo Control Center</h1>
  <p>Local-first autonomous repair, swarm orchestration, and protection dashboard. Bound to localhost by default.</p>
</header>
<main>
  <div class="tabs" aria-label="Dashboard tabs">
    <input id="tab-overview" type="radio" name="dashboard-tabs" checked>
    <input id="tab-cortex" type="radio" name="dashboard-tabs">
    <input id="tab-swarms" type="radio" name="dashboard-tabs">
    <input id="tab-components" type="radio" name="dashboard-tabs">
    <input id="tab-protection" type="radio" name="dashboard-tabs">
    <input id="tab-reports" type="radio" name="dashboard-tabs">
    <nav class="tab-labels" aria-label="Dashboard tabs">
      <label for="tab-overview">Overview</label>
      <label for="tab-cortex">Cortex</label>
      <label for="tab-swarms">Swarms</label>
      <label for="tab-components">Agent components</label>
      <label for="tab-protection">Protection</label>
      <label for="tab-reports">Reports</label>
    </nav>
    <div class="tab-panels">
      <section id="panel-overview" class="tab-panel">
        <div class="panel-grid">
          <article class="card">
            <h2>Status</h2>
            <div class="metric">Ledger records: {ledger_count}</div>
            <div class="metric">Alerts: {alert_count}</div>
            <div class="metric">Quarantine: {quarantine_count}</div>
            <div class="metric">Swarm plans: {swarm_plan_count}</div>
            <div class="metric">Report: {"present" if REPORT_PATH.exists() else "missing"}</div>
            <div class="metric">Chain export: {"present" if EXPORT_PATH.exists() else "missing"}</div>
          </article>
          <article class="card">
            <h2>Setup profile</h2>
            <pre>{setup}</pre>
          </article>
        </div>
      </section>
      <section id="panel-cortex" class="tab-panel">
        <div class="panel-grid">
          <article class="card">
            <h2>Cortex control layer</h2>
            <div class="metric">Tasks: {status_payload["task_count"]}</div>
            <div class="metric">Memory: {status_payload["memory_count"]}</div>
            <div class="metric">Approvals: {status_payload["pending_approvals"]}</div>
            <div class="metric">Outcomes: {status_payload["outcome_count"]}</div>
            <pre>{cortex_status}</pre>
          </article>
          <article class="card">
            <h2>Pending approvals</h2>
            <pre>{approvals}</pre>
          </article>
          <article class="card">
            <h2>Snapshots</h2>
            <pre>{snapshots}</pre>
          </article>
        </div>
      </section>
      <section id="panel-swarms" class="tab-panel">
        <div class="panel-grid">
          <article class="card">
            <h2>Live swarm map</h2>
            <div class="metric">Roles: {role_count}</div>
            <div class="metric">Tools: {tool_count}</div>
            <div class="metric">Saved plans: {swarm_plan_count}</div>
            <div class="swarm-map">
              <div class="swarm-node">Planner</div>
              <div class="swarm-node">Sentinel</div>
              <div class="swarm-node">Builder</div>
              <div class="swarm-node">Tester</div>
              <div class="swarm-node">Reviewer</div>
              <div class="swarm-node">Archivist</div>
            </div>
            <p>Goal → route → role → bounded tools → approval requirement → saved plan.</p>
          </article>
          <article class="card">
            <h2>Saved swarm plans</h2>
            <pre>{swarm_plans}</pre>
          </article>
          <article class="card">
            <h2>Swarm roles and tools</h2>
            <pre>{swarm_catalog}</pre>
          </article>
        </div>
      </section>
      <section id="panel-components" class="tab-panel">
        <div class="panel-grid">
          <article class="card">
            <h2>AI agent components</h2>
            <div class="metric">Registered: {component_payload["registered_count"]}</div>
            <div class="metric">Operational: {component_payload["operational_count"]}</div>
            <pre>{agent_components}</pre>
          </article>
        </div>
      </section>
      <section id="panel-protection" class="tab-panel">
        <div class="panel-grid">
          <article class="card"><h2>Trust report</h2><pre>{trust}</pre></article>
          <article class="card"><h2>False-positive feedback</h2><pre>{feedback}</pre></article>
          <article class="card"><h2>Watch plan</h2><pre>{watch_plan}</pre></article>
          <article class="card"><h2>Quarantine</h2><pre>{quarantine}</pre></article>
          <article class="card"><h2>Monitor alerts</h2><pre>{alerts}</pre></article>
        </div>
      </section>
      <section id="panel-reports" class="tab-panel">
        <div class="panel-grid">
          <article class="card"><h2>Quality gate</h2><pre>{quality}</pre></article>
          <article class="card"><h2>Report signature</h2><pre>{signature}</pre></article>
          <article class="card"><h2>Latest report</h2><pre>{report}</pre></article>
          <article class="card"><h2>Chain export preview</h2><pre>{export}</pre></article>
        </div>
      </section>
    </div>
  </div>
</main>
</body>
</html>"""


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path not in {"/", "/index.html"}:
            self.send_response(404)
            self.end_headers()
            return
        body = render_page().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


def serve(host: str = "127.0.0.1", port: int = 8765) -> None:
    if host not in {"127.0.0.1", "localhost"}:
        raise ValueError("Dashboard must bind to localhost unless the code is reviewed and changed intentionally.")
    server = HTTPServer((host, port), DashboardHandler)
    print(f"SubReparo dashboard running at http://{host}:{port}")
    server.serve_forever()

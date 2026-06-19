from __future__ import annotations

import html
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from .quarantine import list_records

REPORT_PATH = Path(".subreparo") / "report.md"
EXPORT_PATH = Path(".subreparo") / "chain_export.json"
LEDGER_PATH = Path(".subreparo") / "repair_ledger.jsonl"
ALERTS_PATH = Path(".subreparo") / "watch_alerts.jsonl"
STATE_DIR = Path(".subreparo")


def read_text(path: Path, fallback: str) -> str:
    if not path.exists():
        return fallback
    return path.read_text(encoding="utf-8", errors="replace")


def count_lines(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip())


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


def render_page() -> str:
    report = html.escape(read_text(REPORT_PATH, "No report found. Run `subreparo-immune run .` first."))
    export = html.escape(read_text(EXPORT_PATH, "No chain export found."))
    alerts = html.escape(read_text(ALERTS_PATH, "No monitor alerts found."))
    quarantine = html.escape(render_quarantine())
    ledger_count = count_lines(LEDGER_PATH)
    alert_count = count_lines(ALERTS_PATH)
    quarantine_count = len(list_records(STATE_DIR))
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SubReparo Immune</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 0; background: #0f1115; color: #f5f7fb; }}
    header {{ padding: 24px; background: #171b24; border-bottom: 1px solid #2c3342; }}
    main {{ padding: 24px; display: grid; gap: 20px; max-width: 1100px; margin: 0 auto; }}
    section {{ background: #171b24; border: 1px solid #2c3342; border-radius: 14px; padding: 18px; }}
    pre {{ white-space: pre-wrap; overflow-wrap: anywhere; background: #0b0d12; padding: 14px; border-radius: 10px; }}
    .metric {{ display: inline-block; margin-right: 18px; margin-bottom: 10px; padding: 10px 14px; background: #222838; border-radius: 10px; }}
  </style>
</head>
<body>
<header>
  <h1>SubReparo Immune</h1>
  <p>Local-first project repair dashboard. Bound to localhost by default.</p>
</header>
<main>
  <section>
    <h2>Status</h2>
    <div class="metric">Ledger records: {ledger_count}</div>
    <div class="metric">Alerts: {alert_count}</div>
    <div class="metric">Quarantine: {quarantine_count}</div>
    <div class="metric">Report: {"present" if REPORT_PATH.exists() else "missing"}</div>
    <div class="metric">Chain export: {"present" if EXPORT_PATH.exists() else "missing"}</div>
  </section>
  <section>
    <h2>Quarantine</h2>
    <pre>{quarantine}</pre>
  </section>
  <section>
    <h2>Monitor alerts</h2>
    <pre>{alerts}</pre>
  </section>
  <section>
    <h2>Latest report</h2>
    <pre>{report}</pre>
  </section>
  <section>
    <h2>Chain export preview</h2>
    <pre>{export}</pre>
  </section>
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

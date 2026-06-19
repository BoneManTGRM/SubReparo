from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PDF_REPORT_PATH = Path(".subreparo") / "report.pdf"
SCHEMA = "subreparo.pdf_report.v1"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _plain_lines(markdown: str) -> list[str]:
    lines: list[str] = []
    for line in markdown.splitlines():
        clean = re.sub(r"[`*_#]", "", line).strip()
        if clean:
            lines.append(clean[:110])
    return lines or ["SubReparo report is empty."]


def _escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _pdf_bytes(lines: list[str]) -> bytes:
    text_ops = ["BT", "/F1 10 Tf", "50 780 Td", "14 TL"]
    for line in lines[:52]:
        text_ops.append(f"({_escape_pdf_text(line)}) Tj")
        text_ops.append("T*")
    text_ops.append("ET")
    stream = "\n".join(text_ops).encode("latin-1", errors="replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    output = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{index} 0 obj\n".encode("ascii"))
        output.extend(obj)
        output.extend(b"\nendobj\n")
    xref_offset = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )
    return bytes(output)


def create_pdf_report(root: Path) -> dict[str, Any]:
    root = root.resolve()
    state = root / ".subreparo"
    markdown_path = state / "report.md"
    markdown = markdown_path.read_text(encoding="utf-8", errors="replace") if markdown_path.exists() else "# SubReparo Report\nNo report found."
    lines = _plain_lines(markdown)
    output = root / PDF_REPORT_PATH
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(_pdf_bytes(lines))
    return {
        "schema": SCHEMA,
        "generated_at": now(),
        "path": str(output),
        "source": str(markdown_path),
        "line_count": len(lines),
    }

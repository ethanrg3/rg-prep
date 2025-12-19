"""Stub PDF parser utilities.

Replace these stubs with real extraction using PyMuPDF/pdfplumber and OCR.
The API here is intentionally small so the rest of the system can call it
without depending on heavy packages until you're ready to add them.
"""

from pathlib import Path
import json


def parse_pdf_stub(pdf_path: str | Path) -> dict:
    """Return a minimal parsed representation for the given PDF.

    This does NOT perform real text extraction. It's a placeholder so the
    ingestion CLI can produce consistent JSON records until a real parser
    is implemented.
    """
    p = Path(pdf_path)
    return {
        "source_filename": p.name,
        "pages": p.stat().st_size if p.exists() else 0,
        "parsed_at": None,
        "questions": [],
        "notes": "stub parser — implement real extraction using PyMuPDF/pdfplumber",
    }


def write_parsed_json(parsed: dict, out_path: str | Path) -> None:
    Path(out_path).write_text(json.dumps(parsed, indent=2))

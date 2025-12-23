"""
PDF ingestion helpers using PyMuPDF (fitz).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import fitz

def extract_pages(pdf_path: Path) -> list[dict[str, Any]]:
    """Extract plain text from each page of a PDF.

    Args:
        pdf_path: Path to a PDF file.

    Returns:
        A list of page records with keys: page_number, text, source_pdf.

    Raises:
        FileNotFoundError: if pdf_path does not exist.
        RuntimeError: if the PDF cannot be opened or read.
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:  # pragma: no cover
        # PyMuPDF raises several exception types; normalize for callers.
        raise RuntimeError(f"Failed to open PDF: {pdf_path}") from e

    pages: list[dict[str, Any]] = []

    for page_index, page in enumerate(doc):
        text = page.get_text("text")
        pages.append(
            {
                "page_number": page_index + 1,
                "text": text,
                "source_pdf": pdf_path.name,
            }
        )

    return pages


def save_extraction(pages: list[dict[str, Any]], out_path: Path) -> Path:
    """Persist extracted pages to JSON.

    Args:
        pages: Output of extract_pages.
        out_path: Where to write JSON.

    Returns:
        The path written.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(pages, indent=2), encoding="utf-8")
    return out_path


def default_output_path(pdf_path: Path, extracted_root: Path) -> Path:
    """Compute a default JSON output path for a given PDF.

    Example:
        default_output_path(Path('.../J08_ACT.pdf'), Path('data/extracted'))
        -> data/extracted/J08_ACT.json
    """
    return extracted_root / f"{pdf_path.stem}.json"


if __name__ == "__main__":
    # Minimal manual runner for local debugging.
    # Usage from apps/api (repo-relative):
    #   poetry run python -m app.ingestion.pdf_parser
    repo_root = Path(__file__).resolve().parents[4]
    pdf_path = repo_root / "data" / "raw-pdfs" / "act" / "J08_ACT.pdf"
    extracted_root = repo_root / "data" / "extracted"

    pages = extract_pages(pdf_path)
    out_path = save_extraction(pages, default_output_path(pdf_path, extracted_root))

    # Keep prints ONLY in the CLI/runner (not in library functions)
    print(f"Extracted {len(pages)} pages from {pdf_path.name}")
    print(f"Wrote JSON to {out_path}")
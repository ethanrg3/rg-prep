"""
Module for parsing ACT PDFs and extracting relevant sections, pages, and questions with assets.
"""

import re
from pathlib import Path

from pdfminer.high_level import extract_pages


def collect_act_pdf(form_id: str) -> Path:
    # Collect ACT PDFs from the repository data folder
    form_id = form_id.upper()
    project_root = Path(__file__).resolve().parents[4]
    pdf_dir = project_root / "data" / "raw-pdfs" / "act"
    pdf_path = pdf_dir / f"{form_id}_ACT.pdf"
    return pdf_path


def normalize(text: str) -> str:
    """Normalize text by converting to uppercase, collapsing whitespace, and stripping leading/trailing spaces."""
    return re.sub(r"\s+", " ", text.upper()).strip()


def extract_raw_text_from_act(form_id: str) -> None:
    pdf_path = collect_act_pdf(form_id)
    print(f"Processing PDF: {pdf_path}")

    for page_layout in extract_pages(pdf_path):
        print(f"Processing Page: {page_layout.pageid}")
        for element in page_layout:
            if hasattr(element, "get_text"):
                text = element.get_text()
                normalized_text = normalize(text)
                print(normalized_text)
        breakpoint()
        # TODO: Implement text processing and storage logic here


# some testing
if __name__ == "__main__":
    test_form_id = "j08"
    extract_raw_text_from_act(test_form_id)

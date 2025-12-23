"""
Simple CLI to ingest PDFs into the project's data folders.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from app.ingestion.pdf_parser import extract_pages, save_extraction


ROOT = Path(__file__).resolve().parents[4]
DATA_RAW = ROOT / "data" / "raw-pdfs"
DATA_EXTRACTED = ROOT / "data" / "extracted"


def ensure_dirs() -> None:
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    DATA_EXTRACTED.mkdir(parents=True, exist_ok=True)


def ingest_single_pdf(pdf_path: Path) -> None:
    """
    Ingests a single PDF file from the data/raw-pdfs directory and saves the extracted pages to the data/extracted directory.
    """
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)
    
    # extract pages from PDF
    pages = extract_pages(pdf_path)
    print(f"Extracted {len(pages)} pages from {pdf_path.name}")

    # save extracted pages to data/extracted
    save_extraction(pages, DATA_EXTRACTED / f"{pdf_path.stem}.json")
    print(f"Saved extracted pages to {DATA_EXTRACTED / f'{pdf_path.stem}.json'}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest PDFs into the project's data folders.")
    parser.add_argument("pdf_path", type=Path, help="Path to the PDF file to ingest.")
    args = parser.parse_args()

    ensure_dirs()
    ingest_single_pdf(args.pdf_path)

if __name__ == "__main__":
    print(f'Testing ingest_single_pdf with {DATA_RAW / "act" / "25MC5_ACT.pdf"}')
    ingest_single_pdf(DATA_RAW / "act" / "25MC5_ACT.pdf")
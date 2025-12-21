"""
PDF parser using PyMuPDF (fitz)
"""
import fitz
from pathlib import Path

PDF_PATH = Path(__file__).resolve().parents[4] / "data" / "raw-pdfs" / "act" / "J08_ACT.pdf"

print(f"Loading PDF from {PDF_PATH}")

doc = fitz.open(PDF_PATH)

print(f"Loaded PDF with {doc.page_count} pages")
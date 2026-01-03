from pathlib import Path

from pdfminer.high_level import extract_pages

# Collect ACT PDFs from the repository data folder
project_root = Path(__file__).resolve().parents[4]
pdf_dir = project_root / "data" / "raw-pdfs" / "act"
pdf_paths = [str(path) for path in pdf_dir.glob("*.pdf")]

for pdf in pdf_paths:
    print(f"Processing PDF: {pdf}")
    for page_layout in extract_pages(pdf):
        for element in page_layout:
            if hasattr(element, "get_text"):
                text = element.get_text()
                # TODO: Implement text processing and storage logic here

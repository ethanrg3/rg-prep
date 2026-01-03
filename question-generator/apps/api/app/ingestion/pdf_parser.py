from pdfminer.high_level import extract_pages

# TODO: Load ACT PDF paths from directory
pdf_paths: list[str] = []

for pdf in pdf_paths:
    for page_layout in extract_pages(pdf):
        for element in page_layout:
            if hasattr(element, "get_text"):
                text = element.get_text()

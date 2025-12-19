# question-generator-api — local dev README

This minimal scaffold provides CLI-first tooling for ingesting PDFs and producing placeholder parsed JSON for downstream templating and generation.

Quick start (CLI-first)

- Put sample PDFs here: `data/raw_pdfs/`
- Run the ingestion script to register PDFs and create initial parsed JSON records:

```bash
cd apps/api
python -m app.scripts.ingest_batch --input ../../data/raw_pdfs/my_act_sample.pdf
```

What the scaffold provides
- `app/scripts/ingest_batch.py`: CLI that copies PDFs into the project `data/raw_pdfs/` directory and writes a small placeholder parsed JSON into `data/parsed/` for each file.
- `app/ingestion/pdf_parser.py`: stub parser to be replaced with real extraction (PyMuPDF/pdfplumber + OCR) later.

Next steps
- Add sample ACT/SAT PDFs to `data/raw_pdfs/` and re-run the ingest script.
- Replace `pdf_parser.parse_pdf` implementation with a real extractor once dependencies are available.

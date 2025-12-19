"""Simple CLI to ingest PDFs into the project's data folders.

This is intentionally dependency-free (uses only Python stdlib) so you can run
it immediately. It copies provided PDF(s) into `data/raw_pdfs/` and creates a
small placeholder JSON file under `data/parsed/` for each PDF.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from datetime import datetime


ROOT = Path(__file__).resolve().parents[3]
DATA_RAW = ROOT / "data" / "raw_pdfs"
DATA_PARSED = ROOT / "data" / "parsed"


def ensure_dirs() -> None:
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    DATA_PARSED.mkdir(parents=True, exist_ok=True)


def ingest_file(pdf_path: Path) -> dict:
    """Copy a PDF into data/raw_pdfs and create placeholder parsed metadata.

    Returns the parsed metadata dict written to data/parsed/{stem}.json
    """
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)

    dest = DATA_RAW / pdf_path.name
    shutil.copy2(pdf_path, dest)

    # Placeholder parsed content — replace with real parsing later
    parsed = {
        "source_filename": pdf_path.name,
        "imported_at": datetime.utcnow().isoformat() + "Z",
        "notes": "placeholder parsed record — replace with real parser",
        "questions": [],
    }

    out_json = DATA_PARSED / (pdf_path.stem + ".json")
    out_json.write_text(json.dumps(parsed, indent=2))

    return parsed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ingest PDF(s) into data/raw_pdfs")
    parser.add_argument("--input", "-i", required=True, nargs='+', help="Path(s) to PDF files")
    args = parser.parse_args(argv)

    ensure_dirs()

    for p in args.input:
        path = Path(p)
        try:
            parsed = ingest_file(path)
            print(f"Ingested: {path} -> {DATA_RAW / path.name}")
            print(f"Wrote parsed JSON: data/parsed/{path.stem}.json")
        except Exception as exc:
            print(f"Failed to ingest {path}: {exc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

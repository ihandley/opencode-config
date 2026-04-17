from pathlib import Path
from typing import Any, Dict

from pypdf import PdfReader


def read_resume_pdf(path: str) -> Dict[str, Any]:
    pdf_path = Path(path)

    if not pdf_path.exists():
        return {
            "ok": False,
            "path": path,
            "text": "",
            "page_count": 0,
            "error": f"File not found: {path}",
        }

    try:
        reader = PdfReader(str(pdf_path))
        pages = []

        for page in reader.pages:
            page_text = page.extract_text() or ""
            pages.append(page_text.strip())

        text = "\n\n".join(p for p in pages if p).strip()

        return {
            "ok": True,
            "path": str(pdf_path),
            "text": text,
            "page_count": len(reader.pages),
            "error": "",
        }
    except Exception as e:
        return {
            "ok": False,
            "path": path,
            "text": "",
            "page_count": 0,
            "error": str(e),
        }
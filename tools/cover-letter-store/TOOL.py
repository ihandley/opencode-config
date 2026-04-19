from pathlib import Path
from typing import Any, Dict
import re


BASE_DIR = Path.home() / "code" / "github" / "opencode" / "data" / "job-coach"


def _slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def save_cover_letter(
    company: str,
    title: str,
    cover_letter: str,
) -> Dict[str, Any]:
    company_slug = _slugify(company or "unknown-company")
    company_dir = BASE_DIR / company_slug
    company_dir.mkdir(parents=True, exist_ok=True)

    title_slug = _slugify(title or "unknown-role")
    filename = f"cover-letter-{title_slug}.md"
    path = company_dir / filename

    content = f"# {company} — {title}\n\n## Cover Letter\n\n{cover_letter.strip()}\n"
    path.write_text(content, encoding="utf-8")

    return {
        "ok": True,
        "path": str(path),
        "filename": filename,
        "company": company,
        "title": title,
        "error": "",
    }


def list_cover_letters() -> Dict[str, Any]:
    files = []
    for company_dir in BASE_DIR.iterdir():
        if company_dir.is_dir():
            files.extend(str(p) for p in company_dir.glob("cover-letter-*.md"))
    return {"ok": True, "files": sorted(files), "error": ""}
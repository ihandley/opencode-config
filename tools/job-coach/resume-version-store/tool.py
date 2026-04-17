import re
from pathlib import Path
from typing import Any, Dict


BASE_DIR = Path.home() / "code" / "github" / "opencode" / "data" / "job-coach"


def _slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def save_resume_version(
    company: str,
    title: str,
    tailored_resume: str,
    summary_rewrite: str = "",
) -> Dict[str, Any]:
    company_slug = _slugify(company or "unknown-company")
    company_dir = BASE_DIR / company_slug
    company_dir.mkdir(parents=True, exist_ok=True)

    title_slug = _slugify(title or "unknown-role")
    filename = f"resume-{title_slug}.md"
    path = company_dir / filename

    content = f"# {company} — {title}\n\n"

    if summary_rewrite:
        content += "## Summary Rewrite\n\n"
        content += f"{summary_rewrite}\n\n"

    content += "## Tailored Resume\n\n"
    content += tailored_resume.strip()
    content += "\n"

    path.write_text(content, encoding="utf-8")

    return {
        "ok": True,
        "path": str(path),
        "company": company,
        "title": title,
        "error": "",
    }


def list_resume_versions() -> Dict[str, Any]:
    files = []
    for company_dir in BASE_DIR.iterdir():
        if company_dir.is_dir():
            files.extend(str(p) for p in company_dir.glob("resume-*.md"))
    return {
        "ok": True,
        "files": sorted(files),
        "error": "",
    }
from pathlib import Path
from typing import Any, Dict
import re

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT


_PROJECT_ROOT = Path.home() / "code" / "github" / "opencode"
BASE_DIR = _PROJECT_ROOT / "data" / "job-coach"


# ---------------------------------------------------------------------------
# XML escaping (must happen *inside* the rich-text converter, not before)
# ---------------------------------------------------------------------------

def _esc(text: str) -> str:
    """Escape text for ReportLab's XML-based Paragraph markup."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


# ---------------------------------------------------------------------------
# Inline markdown → ReportLab XML tags
# ---------------------------------------------------------------------------

# Order matters: bold+italic first, then bold, then italic.
_INLINE_RE = re.compile(
    r"(\*\*\*(.+?)\*\*\*)"           # group 1,2  — bold+italic
    r"|(\*\*(.+?)\*\*)"              # group 3,4  — bold
    r"|(__(.+?)__)"                   # group 5,6  — bold (underscores)
    r"|(\*(.+?)\*)"                   # group 7,8  — italic
    r"|(_(.+?)_)"                     # group 9,10 — italic (underscores)
    r"|(`(.+?)`)"                     # group 11,12 — inline code
    r"|(\[([^\]]+)\]\(([^)]+)\))"     # group 13,14,15 — link [text](url)
)


def _md_to_xml(text: str) -> str:
    """Convert inline markdown to ReportLab XML, escaping plain text segments."""
    parts: list[str] = []
    last = 0

    for m in _INLINE_RE.finditer(text):
        # Plain text before this match — escape it
        if m.start() > last:
            parts.append(_esc(text[last : m.start()]))

        if m.group(2):       # ***bold italic***
            parts.append(f"<b><i>{_esc(m.group(2))}</i></b>")
        elif m.group(4):     # **bold**
            parts.append(f"<b>{_esc(m.group(4))}</b>")
        elif m.group(6):     # __bold__
            parts.append(f"<b>{_esc(m.group(6))}</b>")
        elif m.group(8):     # *italic*
            parts.append(f"<i>{_esc(m.group(8))}</i>")
        elif m.group(10):    # _italic_
            parts.append(f"<i>{_esc(m.group(10))}</i>")
        elif m.group(12):    # `code`
            parts.append(
                f'<font face="Courier" size="9">{_esc(m.group(12))}</font>'
            )
        elif m.group(14):    # [text](url) — render as underlined link text
            parts.append(
                f'<a href="{_esc(m.group(15))}">{_esc(m.group(14))}</a>'
            )

        last = m.end()

    # Remaining plain text
    if last < len(text):
        parts.append(_esc(text[last:]))

    return "".join(parts)


# ---------------------------------------------------------------------------
# Line-type classification helpers
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)")
_BULLET_RE = re.compile(r"^(\s*)([-*])\s+(.*)")
_NUMBERED_RE = re.compile(r"^(\s*)(\d+)\.\s+(.*)")
_HR_RE = re.compile(r"^[\s]*([-*_])\s*\1\s*\1[\s\-*_]*$")


def _is_metadata_line(line: str) -> bool:
    stripped = line.strip()
    if _HR_RE.match(stripped):
        return True
    return stripped.lower().startswith("resume tailored for")


# ---------------------------------------------------------------------------
# Public export function
# ---------------------------------------------------------------------------

def export_resume_version_pdf(filename: str, company: str = None) -> Dict[str, Any]:
    if not filename:
        return {
            "ok": False,
            "input_path": "",
            "output_path": "",
            "error": "No filename provided",
        }

    # Determine input and output paths
    if company:
        company_slug = company.lower().strip()
        company_slug = re.sub(r"[^a-z0-9]+", "-", company_slug).strip("-")
        input_path = BASE_DIR / company_slug / filename
        output_dir = BASE_DIR / company_slug
    else:
        # Try to find in any company directory
        input_path = None
        output_dir = None
        for company_dir in BASE_DIR.iterdir():
            if company_dir.is_dir():
                candidate = company_dir / filename
                if candidate.is_file():
                    input_path = candidate
                    output_dir = company_dir
                    break
        if input_path is None:
            return {
                "ok": False,
                "input_path": "",
                "output_path": "",
                "error": f"File not found: {filename}",
            }

    if not input_path.is_file():
        return {
            "ok": False,
            "input_path": str(input_path),
            "output_path": "",
            "error": f"File not found: {input_path}",
        }

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{input_path.stem}.pdf"

    try:
        text = input_path.read_text(encoding="utf-8")
        lines = text.splitlines()

        styles = getSampleStyleSheet()

        body = ParagraphStyle(
            "ResumeBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=13,
            alignment=TA_LEFT,
            spaceAfter=4,
        )

        h1 = ParagraphStyle(
            "ResumeH1",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            spaceAfter=10,
        )

        h2 = ParagraphStyle(
            "ResumeH2",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11.5,
            leading=14,
            spaceBefore=8,
            spaceAfter=6,
        )

        h3 = ParagraphStyle(
            "ResumeH3",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=13,
            spaceBefore=6,
            spaceAfter=4,
        )

        bullet = ParagraphStyle(
            "ResumeBullet",
            parent=body,
            leftIndent=12,
            firstLineIndent=-8,
            spaceAfter=3,
        )

        bullet_nested = ParagraphStyle(
            "ResumeBulletNested",
            parent=bullet,
            leftIndent=24,
        )

        numbered = ParagraphStyle(
            "ResumeNumbered",
            parent=body,
            leftIndent=12,
            firstLineIndent=-8,
            spaceAfter=3,
        )

        # Map heading levels to styles
        heading_styles = {1: h1, 2: h2, 3: h3, 4: h3}

        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=LETTER,
            leftMargin=0.65 * inch,
            rightMargin=0.65 * inch,
            topMargin=0.6 * inch,
            bottomMargin=0.6 * inch,
        )

        story: list = []

        for raw_line in lines:
            line = raw_line.rstrip()
            stripped = line.strip()

            # Skip metadata / horizontal rules
            if _is_metadata_line(stripped):
                continue

            # Blank lines → small spacer
            if not stripped:
                story.append(Spacer(1, 6))
                continue

            # --- Headings (#{1,6}) ---
            hm = _HEADING_RE.match(stripped)
            if hm:
                level = min(len(hm.group(1)), 4)
                style = heading_styles.get(level, h3)
                story.append(Paragraph(_md_to_xml(hm.group(2).strip()), style))
                continue

            # --- Bullet lists (- or *) with indentation ---
            bm = _BULLET_RE.match(line)
            if bm:
                indent_depth = len(bm.group(1))
                style = bullet_nested if indent_depth >= 2 else bullet
                story.append(
                    Paragraph(f"• {_md_to_xml(bm.group(3).strip())}", style)
                )
                continue

            # --- Numbered lists (1. text) ---
            nm = _NUMBERED_RE.match(line)
            if nm:
                num = nm.group(2)
                story.append(
                    Paragraph(
                        f"{_esc(num)}. {_md_to_xml(nm.group(3).strip())}",
                        numbered,
                    )
                )
                continue

            # --- Normal paragraph with rich-text ---
            story.append(Paragraph(_md_to_xml(stripped), body))

        doc.build(story)
        return {
            "ok": True,
            "input_path": str(input_path),
            "output_path": str(output_path),
            "error": "",
        }
    except Exception as e:
        return {
            "ok": False,
            "input_path": str(input_path),
            "output_path": str(output_path) if output_path else "",
            "error": str(e),
        }

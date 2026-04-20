---
name: job-coach-prepare-from-link
description: Prepare a job from a link by extracting it, evaluating fit, generating materials, exporting them to DOCX by default, finding the apply link, and updating the tracker
---

You are a deterministic job preparation orchestration system.

## When to use me

Use this skill as the main entry point for job preparation. Pass a job URL, get back: extracted job data, fit evaluation, tailored resume (DOCX), cover letter (optional DOCX), apply link, and tracker update—all in one orchestrated workflow.

**This is the comprehensive skill** – combines multiple sub-skills.

## Input

```json
{
  "url": "Job posting URL (required)",
  "notes": "Optional user notes about the job",
  "export_format": "Optional export format override (defaults to docx)"
}
```

## Output

```json
{
  "company": "string",
  "title": "string",
  "summary": "string (why it may/may not fit)",
  "fit_recommendation": "apply|maybe|skip",
  "fit_score": 0-100,
  "key_strengths": ["string"],
  "key_gaps": ["string"],
  "tailored_resume_created": "boolean",
  "tailored_resume_path": "string",
  "tailored_resume_export_path": "string",
  "cover_letter_created": "boolean",
  "cover_letter_path": "string",
  "cover_letter_export_path": "string",
  "apply_url": "string",
  "tracker_status": "string (usually 'saved')",
  "next_step": "string (one actionable sentence)",
  "warnings": ["string"]
}
```

## Workflow

1. Fetch job page (prefer browser fetcher for LinkedIn)
2. Extract structured job data
3. Load base resume from `data/job-coach/resume.json`
4. Evaluate job fit against resume skills and experience
5. Create company subdirectory: `data/job-coach/{company}/`
6. Generate tailored resume (markdown) highlighting relevant experience
7. Generate cover letter (markdown) if fit is "apply" or "maybe"
8. **Convert markdown to DOCX formatting** (headings, bold, italic, lists, etc.) with no markdown characters visible
9. Export both to DOCX using baseline template styling with proper formatting applied
10. Save job posting details to `data/job-coach/{company}/job-posting.md`
11. Update job tracker in `data/job-coach/jobs.json`
12. Find apply URL
13. Return result with file paths and recommendation

## Resume Configuration

**Primary Resume Source**: `data/job-coach/resume.json`

This is a structured JSON file containing:
- Personal info (name, email, phone, location)
- Professional summary
- Skills (array of competencies)
- Work experience (company, title, dates, bullets)
- Education
- Certifications

**Baseline Reference Files**:
- `data/job-coach/baseline-resume.docx` - DOCX template for export formatting
- `data/job-coach/baseline-resume.pdf` - PDF reference

## File Structure

All files are stored locally in the `data/job-coach/` directory:

```
data/job-coach/
├── resume.json                          # Primary resume (structured data)
├── baseline-resume.docx                 # DOCX template for exports
├── baseline-resume.pdf                  # PDF reference
├── {company}/                           # Company-specific subdirectory
│   ├── {company}_{title}.md             # Tailored resume (markdown)
│   ├── {company}_resume_{title}.docx    # Tailored resume (DOCX export)
│   ├── {company}_{title}.md             # Cover letter (markdown)
│   ├── {company}_cover-letter_{title}.docx  # Cover letter (DOCX export)
│   ├── job-posting.md                   # Saved job posting details
└── └── jobs.json                        # Tracked jobs metadata
```

**Example**: For Bestow Staff Backend Engineer position:
```
data/job-coach/bestow/
├── bestow_staff-backend-engineer.md
├── bestow_resume_staff-backend-engineer.docx
├── bestow_staff-backend-engineer.md
├── bestow_cover-letter_staff-backend-engineer.docx
└── job-posting.md
```

## Rules

- Return valid JSON only
- Do not include explanation outside JSON
- Do not invent qualifications, job details, or links
- If a step fails, record in warnings and continue
- fit_recommendation must be: apply, maybe, skip
- fit_score must be 0-100
- Export defaults to DOCX unless explicitly overridden
- All file paths should be relative to project root (`~/code/github/opencode/`)
- Create directories as needed if they don't exist
- Use consistent naming for exported files: `{company}_{type}.{ext}` where:
  - `{company}` = lowercase company name (e.g., `bestow`, `cribl`)
  - `{type}` = `resume` or `cover-letter`
  - Example: `bestow_resume.docx`, `cribl_cover-letter.docx`
- **CRITICAL:** Convert markdown to DOCX formatting (not plain text):
  - Heading markers (`#`, `##`, `###`) → Apply H1, H2, H3 styles
  - Bold markers (`**text**`) → Apply bold formatting to text
  - Italic markers (`*text*`, `_text_`) → Apply italic formatting to text
  - Strikethrough (`~~text~~`) → Apply strikethrough formatting
  - Inline code (`` `code` ``) → Apply monospace/code formatting
  - Bullet/numbered lists → Apply list formatting
  - Preserve line breaks and paragraph structure
  - Result should be professionally formatted with NO markdown syntax characters visible
---
name: job-list
description: Format and filter job records for display
input_schema:
  type: object
  properties:
    jobs:
      type: array
      items:
        type: object
    status:
      type: string
    company:
      type: string
    sort_by:
      type: string
    sort_order:
      type: string
  required: [jobs]
output_schema:
  type: object
  properties:
    total: { type: integer }
    filtered_total: { type: integer }
    jobs:
      type: array
      items:
        type: object
    summary: { type: string }
  required:
    - total
    - filtered_total
    - jobs
    - summary
---

You are a precise job listing system.

Rules:
- Return valid JSON only
- Do not include explanation outside JSON
- Filter by exact match when status or company is provided
- sort_by may be: company, title, status, created_at, updated_at, last_contact_at
- sort_order may be: asc, desc
- If sort options are missing or invalid, preserve original order
- Be conservative and do not invent fields
- Keep summary under 80 words

Task:
Filter, sort, and format the provided job records for display.
---
name: export-docx
description: Export a saved resume version to DOCX
input_schema:
  type: object
  properties:
    filename:
      type: string
      description: Name of the resume version file (e.g. company-role.md)
  required: [filename]
output_schema:
  type: object
  properties:
    output_path: { type: string }
    ok: { type: boolean }
    error: { type: string }
  required:
    - output_path
    - ok
    - error
---

You are a resume DOCX export system.

Rules:
- Return valid JSON only
- Do not include explanation outside JSON

Workflow:
1. Use the export-docx tool with the provided filename
2. Return the output_path and status

Task:
Export the requested resume version to DOCX.

If no filename is provided:
1. Use resume-version-store to list files
2. Select the most recent one
3. Export that file
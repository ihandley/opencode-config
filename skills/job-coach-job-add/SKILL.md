---
name: job-coach-job-add
description: Create a structured job record from extracted job data
---

You are a precise job record creation system.

## When to use me

Use this skill to convert extracted job data into a storable job record with metadata (ID, status, timestamps). Works with data from `job-coach-description-extract` or `job-coach-save-from-description`.

## Input

```json
{
  "company": "string (required)",
  "title": "string (required)",
  "location": "string",
  "salary": "string",
  "benefits": "string",
  "tech_stack": ["string"],
  "seniority": "string",
  "keywords": ["string"],
  "summary": "string",
  "source": "string",
  "url": "string",
  "notes": "string"
}
```

## Output

```json
{
  "id": "string (unique identifier)",
  "company": "string",
  "title": "string",
  "location": "string",
  "salary": "string",
  "benefits": "string",
  "tech_stack": ["string"],
  "seniority": "string",
  "keywords": ["string"],
  "summary": "string",
  "source": "string",
  "url": "string",
  "status": "saved",
  "notes": "string",
  "created_at": "ISO-8601 timestamp",
  "updated_at": "ISO-8601 timestamp"
}
```

## Rules

- Return valid JSON only
- Do not include explanation outside JSON
- If optional fields are missing, use empty strings or empty arrays
- status must default to "saved"
- created_at and updated_at must be ISO-8601 timestamps if provided by the caller; otherwise return empty strings
- Generate a short unique id using lowercase letters, numbers, and hyphens (e.g., "acme-senior-devops-abc123")
- Include a short random suffix to ensure uniqueness
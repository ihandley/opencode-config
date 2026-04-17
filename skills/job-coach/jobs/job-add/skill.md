---
name: job-add
description: Create a structured job record from extracted job data
input_schema:
  type: object
  properties:
    company: { type: string }
    title: { type: string }
    location: { type: string }
    salary: { type: string }
    benefits: { type: string }
    tech_stack:
      type: array
      items: { type: string }
    seniority: { type: string }
    keywords:
      type: array
      items: { type: string }
    summary: { type: string }
    source: { type: string }
    url: { type: string }
    notes: { type: string }
  required: [company, title]
output_schema:
  type: object
  properties:
    id: { type: string }
    company: { type: string }
    title: { type: string }
    location: { type: string }
    salary: { type: string }
    benefits: { type: string }
    tech_stack:
      type: array
      items: { type: string }
    seniority: { type: string }
    keywords:
      type: array
      items: { type: string }
    summary: { type: string }
    source: { type: string }
    url: { type: string }
    status: { type: string }
    notes: { type: string }
    created_at: { type: string }
    updated_at: { type: string }
  required:
    - id
    - company
    - title
    - location
    - salary
    - benefits
    - tech_stack
    - seniority
    - keywords
    - summary
    - source
    - url
    - status
    - notes
    - created_at
    - updated_at
---

You are a precise job record creation system.

Rules:
- Return valid JSON only
- Do not include explanation outside JSON
- If optional fields are missing, use empty strings or empty arrays
- status must default to "saved"
- created_at and updated_at must be ISO-8601 timestamps if provided by the caller; otherwise return empty strings
- Generate a short unique id using lowercase letters, numbers, and hyphens
- id must be lowercase, hyphenated
- include a short random suffix to ensure uniqueness

Task:
Create a normalized job record from the provided job data.
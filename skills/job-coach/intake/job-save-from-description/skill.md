---
name: job-save-from-description
description: Extract job data from a raw description and prepare a normalized job record for storage
input_schema:
  type: object
  properties:
    text:
      type: string
    source:
      type: string
    url:
      type: string
    notes:
      type: string
  required: [text]
output_schema:
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
    status: { type: string }
    notes: { type: string }
  required:
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
  tools:
    - job-store
    - job-page-fetcher
    - job-page-browser-fetcher
---

You are a precise job intake system.

Rules:
- Return valid JSON only
- Do not include explanation outside JSON
- Extract only what is supported by the job description
- If optional fields are missing, use empty strings or empty arrays
- status must be "saved"
- Be conservative and do not guess

Task:
Read the raw job description and prepare a normalized job record ready to be saved.
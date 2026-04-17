---
name: job-search-dashboard
description: Summarize the current state of the job search tracker and highlight next actions
input_schema:
  type: object
  properties:
    jobs:
      type: array
      items:
        type: object
  required: [jobs]
output_schema:
  type: object
  properties:
    total_jobs: { type: integer }
    by_status:
      type: object
    active_jobs:
      type: array
      items: { type: string }
    follow_up_needed:
      type: array
      items: { type: string }
    recent_activity:
      type: array
      items: { type: string }
    next_actions:
      type: array
      items: { type: string }
    summary: { type: string }
  required:
    - total_jobs
    - by_status
    - active_jobs
    - follow_up_needed
    - recent_activity
    - next_actions
    - summary
---

You are a precise job search dashboard system.

Rules:
- Return valid JSON only
- Do not include explanation outside JSON
- Be conservative and use only the provided jobs data
- active_jobs should include jobs in statuses such as applied, recruiter-contacted, interview-scheduled, interviewing, take-home, offer
- follow_up_needed should include jobs that appear active but have no recent contact or next step noted
- Keep summary under 100 words

Task:
Summarize the current state of the user's job search and identify the most important next actions.
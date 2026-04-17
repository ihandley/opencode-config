## Dashboard Workflow

If the user asks for a dashboard, pipeline summary, or what to do next:

1. Load jobs from job-store
2. Use job-search-dashboard
3. Present the result in a human-friendly format
4. Include:
   - total jobs
   - jobs by status
   - active jobs
   - follow-up needed
   - next actions
5. Only return raw JSON if explicitly requested

## Batch Filtering Workflow

If the user asks which jobs are worth applying to:

1. Load the saved resume if available
2. Use the provided jobs or load tracked jobs
3. Apply user preferences if provided
4. Use job-batch-filter
5. Return ranked jobs with apply, maybe, or skip recommendations

When job-search-dashboard returns structured JSON, never return it directly unless the user explicitly asks for raw JSON.
Always transform it into a human-readable dashboard format.
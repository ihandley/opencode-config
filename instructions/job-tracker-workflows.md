# Job Tracker Workflows

Job Tracker is responsible for extracting, storing, searching, filtering, and reporting on jobs.

## Dashboard Workflow

If the user asks for a dashboard, pipeline summary, or what to do next:

1. Load jobs from job-store
2. Use job-coach-dashboard
3. Present the result in a human-friendly format
4. Include:
   - total jobs
   - jobs by status
   - active jobs
   - follow-up needed
   - next actions
5. Only return raw JSON if explicitly requested

When job-coach-dashboard returns structured JSON, never return it directly unless the user explicitly asks for raw JSON.
Always transform it into a human-readable dashboard format.

## Batch Filtering Workflow

If the user asks which jobs are worth applying to:

1. Load the saved resume if available
2. Use the provided jobs or load tracked jobs
3. Apply user preferences if provided
4. Use job-coach-batch-filter
5. Return ranked jobs with apply, maybe, or skip recommendations

## Job Extraction and Tracking

If the user provides a job description or wants to save a job:

1. Parse the job with job-coach-description-extract
2. Create a job record with job-coach-job-add
3. Save to job-store
4. Return confirmation with ID and key details

## Job Matching

If the user has an email mentioning a job or asks about a specific company:

1. Use job-coach-find-match to identify the tracked job
2. If exact match: return job details
3. If multiple matches: ask user to clarify
4. If no match: offer to create a new tracked job

## Job Status Updates

Track job application progress:

1. Use job-coach-job-update-status
2. Record status change and any notes
3. Update last_contact_at if needed

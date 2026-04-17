## Email Processing Workflow

If the user asks to check email for job-related responses:

1. Use the Google Workspace MCP Gmail tools to search recent job-related emails
2. Read the relevant emails
3. Use email-job-response-extract on each email
4. Load tracked jobs from job-store
5. Use job-find-match to find the best matching tracked job
6. If one clear match exists, update the job record
7. If the match is ambiguous, summarize the email and ask the user to confirm
8. Return a short summary of updates, unmatched emails, and actions needed

## Email Rules

- Prefer exact company match
- If multiple jobs share the same company, prefer the most recently updated one only if clearly appropriate
- Do not update automatically if the match is ambiguous
- Do not invent interview times, names, or deadlines
- Only mark a job as rejected if the email clearly says so
- If the email is job-related but status is unclear, leave status unchanged and return action items only
# Outreach Manager Workflows

Outreach Manager is responsible for email processing, follow-up coordination, and candidate communication.

## Email Processing Workflow

If the user asks to check email for job-related responses:

1. Use the Google Workspace MCP Gmail tools to search recent job-related emails
2. Read the relevant emails
3. Use job-coach-email-job-response-extract on each email
4. Load tracked jobs from job-store
5. Use job-coach-find-match to find the best matching tracked job
6. If one clear match exists, update the job record
7. If the match is ambiguous, summarize the email and ask the user to confirm
8. Return a short summary of updates, unmatched emails, and actions needed

### Email Rules

- Prefer exact company match
- If multiple jobs share the same company, prefer the most recently updated one only if clearly appropriate
- Do not update automatically if the match is ambiguous
- Do not invent interview times, names, or deadlines
- Only mark a job as rejected if the email clearly says so
- If the email is job-related but status is unclear, leave status unchanged and return action items only

## Follow-up Recommendation Workflow

If the user asks what to follow up on or what to do next:

1. Load jobs from job-store
2. Use job-coach-follow-up-recommendation
3. Return concise suggestions
4. Prioritize by: time since last contact, interview stage, application status

## Follow-up Message Workflow

If the user wants to send or draft a follow-up:

1. Identify the relevant job
2. Use job-coach-follow-up-message-draft
3. Return subject and body
4. Offer to send via Gmail if the user approves

## Follow-up Automation Notes

- Suggest follow-up to users proactively when:
  - 2+ weeks since application with no response
  - Interview scheduled but no recent updates
  - Recruiter contact made but no next step defined
  - Job in "offer" stage waiting for response

# Improved Email Search Workflow for Job Coach

## Problem Solved
Previously, email searches for job status updates used generic keywords and company domains, which missed emails with generic subject lines (like Deloitte's "Deloitte Follow Up").

## Solution
Use the job tracker as the single source of truth for which companies to search.

## Implementation

### When User Asks: "Check my email for job updates"

**Step 1: Load Job Tracker**
```
Read: ~/code/github/opencode/data/job-coach/jobs.json
Extract: All companies with status "applied" or "saved"
```

**Step 2: Build Dynamic Search Query**
```
Run: python3 ~/code/github/opencode/data/job-coach/search_job_emails.py
Output: from:(Company1 OR Company2 OR Company3 OR ...)
```

**Step 3: Search Gmail**
```
Use: google_workspace_search_gmail_messages
Query: from:(Hightouch OR Paxos OR Teleport OR ...)
Page size: 50 (to catch all recent emails)
```

**Step 4: Parse Results**
For each email:
- Extract company name
- Determine status:
  - "rejection" if contains: "unfortunately", "not a fit", "other candidates", "not ideally suited"
  - "interview" if contains: "interview", "next steps", "schedule", "call"
  - "offer" if contains: "offer", "congratulations", "excited to"
  - "under_review" if contains: "thank you", "received", "reviewing"
- Extract dates, contact info, next steps

**Step 5: Update Job Tracker**
For each status change:
- Update job record with new status
- Add email date and summary to notes
- Record any contact information

**Step 6: Report to User**
Display:
- New rejections (with reason)
- New interviews scheduled (with dates/contacts)
- New offers (with details)
- Still under review (with timeline)

## Code Template

```python
def check_job_emails(user_email):
    """Check for job status updates from all applied companies."""
    
    # Step 1: Load tracker and extract companies
    tracker = load_job_tracker("data/job-coach/jobs.json")
    companies = extract_applied_companies(tracker)
    
    if not companies:
        return {"status": "no_jobs", "message": "No applied jobs in tracker"}
    
    # Step 2: Build search query
    search_query = build_search_query(companies)
    
    # Step 3: Search Gmail
    messages = google_workspace_search_gmail_messages(
        user_email=user_email,
        query=search_query,
        page_size=50
    )
    
    # Step 4: Parse results
    updates = []
    for msg in messages:
        company = extract_company_from_email(msg)
        status = determine_email_status(msg)
        details = extract_email_details(msg)
        
        updates.append({
            "company": company,
            "status": status,
            "date": msg.date,
            "details": details
        })
    
    # Step 5: Update tracker
    for update in updates:
        update_job_tracker(tracker, update)
    
    # Step 6: Report to user
    return format_status_report(updates)
```

## Key Advantages

1. **Accuracy**: Only searches for companies you've actually applied to
2. **Completeness**: Catches emails from any domain (recruiting@, careers@, noreply@, etc.)
3. **Scalability**: Automatically includes new companies as you add them to tracker
4. **Reliability**: Not dependent on subject line keywords or generic patterns
5. **Maintainability**: Single source of truth (job tracker) drives the search
6. **Auditability**: Search query is deterministic and reproducible

## Example Comparison

### Before (Generic Search - MISSED Deloitte)
```
Query: from:(linkedin OR recruiter OR jobs OR careers OR hiring)
       subject:(interview OR offer OR rejection OR status OR application)
Result: 5 emails found
Missing: Deloitte (domain not in list, subject was "Deloitte Follow Up")
```

### After (Tracker-Based Search - FOUND Deloitte)
```
Query: from:(Hightouch OR Paxos OR Teleport OR Deloitte OR NRG OR Maven OR Scribd OR Assured)
Result: 7 emails found
Found: All companies including Deloitte
```

## Files

- `search_job_emails.py` - Helper script to generate search query
- `email-search-helper.md` - Documentation
- `IMPROVED-EMAIL-SEARCH-WORKFLOW.md` - This file

## Next Steps

1. Integrate this workflow into job-coach-follow-up-recommendation skill
2. Update job-coach-dashboard to use this search method
3. Create automated email check on schedule (daily/weekly)

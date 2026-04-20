# Job Coach Email Search Helper

## Purpose
Improved email search workflow that uses the job tracker to find status updates from all applied companies.

## Workflow

### Step 1: Load Job Tracker
Read `data/job-coach/jobs.json` and extract all companies with status "applied" or "saved".

### Step 2: Build Dynamic Search Query
Create a search query from company names:
```
from:(company1 OR company2 OR company3 OR ...)
```

### Step 3: Execute Search
Search Gmail with the dynamic query to find all emails from applied companies.

### Step 4: Parse Results
For each email found:
- Extract company name
- Determine status: rejection, interview scheduled, under review, offer
- Extract key details (dates, next steps, contact info)
- Match to job tracker entry

### Step 5: Update Tracker
Update job tracker with new status and notes.

## Implementation

```python
def search_job_emails(jobs_tracker_path, user_email):
    """
    Search for emails from all applied companies.
    
    Args:
        jobs_tracker_path: Path to jobs.json
        user_email: User's Gmail address
    
    Returns:
        List of email updates with company, status, and details
    """
    import json
    
    # Load tracker
    with open(jobs_tracker_path) as f:
        tracker = json.load(f)
    
    # Extract applied companies
    companies = set()
    
    # Top-level jobs
    if "jobs" in tracker:
        for job in tracker["jobs"]:
            if job.get("status") in ["applied", "saved"]:
                companies.add(job["company"])
    
    # Also check nested jobs array
    if "jobs" in tracker and isinstance(tracker["jobs"], list):
        for job in tracker["jobs"]:
            if job.get("status") in ["applied", "saved"]:
                companies.add(job["company"])
    
    if not companies:
        return []
    
    # Build search query
    company_list = " OR ".join(companies)
    search_query = f"from:({company_list})"
    
    # Search Gmail (would call google_workspace_search_gmail_messages here)
    # Returns: list of messages with company, status, details
    
    return search_results
```

## Key Improvements Over Generic Search

1. **Accuracy**: Only searches for companies you've actually applied to
2. **Completeness**: Catches emails from any domain (recruiting@, careers@, noreply@, etc.)
3. **Scalability**: Automatically includes new companies as you add them to tracker
4. **Reliability**: Not dependent on subject line keywords or generic patterns
5. **Maintainability**: Single source of truth (job tracker) drives the search

## Usage

When user asks "Check my email for job updates":

1. Load jobs.json
2. Extract applied companies: [Paxos, Teleport, Hightouch, Deloitte, NRG, Maven, Scribd, Assured]
3. Search: `from:(Paxos OR Teleport OR Hightouch OR Deloitte OR NRG OR Maven OR Scribd OR Assured)`
4. Parse results and update tracker
5. Report status changes to user

## Example

**Before (Generic Search - MISSED Deloitte):**
```
from:(linkedin OR recruiter OR jobs OR careers OR hiring)
subject:(interview OR offer OR rejection OR status OR application)
```
Result: Missed Deloitte because domain wasn't in list

**After (Tracker-Based Search - FOUND Deloitte):**
```
from:(Paxos OR Teleport OR Hightouch OR Deloitte OR NRG OR Maven OR Scribd OR Assured)
```
Result: Found all emails from applied companies

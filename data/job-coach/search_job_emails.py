#!/usr/bin/env python3
"""
Job Coach Email Search Helper

Searches for emails from all applied companies using the job tracker as the source of truth.
"""

import json
import sys
from pathlib import Path


def load_job_tracker(tracker_path):
    """Load and parse the job tracker."""
    with open(tracker_path) as f:
        return json.load(f)


def extract_applied_companies(tracker):
    """Extract all companies with 'applied' or 'saved' status."""
    companies = set()
    
    # Check top-level job (Paxos structure)
    if tracker.get("status") in ["applied", "saved"]:
        company = tracker.get("company", "").strip()
        if company:
            companies.add(company)
    
    # Check nested jobs array
    if "jobs" in tracker and isinstance(tracker["jobs"], list):
        for job in tracker["jobs"]:
            status = job.get("status", "").lower()
            company = job.get("company", "").strip()
            if status in ["applied", "saved"] and company:
                companies.add(company)
    
    return sorted(companies)


def build_search_query(companies):
    """Build Gmail search query from company names."""
    if not companies:
        return None
    
    company_list = " OR ".join(companies)
    return f"from:({company_list})"


def print_search_query(companies, query):
    """Print the search query for use with Gmail."""
    print("=" * 70)
    print("JOB COACH EMAIL SEARCH QUERY")
    print("=" * 70)
    print(f"\nCompanies to search ({len(companies)}):")
    for company in companies:
        print(f"  - {company}")
    print(f"\nGmail search query:")
    print(f"  {query}")
    print("\n" + "=" * 70)


def main():
    tracker_path = Path.home() / "code/github/opencode/data/job-coach/jobs.json"
    
    if not tracker_path.exists():
        print(f"Error: Job tracker not found at {tracker_path}")
        sys.exit(1)
    
    # Load tracker and extract companies
    tracker = load_job_tracker(tracker_path)
    companies = extract_applied_companies(tracker)
    
    if not companies:
        print("No applied or saved jobs found in tracker.")
        sys.exit(0)
    
    # Build and display search query
    query = build_search_query(companies)
    print_search_query(companies, query)
    
    # Output for use in other scripts
    print(f"\nJSON output:")
    print(json.dumps({
        "companies": companies,
        "count": len(companies),
        "search_query": query
    }, indent=2))


if __name__ == "__main__":
    main()

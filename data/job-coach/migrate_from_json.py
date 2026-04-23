#!/usr/bin/env python3
"""
Migration script to migrate data from JSON files to SQLite database.
Migrates jobs.json and resume.json to the job_coach.db database.
"""

import json
import os
import sys
from pathlib import Path
from db_helper import JobCoachDB

def load_json_file(file_path: str) -> dict:
    """Load JSON file and return data."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return {}

def migrate_jobs(db: JobCoachDB, jobs_data: dict):
    """Migrate jobs data to database."""
    jobs = jobs_data.get('jobs', [])
    print(f"Migrating {len(jobs)} jobs...")

    migrated = 0
    for job in jobs:
        if db.save_job(job):
            migrated += 1
        else:
            print(f"Failed to migrate job: {job.get('id', 'unknown')}")

    print(f"Successfully migrated {migrated} jobs")

def migrate_resume(db: JobCoachDB, resume_data: dict):
    """Migrate resume data to database."""
    print("Migrating resume data...")
    if db.save_resume(resume_data):
        print("Successfully migrated resume")
    else:
        print("Failed to migrate resume")

def main():
    """Main migration function."""
    # Get paths
    data_dir = Path(__file__).parent
    jobs_json = data_dir / "jobs.json"
    resume_json = data_dir / "resume.json"

    # Check if JSON files exist
    if not jobs_json.exists():
        print(f"Jobs JSON file not found: {jobs_json}")
        return

    if not resume_json.exists():
        print(f"Resume JSON file not found: {resume_json}")
        return

    # Initialize database
    db = JobCoachDB()

    # Load JSON data
    print("Loading JSON data...")
    jobs_data = load_json_file(str(jobs_json))
    resume_data = load_json_file(str(resume_json))

    if not jobs_data:
        print("No jobs data to migrate")
        return

    if not resume_data:
        print("No resume data to migrate")
        return

    # Migrate data
    migrate_jobs(db, jobs_data)
    migrate_resume(db, resume_data)

    print("Migration completed!")

    # Optional: Backup original files
    backup_dir = data_dir / "backup"
    backup_dir.mkdir(exist_ok=True)

    import shutil
    shutil.copy2(jobs_json, backup_dir / "jobs.json.backup")
    shutil.copy2(resume_json, backup_dir / "resume.json.backup")

    print(f"Original files backed up to: {backup_dir}")

if __name__ == "__main__":
    main()
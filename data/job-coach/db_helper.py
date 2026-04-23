#!/usr/bin/env python3
"""
Database helper module for Job Coach SQLite operations.
Provides functions to interact with jobs and resume data.
"""

import sqlite3
import json
import os
from typing import List, Dict, Optional, Any
from pathlib import Path

class JobCoachDB:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = os.getenv('JOB_COACH_DB', '/Users/ianhandley/code/github/opencode/data/job-coach/job_coach.db')
        self.db_path = db_path
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Ensure database exists, create if it doesn't."""
        if not Path(self.db_path).exists():
            # Run init script
            init_script = Path(__file__).parent / "init_db.py"
            if init_script.exists():
                os.system(f"python3 {init_script}")
            else:
                raise FileNotFoundError(f"Database not found and init script missing: {init_script}")

    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        return sqlite3.connect(self.db_path)

    def _json_dumps(self, data: Any) -> str:
        """Convert data to JSON string."""
        return json.dumps(data) if data else '[]'

    def _json_loads(self, data: str) -> Any:
        """Convert JSON string to data."""
        return json.loads(data) if data else []

    # Job operations
    def save_job(self, job_data: Dict[str, Any]) -> bool:
        """Save or update a job."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()

                # Convert arrays to JSON
                requirements = self._json_dumps(job_data.get('requirements', []))
                nice_to_have = self._json_dumps(job_data.get('nice_to_have', []))
                benefits = self._json_dumps(job_data.get('benefits', []))
                contacts = self._json_dumps(job_data.get('contacts', []))
                tech_stack = self._json_dumps(job_data.get('tech_stack', []))

                cursor.execute('''
                    INSERT OR REPLACE INTO jobs
                    (id, company, title, status, applied_date, location, salary,
                     description, requirements, nice_to_have, benefits, recruiter,
                     contacts, notes, saved_date, url, tech_stack)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    job_data['id'],
                    job_data['company'],
                    job_data['title'],
                    job_data.get('status', 'saved'),
                    job_data.get('applied_date'),
                    job_data.get('location'),
                    job_data.get('salary'),
                    job_data.get('description'),
                    requirements,
                    nice_to_have,
                    benefits,
                    job_data.get('recruiter', ''),
                    contacts,
                    job_data.get('notes', ''),
                    job_data['saved_date'],
                    job_data.get('url'),
                    tech_stack
                ))

                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving job: {e}")
            return False

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get a job by ID."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM jobs WHERE id = ?', (job_id,))
                row = cursor.fetchone()

                if row:
                    columns = [desc[0] for desc in cursor.description]
                    job_dict = dict(zip(columns, row))

                    # Convert JSON strings back to arrays
                    job_dict['requirements'] = self._json_loads(job_dict['requirements'])
                    job_dict['nice_to_have'] = self._json_loads(job_dict['nice_to_have'])
                    job_dict['benefits'] = self._json_loads(job_dict['benefits'])
                    job_dict['contacts'] = self._json_loads(job_dict['contacts'])
                    job_dict['tech_stack'] = self._json_loads(job_dict['tech_stack'])

                    return job_dict
        except Exception as e:
            print(f"Error getting job: {e}")
        return None

    def get_all_jobs(self) -> List[Dict[str, Any]]:
        """Get all jobs."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM jobs ORDER BY saved_date DESC')
                rows = cursor.fetchall()

                columns = [desc[0] for desc in cursor.description]
                jobs = []

                for row in rows:
                    job_dict = dict(zip(columns, row))
                    # Convert JSON strings back to arrays
                    job_dict['requirements'] = self._json_loads(job_dict['requirements'])
                    job_dict['nice_to_have'] = self._json_loads(job_dict['nice_to_have'])
                    job_dict['benefits'] = self._json_loads(job_dict['benefits'])
                    job_dict['contacts'] = self._json_loads(job_dict['contacts'])
                    job_dict['tech_stack'] = self._json_loads(job_dict['tech_stack'])
                    jobs.append(job_dict)

                return jobs
        except Exception as e:
            print(f"Error getting all jobs: {e}")
            return []

    def update_job_status(self, job_id: str, status: str) -> bool:
        """Update job status."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE jobs SET status = ? WHERE id = ?', (status, job_id))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating job status: {e}")
            return False

    # Resume operations
    def save_resume(self, resume_data: Dict[str, Any]) -> bool:
        """Save resume data."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()

                # Convert arrays to JSON
                skills = self._json_dumps(resume_data.get('skills', []))
                work_experience = self._json_dumps(resume_data.get('work_experience', []))

                cursor.execute('''
                    INSERT OR REPLACE INTO resume
                    (id, name, email, phone, location, linkedin, github, website,
                     summary, skills, work_experience)
                    VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    resume_data['name'],
                    resume_data['email'],
                    resume_data.get('phone'),
                    resume_data.get('location'),
                    resume_data.get('linkedin'),
                    resume_data.get('github'),
                    resume_data.get('website'),
                    resume_data.get('summary'),
                    skills,
                    work_experience
                ))

                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving resume: {e}")
            return False

    def get_resume(self) -> Optional[Dict[str, Any]]:
        """Get resume data."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM resume WHERE id = 1')
                row = cursor.fetchone()

                if row:
                    columns = [desc[0] for desc in cursor.description]
                    resume_dict = dict(zip(columns, row))

                    # Convert JSON strings back to arrays
                    resume_dict['skills'] = self._json_loads(resume_dict['skills'])
                    resume_dict['work_experience'] = self._json_loads(resume_dict['work_experience'])

                    return resume_dict
        except Exception as e:
            print(f"Error getting resume: {e}")
        return None
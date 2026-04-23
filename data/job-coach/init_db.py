#!/usr/bin/env python3
"""
Database initialization script for Job Coach SQLite database.
Creates the database and runs the schema if it doesn't exist.
"""

import sqlite3
import os
import sys
from pathlib import Path

def init_database(db_path: str):
    """Initialize the SQLite database with schema."""
    print(f"Initializing database at: {db_path}")

    # Create directory if it doesn't exist
    db_dir = Path(db_path).parent
    db_dir.mkdir(parents=True, exist_ok=True)

    # Connect to database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Read and execute schema
    schema_path = Path(__file__).parent / "schema.sql"
    if not schema_path.exists():
        print(f"Error: schema.sql not found at {schema_path}")
        sys.exit(1)

    with open(schema_path, 'r') as f:
        schema_sql = f.read()

    # Execute schema
    cursor.executescript(schema_sql)
    conn.commit()

    print("Database initialized successfully!")

    # Verify tables were created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Created tables: {[table[0] for table in tables]}")

    conn.close()

if __name__ == "__main__":
    # Get database path from environment variable or default
    db_path = os.getenv('JOB_COACH_DB', '/Users/ianhandley/code/github/opencode/data/job-coach/job_coach.db')

    try:
        init_database(db_path)
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)
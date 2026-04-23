-- Job Coach Database Schema
-- SQLite database for tracking job applications and resume data

-- Jobs table
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    company TEXT NOT NULL,
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'saved',
    applied_date TEXT,
    location TEXT,
    salary TEXT,
    description TEXT,
    requirements TEXT, -- JSON array
    nice_to_have TEXT, -- JSON array
    benefits TEXT, -- JSON array
    recruiter TEXT,
    contacts TEXT, -- JSON array
    notes TEXT,
    saved_date TEXT NOT NULL,
    url TEXT,
    tech_stack TEXT -- JSON array
);

-- Resume table (single entry)
CREATE TABLE IF NOT EXISTS resume (
    id INTEGER PRIMARY KEY CHECK (id = 1), -- Only one resume entry
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    location TEXT,
    linkedin TEXT,
    github TEXT,
    website TEXT,
    summary TEXT,
    skills TEXT, -- JSON array
    work_experience TEXT -- JSON array
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company);
CREATE INDEX IF NOT EXISTS idx_jobs_applied_date ON jobs(applied_date);
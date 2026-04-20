## Skill Execution Rules (Non-Negotiable)

These rules enforce proper use of the skill system and prevent workarounds or alternative workflows.

### 1. Job Preparation Workflow

**For ANY single job link with "prepare" request:**

- ALWAYS use `job-coach-prepare-from-link` skill directly
- NEVER delegate to general agent
- NEVER create alternative workflows
- NEVER use bash/pandoc/manual file creation as substitutes for skill execution
- Wait for skill to complete and return results
- Do not attempt to work around skill limitations

### 2. Batch Job Filtering

**For 2 or more job links:**

- ALWAYS use `job-coach-batch-filter` skill
- Load resume from `~/code/github/opencode/data/job-coach/resume.json` automatically
- Do not ask clarifying questions
- Return ranked results with apply/maybe/skip recommendations

### 3. Skill Priority (General Rule)

**When a skill exists for a task:**

- Use the skill FIRST
- Do not create workarounds
- Do not use general agents as substitutes
- If skill fails, report the failure honestly—do not work around it
- If skill output is incomplete, ask user for clarification rather than improvising

### 4. No Workarounds

**Explicitly forbidden:**

- Do not use bash commands to create DOCX files when export skills exist
- Do not use pandoc as a substitute for `job-coach-export-docx` or `job-coach-export-pdf`
- Do not manually orchestrate multi-step workflows that have dedicated skills
- Do not assume file creation succeeded without verification
- Do not create alternative file formats or locations to bypass skill workflows

### 5. Instruction Hierarchy

**Priority order (highest to lowest):**

1. Skill-specific instructions (in skill documentation)
2. Explicit workflow rules (in this file and job-coach-rules.md)
3. General instructions (in system prompt)
4. Discretionary choices (use only when no specific rule applies)

**When in doubt:** Use the most specific skill available for the task.

### 6. Verification and Reporting

**After using a skill:**

- Verify the skill completed successfully
- Report actual file paths and results
- Do not claim success if skill failed
- If partial results, clearly indicate what succeeded and what failed
- Provide user with actionable next steps

### 7. Resume Data Handling

**Always load from canonical source:**

- Primary resume: `~/code/github/opencode/data/job-coach/resume.json`
- Do not ask user for resume location
- Do not use alternative resume formats without explicit user request
- Load automatically for all job-related tasks

### 8. Job Tracker Updates

**After job preparation:**

- Update `~/code/github/opencode/data/job-coach/jobs.json` with:
  - Job details (company, title, URL, salary, location)
  - Fit score and recommendation
  - Key strengths and gaps
  - Status (usually "saved" for new jobs)
  - Timestamp
- Do not skip tracker updates
- Verify tracker was updated before reporting completion

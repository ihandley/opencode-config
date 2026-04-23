## Skill Execution Rules (Non-Negotiable)

These rules prevent manual workarounds when a dedicated skill exists.

## 1. Required Skill Selection
- For any single job link with a preparation request, always use `job-coach-prepare-from-link`.
- For 2 or more job links, always use `job-coach-batch-filter`.
- When a dedicated skill exists for a task, use it first.

## 2. Forbidden Substitutions
- Do not use general agents as substitutes for dedicated skills.
- Do not manually orchestrate multi-step workflows that already have dedicated skills.
- Do not use bash, pandoc, or manual file creation as substitutes for export skills.
- Do not invent alternate file formats or locations to bypass skill workflows.

## 3. Failure Handling
- If a skill fails, report the failure honestly.
- Do not work around a failed skill unless the user explicitly asks for a manual fallback.
- Do not claim success without verifying the result.

## 4. Canonical Data Sources
- Resume data: SQLite database at `$JOB_COACH_DB`
- Job tracker: SQLite database at `$JOB_COACH_DB`

## 5. Required Post-Execution Checks
After using a skill:
- Verify completion
- Report actual output paths
- Confirm the tracker was updated when job preparation was performed
- Clearly distinguish success, partial success, and failure

## 6. Instruction Priority
Use this order:
1. Skill-specific documentation
2. Explicit workflow rules in this file
3. Repo-wide rules in `AGENTS.md`
4. General model discretion
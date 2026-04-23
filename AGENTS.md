# Agent Instructions

## Default Working Directory
Always default to `~/code/github/opencode` as the working directory for all opencode operations in this project.

## Global Config
Keep `~/.config/opencode` as minimal as possible. All project-specific configuration belongs in this repository.

## Terminology
When "making changes to opencode" or "updating opencode" is mentioned, it refers to the project at `~/code/github/opencode`, not the global config at `~/.config/opencode`.

## Repo Workflow Rules
- Before starting any non-trivial task, inspect available skills.
- If a matching skill exists, load and use that skill before doing any manual workflow.
- Do not manually recreate a workflow that already has a dedicated skill.
- Do not use bash, ad hoc scripts, or manual file creation as substitutes for a dedicated skill unless the user explicitly asks for a manual fallback.
- Only use sub-agents when no dedicated top-level skill exists for the task.
- If a skill fails, report the failure clearly and stop rather than improvising a workaround.
- If multiple instruction sources conflict, follow the most specific workflow rule and the most specific skill documentation.

## Job-Coach Rules
- For a single job link with a preparation request, use `job-coach-prepare-from-link`.
- For 2 or more job links, use `job-coach-batch-filter`.
- Load resume data automatically from SQLite database at `$JOB_COACH_DB`.
- Update the canonical job tracker after successful job preparation.

## Canonical Paths
- Resume data: SQLite database at `$JOB_COACH_DB`
- Job tracker: SQLite database at `$JOB_COACH_DB`
## Job Preparation From Link Workflow

If the user asks to prepare a job from a link:

1. Use job-prepare-from-link
2. Export the tailored resume to DOCX by default unless the user requests another format
3. If a cover letter is created, export it to DOCX by default unless the user requests another format
4. Present the result in a human-friendly format
5. Only return raw JSON if explicitly requested

### Response Format

#### Job
- Company: <company>
- Title: <title>

#### Summary
<summary>

#### Fit
- Recommendation: <fit_recommendation>
- Score: <fit_score>/100

#### Strengths
- <strength 1>
- <strength 2>
- <strength 3>

#### Gaps
- <gap 1>
- <gap 2>
- <gap 3>

#### Coach Perspective
- Reality check: <short paragraph>
- Leverage: <positioning>
- Risks: <concerns>
- Strategy: <what to do>

#### Materials
- Tailored resume: <created/not created> <path if available>
- Cover letter: <created/not created> <path if available>

#### Apply
- Link: <apply_url>

#### Tracker
- Status: <tracker_status>

#### Next Step
<next_step>

#### Warnings
- <warning 1>
- <warning 2>

## Application Preparation Workflow

If the user wants help applying to a job that is already known:

1. Use application-runner
2. Return a concise structured result
3. Highlight risks, materials, and next steps clearly

## Application Browser Workflow

If the user wants help filling an application:

1. Prepare application materials
2. Use application-browser to fill obvious fields
3. Upload resume if available
4. Stop before final submission unless explicitly told to continue

## Application Form Population Workflow

If the user wants help filling an application form:
1. Load the saved resume if available
2. Use application-form-populate
3. Return structured form-ready data
4. If needed, use that data to fill browser form fields
5. Warn about any fields that still need manual input
## Application Autofill Workflow

If the user is on an application page:

1. Load saved resume
2. Use application-form-populate
3. Use application-browser-fill
4. Fill obvious fields
5. Stop before submission
6. Report what was filled and what needs manual input
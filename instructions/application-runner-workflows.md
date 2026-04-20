# Application Runner Workflows

Application Runner is responsible for preparing complete job application packages and handling form autofill.

## Job Preparation From Link Workflow

If the user asks to prepare a job from a link:

1. Use job-coach-prepare-from-link
2. Export the tailored resume to DOCX by default unless the user requests another format
3. If a cover letter is created, export it to DOCX by default unless the user requests another format
4. Present the result in a human-friendly format
5. Only return raw JSON if explicitly requested

### Response Format

#### Job
- Company: {company}
- Title: {title}

#### Summary
{summary}

#### Fit
- Recommendation: {fit_recommendation}
- Score: {fit_score}/100

#### Strengths
- {strength 1}
- {strength 2}
- {strength 3}

#### Gaps
- {gap 1}
- {gap 2}
- {gap 3}

#### Coach Perspective
- Reality check: {short paragraph}
- Leverage: {positioning}
- Risks: {concerns}
- Strategy: {what to do}

#### Materials
- Tailored resume: {created/not created} {path if available}
- Cover letter: {created/not created} {path if available}

#### Apply
- Link: {apply_url}

#### Tracker
- Status: {tracker_status}

#### Next Step
{next_step}

#### Warnings
- {warning 1}
- {warning 2}

## Application Preparation Workflow

If the user wants help applying to a job that is already known:

1. Use job-coach-application-runner
2. Return a concise structured result
3. Highlight risks, materials, and next steps clearly

## Application Form Population Workflow

If the user wants help filling an application form:

1. Load the saved resume if available
2. Use job-coach-application-form-populate
3. Return structured form-ready data
4. Always use that data to fill browser form fields
5. Warn about any fields that still need manual input

## Application Form Answer Workflow

If the user needs help answering a specific application question:

1. Identify the question
2. Load saved resume and job context if available
3. Use job-coach-application-form-answer
4. Return draft answer with confidence level
5. Offer personalization suggestions if available

## Application Autofill Workflow

If the user is on an application page:

1. Load saved resume
2. Use job-coach-application-form-populate
3. Use application-browser-fill
4. Fill obvious fields
5. Stop before submission
6. Report what was filled and what needs manual input

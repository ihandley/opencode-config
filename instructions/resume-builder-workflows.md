# Resume Builder Workflows

Resume Builder is responsible for extracting, analyzing, and customizing resumes for job applications.

## Resume Intake

If the user provides a resume PDF:

1. Use resume-pdf-reader
2. Take only the text field from the result
3. Pass that text into job-coach-resume-extract
4. Save the exact JSON with resume-store
5. Do not summarize or infer before extraction
6. Return a short confirmation with name and number of roles found

## Resume Usage

When evaluating a job or tailoring a resume:
- automatically load the saved resume using resume-store
- use it as the default resume input
- only ask for a resume if none is saved

## Resume Baseline Review

If the user wants general resume advice (not job-specific):

1. Load saved resume or accept provided text
2. Use job-coach-resume-baseline-review
3. Return assessment, strengths, weaknesses, clarity issues, and formatting advice

## Resume Evaluation Against Job

If the user wants to see how well their resume fits a job:

1. Load saved resume
2. Get job description (provided or from URL)
3. Use job-coach-resume-review-against-job
4. Return overall assessment, strong points, weak points, and tailoring advice

## Resume Tailoring Suggestions

If the user wants specific edits to improve fit:

1. Load saved resume
2. Get job description
3. Use job-coach-resume-tailor-suggestions
4. Return prioritized changes: rewrite bullets, add keywords, reorganize sections, warnings

## Resume Customization Workflow

If the user wants a complete tailored resume draft:

1. Load the saved resume if available
2. Use the provided job description or job URL
3. Use job-coach-customize-for-job
4. Return the tailored resume draft, key changes, and warnings

## Resume Export to DOCX

If the user wants a resume exported to DOCX:

1. Create or locate the resume version
2. Use job-coach-export-docx
3. Return the export path

## Resume Export to PDF

If the user wants a resume exported to PDF:

1. Create or locate the resume version
2. Use job-coach-export-pdf
3. Return the export path

## Cover Letter Generation

If the user wants a cover letter for a job:

1. Load saved resume
2. Get job description
3. Use job-coach-cover-letter-draft
4. Return draft, highlights used, keywords matched
5. Offer to save and export if approved

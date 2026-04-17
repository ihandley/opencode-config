## Resume Intake

If the user provides a resume PDF:

1. Use resume-pdf-reader
2. Take only the text field from the result
3. Pass that text into resume-extract
4. Save the exact JSON with resume-store
5. Do not summarize or infer before extraction
6. Return a short confirmation with name and number of roles found

## Resume Usage

When evaluating a job or tailoring a resume:
- automatically load the saved resume using resume-store
- use it as the default resume input
- only ask for a resume if none is saved

## Resume Customization Workflow

If the user wants a tailored resume for a specific job:

1. Load the saved resume if available
2. Use the provided job description or job URL
3. Use resume-customize-for-job
4. Return the tailored resume draft, key changes, and warnings

## Resume Export Workflow

If the user wants a tailored resume exported:

1. Create or locate the tailored resume version
2. Export it to DOCX by default
3. Export to PDF only if explicitly requested
4. Return the export path

## Cover Letter Export Workflow

If the user wants a cover letter saved or exported:

1. Save the cover letter with cover-letter-store
2. Export it to DOCX by default unless another format is requested
3. Return the saved path and export path

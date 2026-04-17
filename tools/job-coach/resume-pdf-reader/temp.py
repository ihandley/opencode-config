from pathlib import Path
from pypdf import PdfReader

path = Path("/Users/ianhandley/Downloads/Ian_Handley_Resume_Final_v2.pdf")
reader = PdfReader(str(path))

for i, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ""
    print(f"\n--- PAGE {i} ---\n")
    print(text[:2000])
import pdfplumber

pdf_path = r"c:\Users\Shilpa S Nair\Desktop\Zecpath AI\data\resumes\ATS_Friendly_Resume.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        print(f"--- Page {i+1} ---")
        print(page.extract_text())
        print("\n" + "="*50 + "\n")

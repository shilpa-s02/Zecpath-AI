import sys
import os
sys.path.append(os.getcwd())

from parsers.pdf_parser import extract_text_from_pdf

pdf_path = r"c:\Users\Shilpa S Nair\Desktop\Zecpath AI\data\resumes\ATS_Friendly_Resume.pdf"
text = extract_text_from_pdf(pdf_path)

print("--- EXTRACTED TEXT ---")
print(text)
print("--- END ---")

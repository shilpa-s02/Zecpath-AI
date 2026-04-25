import sys
import os
sys.path.append(os.getcwd())

from parsers.pdf_parser import extract_text_from_pdf

pdf_path = r"c:\Users\Shilpa S Nair\Desktop\Zecpath AI\data\resumes\ASNA Resume org.pdf"
text = extract_text_from_pdf(pdf_path)

print("--- RAW TEXT START ---")
print(text)
print("--- RAW TEXT END ---")

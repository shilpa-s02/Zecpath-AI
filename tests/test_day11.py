
# import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from parsers.education_parser import EducationParser

# sample_text = """
# Bachelor of Technology in Computer Science, ABC University, 2019
# Master of Science in Data Science from XYZ University 2021

# AWS Certified Solutions Architect
# Certified Scrum Master
# Google Data Analytics Certificate
# """

# parser = EducationParser()

# education = parser.extract_education(sample_text)
# certs = parser.extract_certifications(sample_text)

# print("\n===== EDUCATION =====")
# print(education)

# print("\n===== CERTIFICATIONS =====")
# print(certs)

import sys
import os
import json

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from parsers.education_parser import EducationParser

# -----------------------------
# SAMPLE INPUT
# -----------------------------
sample_text = """
Bachelor of Technology in Computer Science, ABC University, 2019
Master of Science in Data Science from XYZ University 2021

AWS Certified Solutions Architect
Certified Scrum Master
Google Data Analytics Certificate
"""

parser = EducationParser()

education = parser.extract_education(sample_text)
certifications = parser.extract_certifications(sample_text)

# -----------------------------
# OUTPUT STRUCTURE
# -----------------------------
result = {
    "education": education,
    "certifications": certifications
}

# -----------------------------
# PRINT OUTPUT
# -----------------------------
print("\n===== DAY 11 OUTPUT =====")
print(json.dumps(result, indent=2))

# -----------------------------
# SAVE TO FILE ✅
# -----------------------------
output_dir = "output/day11_results"
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "education_results.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

print(f"\n✅ Results saved to {output_path}")
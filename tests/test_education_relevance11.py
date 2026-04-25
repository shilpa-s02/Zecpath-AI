import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from parsers.education_relevance import calculate_education_relevance

# -----------------------------
# SAMPLE EDUCATION DATA
# -----------------------------
education = [
    {
        "degree": "Bachelor's",
        "field": "Computer Science",
        "institution": "ABC University",
        "graduation_year": "2019"
    }
]

# -----------------------------
# SAMPLE JOB DESCRIPTION
# -----------------------------
job_description = """
Looking for a Computer Science graduate with strong Python and backend skills.
"""

# -----------------------------
# RUN LOGIC
# -----------------------------
score = calculate_education_relevance(education, job_description)

print("\n===== EDUCATION RELEVANCE =====")
print("Score:", score)

import json

output_dir = "output/day11_results"
os.makedirs(output_dir, exist_ok=True)

with open(os.path.join(output_dir, "education_relevance.json"), "w") as f:
    json.dump({"education_relevance": score}, f, indent=2)

print("Saved to file ✅")
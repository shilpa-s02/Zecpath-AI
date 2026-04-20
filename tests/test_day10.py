import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json

from parsers.experience_parser import enrich_experience
from scoring.relevance_engine import compute_relevance

# Load your resume JSON
with open("output/resume_data/sample_resume.json") as f:
    resume = json.load(f)

# Dummy job description
job_text = "Looking for Python backend engineer with API experience"

# Get experience
experiences = resume.get("experience", [])

# Process
experiences, total_exp = enrich_experience(experiences)
experiences, score = compute_relevance(experiences, job_text)

print("\n===== DAY 10 OUTPUT =====")
print("Total Experience:", total_exp)
print("Relevance Score:", score)

for exp in experiences:
    print(exp)

output_data = {
    "total_experience": total_exp,
    "overall_relevance": score,
    "roles": experiences
}

# Create folder if not exists
os.makedirs("output/day10_results", exist_ok=True)

# Save file
with open("output/day10_results/result.json", "w") as f:
    json.dump(output_data, f, indent=2)

print("\n✅ Results saved to output/day10_results/result.json")
from parsers.resume_parser import ResumeParser, save_resume_json

# Initialize parser
parser = ResumeParser()

# Input PDF (change name if needed)
input_file = "data/resumes/ATS_Friendly_Resume.pdf"

# Output JSON
output_file = "output/resume_data/ATS_resume.json"

# Run parser
data = parser.parse_file(input_file)

# Save JSON
save_resume_json(data, output_file)

print("✅ Resume converted to JSON successfully!")
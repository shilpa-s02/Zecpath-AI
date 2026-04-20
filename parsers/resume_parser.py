# import os
# import json
# import re
# from typing import Dict, Any
# from parsers.pdf_parser import extract_text_from_pdf
# from parsers.docx_parser import extract_text_from_docx
# from parsers.section_classifier import SectionClassifier
# from parsers.skill_extractor import SkillExtractor
# from utils.text_cleaner import clean_text
# from utils.logger import log

# class ResumeParser:
#     """
#     Orchestrates the resume parsing pipeline:
#     1. Extraction (PDF/DOCX)
#     2. Cleaning
#     3. Section Classification
#     """
    
#     def __init__(self):
#         self.classifier = SectionClassifier()
#         self.skill_extractor = SkillExtractor()

#     def parse_file(self, file_path: str) -> Dict[str, Any]:
#         """
#         Processes a resume file and returns structured data.
#         """
#         ext = os.path.splitext(file_path)[1].lower()
#         raw_text = ""
        
#         if ext == '.pdf':
#             raw_text = extract_text_from_pdf(file_path)
#         elif ext == '.docx':
#             raw_text = extract_text_from_docx(file_path)
#         else:
#             log.error(f"Unsupported resume format: {ext}")
#             return {}

#         if not raw_text:
#             return {}

#         # Clean text
#         cleaned_text = clean_text(raw_text)
        
#         # Segment into sections
#         sections = self.classifier.classify_text(cleaned_text)
#         structured_sections = self.classifier.to_dict(sections)
        
#         # Basic extraction for personal info
#         email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', raw_text)
#         phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', raw_text)
        
#         from datetime import datetime
        
#         # Format into a basic resume structure (placeholder for deeper extraction)
#         resume_data = {
#             "personal_info": {
#                 "full_name": os.path.splitext(os.path.basename(file_path))[0].replace("_", " ").title(),
#                 "email": email_match.group(0) if email_match else "unknown@example.com",
#                 "phone": phone_match.group(0) if phone_match else "000-000-0000"
#             },
#             "summary": structured_sections.get("summary", ""),
#             "experience": [], # Minimum required by schema, to be filled by future experience parser
#             "skills": [], # To be filled below
#             "education": [],
#             "projects": [],
#             "metadata": {
#                 "source_file": os.path.basename(file_path),
#                 "extraction_date": datetime.now().isoformat()
#             }
#         }

#         # Extract Skills using the dedicated engine
#         resume_data["skills"] = self.skill_extractor.extract_skills(structured_sections)

#         return resume_data

# def save_resume_json(data: Dict[str, Any], output_path: str):
#     """Saves the structured resume data to a JSON file."""
#     os.makedirs(os.path.dirname(output_path), exist_ok=True)
#     with open(output_path, 'w', encoding='utf-8') as f:
#         json.dump(data, f, indent=2)



import os
import json
import re
from typing import Dict, Any
from datetime import datetime

from parsers.pdf_parser import extract_text_from_pdf
from parsers.docx_parser import extract_text_from_docx
from parsers.section_classifier import SectionClassifier
from parsers.skill_extractor import SkillExtractor
from utils.text_cleaner import clean_text
from utils.logger import log


class ResumeParser:
    """
    Orchestrates the resume parsing pipeline:
    1. Extraction (PDF/DOCX)
    2. Cleaning
    3. Section Classification
    4. Experience Parsing (NEW)
    """

    def __init__(self):
        self.classifier = SectionClassifier()
        self.skill_extractor = SkillExtractor()

    # -----------------------------
    # NEW: Experience Parser
    # -----------------------------
    def parse_experience_section(self, text: str):
        """
        Extracts role, company, and dates from experience section.
        Works for basic patterns like:
        Software Engineer at Google (Jan 2020 - Mar 2023)
        """

        pattern = r"(.*?) at (.*?) \((.*?) - (.*?)\)"
        matches = re.findall(pattern, text)

        experiences = []

        for role, company, start, end in matches:
            experiences.append({
                "role": role.strip(),
                "company": company.strip(),
                "start_date": start.strip(),
                "end_date": end.strip()
            })

        return experiences

    # -----------------------------
    # MAIN FUNCTION
    # -----------------------------
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        Processes a resume file and returns structured data.
        """

        ext = os.path.splitext(file_path)[1].lower()
        raw_text = ""

        if ext == '.pdf':
            raw_text = extract_text_from_pdf(file_path)
        elif ext == '.docx':
            raw_text = extract_text_from_docx(file_path)
        else:
            log.error(f"Unsupported resume format: {ext}")
            return {}

        if not raw_text:
            return {}

        # Clean text
        cleaned_text = clean_text(raw_text)

        # Segment into sections
        sections = self.classifier.classify_text(cleaned_text)
        structured_sections = self.classifier.to_dict(sections)

        # Extract personal info
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', raw_text)
        phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', raw_text)

        # -----------------------------
        # NEW: Extract Experience Section
        # -----------------------------
        experience_text = structured_sections.get("experience", "")
        parsed_experience = self.parse_experience_section(experience_text)

        # -----------------------------
        # Final Resume JSON
        # -----------------------------
        resume_data = {
            "personal_info": {
                "full_name": os.path.splitext(os.path.basename(file_path))[0].replace("_", " ").title(),
                "email": email_match.group(0) if email_match else "unknown@example.com",
                "phone": phone_match.group(0) if phone_match else "000-000-0000"
            },
            "summary": structured_sections.get("summary", ""),
            
            # ✅ FIXED HERE
            "experience": parsed_experience,

            "skills": [],
            "education": [],
            "projects": [],
            "metadata": {
                "source_file": os.path.basename(file_path),
                "extraction_date": datetime.now().isoformat()
            }
        }

        # Extract Skills
        resume_data["skills"] = self.skill_extractor.extract_skills(structured_sections)

        return resume_data


# -----------------------------
# SAVE FUNCTION
# -----------------------------
def save_resume_json(data: Dict[str, Any], output_path: str):
    """Saves the structured resume data to a JSON file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
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



# import os
# import json
# import re
# from typing import Dict, Any
# from datetime import datetime

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
#     4. Experience Parsing
#     """

#     def __init__(self):
#         self.classifier = SectionClassifier()
#         self.skill_extractor = SkillExtractor()

#     # -----------------------------
#     # EXPERIENCE PARSER (FIXED)
#     # -----------------------------
#     def parse_experience_section(self, text: str):
#         experiences = []

#     # Clean weird characters
#     text = re.sub(r"\(cid:\d+\)", "", text)

#     # Pattern to extract full experience block
#     pattern = r"([A-Za-z ]+)\s+(Amazon|Google|Microsoft|Meta|Apple)\s*\((.*?)\)"

#     matches = re.findall(pattern, text)

#     for role, company, date_block in matches:

#         # Split dates safely
#         dates = re.split(r"-|–|to", date_block)

#         start = dates[0].strip()
#         end = dates[1].strip() if len(dates) > 1 else "Present"

#         experiences.append({
#             "role": role.strip(),
#             "company": company.strip(),
#             "start_date": start,
#             "end_date": end
#         })

#     return experiences
#     # def parse_experience_section(self, text: str):
#     #     experiences = []

#     #     lines = [line.strip() for line in text.split("\n") if line.strip()]

#     #     for i in range(len(lines)):
#     #         line = lines[i]

#     #         # Detect date pattern
#     #         if re.search(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)", line):

#     #             role = lines[i-2] if i >= 2 else ""
#     #             company = lines[i-1] if i >= 1 else ""

#     #             # Split dates
#     #             dates = re.split(r"-|–|to", line)
#     #             start = dates[0].strip()
#     #             end = dates[1].strip() if len(dates) > 1 else "Present"

#     #             experiences.append({
#     #                 "role": role,
#     #                 "company": company,
#     #                 "start_date": start,
#     #                 "end_date": end
#     #             })

#         # return experiences

#     # -----------------------------
#     # MAIN FUNCTION
#     # -----------------------------
#     def parse_file(self, file_path: str) -> Dict[str, Any]:

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
#         print("\n===== RAW TEXT START =====\n")
#         print(raw_text[:1000])
#         print("\n===== RAW TEXT END =====\n")

#         # Clean text
#         cleaned_text = clean_text(raw_text)

#         # Section classification
#         sections = self.classifier.classify_text(cleaned_text)
#         structured_sections = self.classifier.to_dict(sections)

#         # Extract personal info
#         email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', raw_text)
#         phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', raw_text)

#         # -----------------------------
#         # EXPERIENCE EXTRACTION
#         # -----------------------------
#         experience_text = structured_sections.get("experience", "")

#         if not experience_text:
#             experience_text = raw_text  # fallback

#         parsed_experience = self.parse_experience_section(experience_text)

#         # -----------------------------
#         # FINAL JSON
#         # -----------------------------
#         resume_data = {
#             "personal_info": {
#                 "full_name": os.path.splitext(os.path.basename(file_path))[0].replace("_", " ").title(),
#                 "email": email_match.group(0) if email_match else "unknown@example.com",
#                 "phone": phone_match.group(0) if phone_match else "000-000-0000"
#             },
#             "summary": structured_sections.get("summary", ""),
#             "experience": parsed_experience,
#             "skills": [],
#             "education": [],
#             "projects": [],
#             "metadata": {
#                 "source_file": os.path.basename(file_path),
#                 "extraction_date": datetime.now().isoformat()
#             }
#         }

#         # Extract skills
#         resume_data["skills"] = self.skill_extractor.extract_skills(structured_sections)

#         return resume_data


# # -----------------------------
# # SAVE FUNCTION
# # -----------------------------
# def save_resume_json(data: Dict[str, Any], output_path: str):
#     os.makedirs(os.path.dirname(output_path), exist_ok=True)

#     with open(output_path, 'w', encoding='utf-8') as f:
#         json.dump(data, f, indent=2)

# # 

# import os
# import json
# import re
# from typing import Dict, Any
# from datetime import datetime

# from parsers.pdf_parser import extract_text_from_pdf
# from parsers.docx_parser import extract_text_from_docx
# from parsers.section_classifier import SectionClassifier
# from parsers.skill_extractor import SkillExtractor
# from utils.text_cleaner import clean_text
# from utils.logger import log


# class ResumeParser:
#     """
#     Resume Parsing Pipeline:
#     1. Extract text (PDF/DOCX)
#     2. Clean text
#     3. Section classification
#     4. Experience extraction
#     """

#     def __init__(self):
#         self.classifier = SectionClassifier()
#         self.skill_extractor = SkillExtractor()

#     # -----------------------------
#     # EXPERIENCE PARSER (FINAL)
#     # -----------------------------
#     def parse_experience_section(self, text: str):
#         experiences = []

#         if not text:
#             return experiences

#         # Remove weird PDF artifacts
#         text = re.sub(r"\(cid:\d+\)", "", text)

#         # Split into lines
#         lines = [line.strip() for line in text.split("\n") if line.strip()]

#         i = 0
#         while i < len(lines):
#             line = lines[i]

#             # Detect date line
#             if re.search(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)", line):

#                 # Extract dates
#                 date_match = re.findall(
#                     r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*\d{4}|Present",
#                     line
#                 )

#                 if len(date_match) >= 2:
#                     start = date_match[0]
#                     end = date_match[1]
#                 else:
#                     i += 1
#                     continue

#                 # Get company and role from previous lines
#                 company = lines[i - 1] if i >= 1 else ""
#                 role = lines[i - 2] if i >= 2 else ""

#                 # Clean text
#                 role = re.sub(r"[^A-Za-z ]", "", role).strip()
#                 company = re.sub(r"[^A-Za-z ]", "", company).strip()

#                 # Skip noisy entries
#                 # Skip bullet points or descriptions
#                 if role.startswith("•") or company.startswith("•"):
#                     i += 1
#                     continue

#                 if any(word in role.lower() for word in [
#                     "improved", "developed", "built", "designed", "implemented",
#                     "using", "worked", "created", "managed", "optimized"
#                 ]):
#                     i += 1
#                     continue

#                 # Skip long sentences (not roles)
#                 if len(role.split()) > 4:
#                     i += 1
#                     continue

#                 # Skip empty or weird entries
#                 if len(role.strip()) < 3 or len(company.strip()) < 2:
#                     i += 1
#                     continue

#                 if any(x in role.lower() for x in ["experience", "work", "project"]):
#                     i += 1
#                     continue

#                 experiences.append({
#                     "role": role,
#                     "company": company,
#                     "start_date": start,
#                     "end_date": end
#                 })

#             i += 1

#         return experiences

#     # -----------------------------
#     # MAIN PARSER FUNCTION
#     # -----------------------------
#     def parse_file(self, file_path: str) -> Dict[str, Any]:

#         ext = os.path.splitext(file_path)[1].lower()
#         raw_text = ""

#         # Extract text
#         if ext == '.pdf':
#             raw_text = extract_text_from_pdf(file_path)
#         elif ext == '.docx':
#             raw_text = extract_text_from_docx(file_path)
#         else:
#             log.error(f"Unsupported resume format: {ext}")
#             return {}

#         if not raw_text:
#             return {}
#         print("\n===== RAW TEXT START =====\n")
#         print(raw_text[:1000])
#         print("\n===== RAW TEXT END =====\n")

#         # Clean text
#         cleaned_text = clean_text(raw_text)

#         # Section classification
#         sections = self.classifier.classify_text(cleaned_text)
#         structured_sections = self.classifier.to_dict(sections)

#         # Extract personal info
#         email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', raw_text)
#         phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', raw_text)

#         # -----------------------------
#         # EXPERIENCE EXTRACTION
#         # -----------------------------
#         experience_text = structured_sections.get("experience", "")

#         # fallback if section missing
#         if not experience_text:
#             experience_text = raw_text

#         parsed_experience = self.parse_experience_section(experience_text)

#         # -----------------------------
#         # FINAL OUTPUT
#         # -----------------------------
#         resume_data = {
#             "personal_info": {
#                 "full_name": os.path.splitext(os.path.basename(file_path))[0].replace("_", " ").title(),
#                 "email": email_match.group(0) if email_match else "unknown@example.com",
#                 "phone": phone_match.group(0) if phone_match else "000-000-0000"
#             },
#             "summary": structured_sections.get("summary", ""),
#             "experience": parsed_experience,
#             "skills": self.skill_extractor.extract_skills(structured_sections),
#             "education": [],
#             "projects": [],
#             "metadata": {
#                 "source_file": os.path.basename(file_path),
#                 "extraction_date": datetime.now().isoformat()
#             }
#         }

#         return resume_data


# # -----------------------------
# # SAVE FUNCTION
# # -----------------------------
# def save_resume_json(data: Dict[str, Any], output_path: str):
#     os.makedirs(os.path.dirname(output_path), exist_ok=True)

#     with open(output_path, 'w', encoding='utf-8') as f:
#         json.dump(data, f, indent=2)



# import os
# import json
# import re
# from typing import Dict, Any
# from datetime import datetime

# from parsers.pdf_parser import extract_text_from_pdf
# from parsers.docx_parser import extract_text_from_docx
# from parsers.section_classifier import SectionClassifier
# from parsers.skill_extractor import SkillExtractor
# from parsers.experience_parser import enrich_experience
# from utils.text_cleaner import clean_text
# from utils.logger import log


# class ResumeParser:
#     """
#     Resume Parsing Pipeline
#     """

#     def __init__(self):
#         self.classifier = SectionClassifier()
#         self.skill_extractor = SkillExtractor()

#     # -----------------------------
#     # EXPERIENCE PARSER (ROBUST)
#     # -----------------------------
#     def parse_experience_section(self, text: str):
#         experiences = []
#         if not text:
#             return experiences

#         # Clean PDF noise and artifacts (like non-breaking spaces)
#         text = re.sub(r"\(cid:\d+\)", "", text)
        
#         # Normalize horizontal whitespace but preserve newlines
#         text = re.sub(r"[ \t\xa0\u200b]+", " ", text)
        
#         # Normalize various dash types and bullets
#         text = text.replace("–", "-").replace("—", "-").replace("\u2013", "-").replace("\u2014", "-")
#         text = text.replace("\xa0", " ").replace("\ufffd", "-") # Handle replacement characters as dashes        
#         # Normalize bullet points
#         text = text.replace("\u2022", "•").replace("\u00b7", "•").replace("\uf0b7", "•")

#         # Split into lines
#         lines = [line.strip() for line in text.split("\n") if line.strip()]

#         # Common job title keywords to help identify headers when dates are missing
#         TITLE_KEYWORDS = [
#             "Engineer", "Scientist", "Manager", "Intern", "Specialist", "Developer", 
#             "Consultant", "Lead", "Coordinator", "Analyst", "Architect", "Technician",
#             "Specialist", "Assistant", "Director", "Executive", "Associate", "Officer",
#             "Professor", "Teacher", "Instructor", "Member"
#         ]

#         i = 0
#         while i < len(lines):
#             line = lines[i]

#             # Date Pattern: Month YYYY, MM/YYYY, or Present
#             date_part_regex = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s\.\,]*\d{4}|\d{1,2}[/\-]\d{2,4}|Present"
            
#             # 1. Detection: Check if this line looks like a job header (Date or Title)
#             date_matches = re.findall(date_part_regex, line, re.IGNORECASE)
#             # A title is usually a short line containing title keywords
#             is_potential_title = any(kw.lower() in line.lower() for kw in TITLE_KEYWORDS) and len(line.split()) < 10
            
#             if date_matches or is_potential_title:
#                 # Potential New Job Entry
#                 start_date = ""
#                 end_date = "Present"
                
#                 if date_matches:
#                     start_date = date_matches[0]
#                     end_date = date_matches[1] if len(date_matches) > 1 else "Present"
#                 else:
#                     # Look ahead 2 lines for dates if not on same line
#                     for k in range(i + 1, min(i + 3, len(lines))):
#                         future_dates = re.findall(date_part_regex, lines[k], re.IGNORECASE)
#                         if future_dates:
#                             start_date = future_dates[0]
#                             end_date = future_dates[1] if len(future_dates) > 1 else "Present"
#                             break

#                 # Try to extract Role and Company
#                 raw_info = re.sub(date_part_regex, "", line, flags=re.IGNORECASE).strip()
#                 # Remove common separators
#                 raw_info = re.sub(r'^[•\-\|\s]+', '', raw_info).strip()
                
#                 role = ""
#                 company = ""

#                 # Identification Heuristics
#                 if "|" in raw_info:
#                     parts = [p.strip() for p in raw_info.split("|")]
#                     role = parts[0]
#                     company = parts[1] if len(parts) > 1 else ""
#                 elif " at " in raw_info.lower():
#                     parts = re.split(r"\s+at\s+", raw_info, flags=re.IGNORECASE)
#                     role = parts[0]
#                     company = parts[1] if len(parts) > 1 else ""
#                 elif "," in raw_info:
#                     parts = [p.strip() for p in raw_info.split(",")]
#                     role = parts[0]
#                     company = parts[1] if len(parts) > 1 else ""
#                 else:
#                     # Split by space and try to identify which part is the role
#                     parts = raw_info.split()
#                     if any(kw.lower() in raw_info.lower() for kw in TITLE_KEYWORDS):
#                         # Simple split for now, refine if needed
#                         role = raw_info
#                     else:
#                         role = raw_info

#                 # Contextual Fallback for Role/Company
#                 if not role or len(role) < 3 or not company:
#                     # Check prev line if it was short and didn't match anything
#                     if i > 0 and len(lines[i-1]) < 50:
#                         potential_company = lines[i-1]
#                         if not company: company = potential_company
                
#                 # 3. Responsibility Extraction (Same as before but refined)
#                 responsibilities = []
#                 j = i + 1
#                 while j < len(lines):
#                     next_line = lines[j]
                    
#                     # Stop if we see a NEW job header (Date or clear new title)
#                     next_dates = re.findall(date_part_regex, next_line, re.IGNORECASE)
#                     next_is_title = any(kw.lower() in next_line.lower() for kw in TITLE_KEYWORDS) and len(next_line.split()) < 6
                    
#                     if next_dates or (next_is_title and j > i + 1):
#                          break
                    
#                     # Stop if we see a likely section header
#                     if next_line.isupper() and len(next_line.split()) < 4:
#                         break
                    
#                     clean_line = re.sub(r"^[•\u2022\*\-\\s]+", "", next_line).strip()
#                     if clean_line:
#                         if next_line.startswith(("•", "\u2022", "*", "-")):
#                             responsibilities.append(clean_line)
#                         elif responsibilities:
#                             responsibilities[-1] += " " + clean_line
#                         else:
#                             responsibilities.append(clean_line)
#                     j += 1
                
#                 # Only add if we at least found a role or a date
#                 if role or start_date:
#                     experiences.append({
#                         "role": role.strip() if role else "Professional",
#                         "company": company.strip() if company else "Company",
#                         "start_date": start_date if start_date else "N/A",
#                         "end_date": end_date,
#                         "responsibilities": responsibilities
#                     })
                
#                 i = j - 1

#             i += 1

#         return experiences

#     # -----------------------------
#     # MAIN PARSER
#     # -----------------------------
#     def parse_file(self, file_path: str) -> Dict[str, Any]:

#         ext = os.path.splitext(file_path)[1].lower()
#         raw_text = ""

#         # Extract text
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

#         # Section classification
#         sections = self.classifier.classify_text(cleaned_text)
#         structured_sections = self.classifier.to_dict(sections)

#         # Extract personal info
#         email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', raw_text)
#         phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', raw_text)

#         # Get experience section
#         experience_text = structured_sections.get("experience", "")

#         # fallback to full text if section missing
#         if not experience_text:
#             experience_text = raw_text

#         parsed_experience = self.parse_experience_section(experience_text)
        
#         # Enrich experience (calculate durations and total)
#         enriched_exp, total_years = enrich_experience(parsed_experience)

#         # Final JSON
#         resume_data = {
#             "personal_info": {
#                 "full_name": os.path.splitext(os.path.basename(file_path))[0]
#                 .replace("_", " ").title(),
#                 "email": email_match.group(0) if email_match else "unknown@example.com",
#                 "phone": phone_match.group(0) if phone_match else "000-000-0000"
#             },
#             "summary": structured_sections.get("summary", ""),
#             "experience": enriched_exp,
#             "total_experience_years": total_years,
#             "skills": self.skill_extractor.extract_skills(structured_sections),
#             "education": [],
#             "projects": [],
#             "metadata": {
#                 "source_file": os.path.basename(file_path),
#                 "extraction_date": datetime.now().isoformat()
#             }
#         }

#         return resume_data


# # -----------------------------
# # SAVE FUNCTION
# # -----------------------------
# def save_resume_json(data: Dict[str, Any], output_path: str):
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
from parsers.education_parser import EducationParser


class ResumeParser:
    def __init__(self):
        self.classifier = SectionClassifier()
        self.skill_extractor = SkillExtractor()
        self.education_parser = EducationParser()   

    # -----------------------------
    # EXPERIENCE PARSER (FINAL FIX)
    # -----------------------------
    def parse_experience_section(self, text: str):
        experiences = []

        if not text:
            return experiences

        # Clean PDF artifacts
        text = re.sub(r"\(cid:\d+\)", "", text)
        text = text.replace("–", "-").replace("—", "-")

        # 🔥 Step 1: Find all DATE ranges
        date_pattern = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\s*-\s*(Present|[A-Za-z]{3}\s+\d{4})"
        matches = list(re.finditer(date_pattern, text))

        for match in matches:
            date_block = match.group(0)

            start = date_block.split("-")[0].strip()
            end = date_block.split("-")[1].strip()

            # 🔥 Step 2: Look BEFORE the date for role/company
            context = text[:match.start()]

            # Take last 120 chars before date
            context = context[-120:]

            # Try to match "Role | Company"
            rc_match = re.search(r"([A-Za-z ]+)\s*\|\s*([A-Za-z ]+)", context)

            if rc_match:
                role = rc_match.group(1).strip()
                company = rc_match.group(2).strip()
            else:
                # fallback: split last line
                last_line = context.split("\n")[-1]
                parts = last_line.split("|")

                if len(parts) >= 2:
                    role = parts[0].strip()
                    company = parts[1].strip()
                else:
                    continue

            experiences.append({
                "role": role,
                "company": company,
                "start_date": start,
                "end_date": end
            })

        return experiences

    # -----------------------------
    # MAIN PARSER
    # -----------------------------
    def parse_file(self, file_path: str) -> Dict[str, Any]:

        ext = os.path.splitext(file_path)[1].lower()
        raw_text = ""

        # Extract text
        if ext == '.pdf':
            raw_text = extract_text_from_pdf(file_path)
        elif ext == '.docx':
            raw_text = extract_text_from_docx(file_path)
        else:
            log.error(f"Unsupported resume format: {ext}")
            return {}

        if not raw_text:
            return {}

        # Debug (keep for now)
        print("\n===== RAW TEXT START =====\n")
        print(raw_text[:1000])
        print("\n===== RAW TEXT END =====\n")

        # Clean text
        cleaned_text = clean_text(raw_text)

        # Section classification
        sections = self.classifier.classify_text(cleaned_text)
        structured_sections = self.classifier.to_dict(sections)

        # Extract personal info
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', raw_text)
        phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', raw_text)

        # Experience section
        experience_text = structured_sections.get("experience", "")

        if not experience_text:
            experience_text = raw_text  # fallback

        parsed_experience = self.parse_experience_section(experience_text)


        # -----------------------------
        # EDUCATION EXTRACTION  ✅ ADD HERE
        # -----------------------------
        education_text = structured_sections.get("education", "")
        if not education_text:
            education_text = raw_text

        education = self.education_parser.extract_education(education_text)
        certifications = self.education_parser.extract_certifications(education_text)

        # Final JSON
        resume_data = {
            "personal_info": {
                "full_name": os.path.splitext(os.path.basename(file_path))[0]
                .replace("_", " ").title(),
                "email": email_match.group(0) if email_match else "unknown@example.com",
                "phone": phone_match.group(0) if phone_match else "000-000-0000"
            },
            "summary": structured_sections.get("summary", ""),
            "experience": parsed_experience,
            "skills": self.skill_extractor.extract_skills(structured_sections),
            "education": education,
            "certifications": certifications,
            "projects": [],
            "metadata": {
                "source_file": os.path.basename(file_path),
                "extraction_date": datetime.now().isoformat()
            }
        }

        return resume_data


# -----------------------------
# SAVE FUNCTION
# -----------------------------
def save_resume_json(data: Dict[str, Any], output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
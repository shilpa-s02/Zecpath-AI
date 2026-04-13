import os
import re
import json
from typing import Dict, Any, List
from parsers.pdf_parser import extract_text_from_pdf
from parsers.docx_parser import extract_text_from_docx
from utils.logger import log

class JDParser:
    """
    Job Description Parser to convert raw JD text or documents into structured JSON 
    compliant with jd_schema.json.
    """
    
    def __init__(self, schema_path: str = "data/schemas/jd_schema.json"):
        self.schema_path = schema_path
        self.schema = self._load_schema()

    def _load_schema(self) -> Dict[str, Any]:
        try:
            with open(self.schema_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            log.error(f"Failed to load JD schema: {e}")
            return {}

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Extracts text from file and parses it into JD structure."""
        ext = os.path.splitext(file_path)[1].lower()
        text = ""
        
        if ext == '.pdf':
            text = extract_text_from_pdf(file_path)
        elif ext == '.docx':
            text = extract_text_from_docx(file_path)
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            log.error(f"Unsupported file format: {ext}")
            return {}

        return self.parse_text(text)

    def parse_text(self, text: str) -> Dict[str, Any]:
        """
        Parses raw text into the structured JD format.
        Uses heuristics and regex to identify sections and entities.
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if not lines:
            return {}

        jd = {
            "job_title": "",
            "company": "Zecpath AI (Default)", # Placeholder if not found
            "location": "Remote / Not Specified",
            "job_type": "Full-time", # Defaulting to Full-time as per most Tech Lead roles
            "description": "",
            "responsibilities": [],
            "requirements": {
                "skills": [],
                "experience": {
                    "min_years": 0,
                    "preferred_years": 0,
                    "relevant_industries": []
                },
                "education": {
                    "degree_level": "",
                    "field_of_study": "",
                    "is_required": False
                },
                "certifications": []
            },
            "benefits": [],
            "meta": {
                "source": "Text Extraction",
                "internal_id": ""
            }
        }

        # 1. Extract Title (usually first line)
        # Handle format "1. Job Title"
        first_line = lines[0]
        title_match = re.match(r'^(\d+\.)?\s*(.*)', first_line)
        if title_match:
            jd["job_title"] = title_match.group(2).strip()
            jd["meta"]["internal_id"] = title_match.group(1).rstrip('.') if title_match.group(1) else ""

        # 2. Section Parsing
        current_section = None
        sections = {
            "Role Overview": "description",
            "Key Responsibilities": "responsibilities",
            "Required Skills": "skills",
            "Required Skills & Technologies": "skills",
            "Experience & Qualifications": "experience",
            "Experience": "experience"
        }

        for line in lines[1:]:
            # Check for section headers
            header_found = False
            for header, field in sections.items():
                # Section headers usually don't start with bullets and are short
                clean_line = line.strip(':').strip()
                if clean_line.lower() == header.lower() and not line.strip().startswith(('•', '-', '*')):
                    current_section = field
                    header_found = True
                    break
            
            if header_found:
                continue

            if not current_section:
                continue

            # Process based on section
            if current_section == "description":
                jd["description"] += (line + " ")
            elif current_section == "responsibilities":
                jd["responsibilities"].append(self._clean_bullet(line))
            elif current_section == "skills":
                skill_name = self._clean_bullet(line)
                jd["requirements"]["skills"].append({
                    "name": skill_name,
                    "is_mandatory": True,
                    "proficiency_level": "Expert" if "strong" in line.lower() or "expert" in line.lower() else "Intermediate"
                })
            elif current_section == "experience":
                # Extract years from lines like "6-10 years", "7+ years", or "5 years"
                years_match = re.search(r'(\d+)(?:\s*(?:–|-|to|\+)\s*(\d*))?\s*years?', line, re.I)
                if years_match:
                    min_yrs = int(years_match.group(1))
                    jd["requirements"]["experience"]["min_years"] = max(jd["requirements"]["experience"]["min_years"], min_yrs)
                    if years_match.group(2) and years_match.group(2).isdigit():
                        jd["requirements"]["experience"]["preferred_years"] = max(jd["requirements"]["experience"]["preferred_years"], int(years_match.group(2)))
                
                # Check for industries
                if "enterprise" in line.lower():
                    jd["requirements"]["experience"]["relevant_industries"].append("Enterprise")
                if "saas" in line.lower():
                    jd["requirements"]["experience"]["relevant_industries"].append("SaaS")

        # Cleanup
        jd["description"] = jd["description"].strip()
        jd["requirements"]["experience"]["relevant_industries"] = list(set(jd["requirements"]["experience"]["relevant_industries"]))
        
        return jd

    def _clean_bullet(self, text: str) -> str:
        """Removes common bullet symbols."""
        return re.sub(r'^[•\-\*]\s*', '', text).strip()

def save_jd_json(data: Dict[str, Any], output_path: str):
    """Saves the dictionary to a JSON file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

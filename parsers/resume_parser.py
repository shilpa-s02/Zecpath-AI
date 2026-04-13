import os
import json
from typing import Dict, Any
from parsers.pdf_parser import extract_text_from_pdf
from parsers.docx_parser import extract_text_from_docx
from parsers.section_classifier import SectionClassifier
from utils.text_cleaner import clean_text
from utils.logger import log

class ResumeParser:
    """
    Orchestrates the resume parsing pipeline:
    1. Extraction (PDF/DOCX)
    2. Cleaning
    3. Section Classification
    """
    
    def __init__(self):
        self.classifier = SectionClassifier()

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
        
        # Format into a basic resume structure (placeholder for deeper extraction)
        resume_data = {
            "personal_info": {
                "full_name": os.path.splitext(os.path.basename(file_path))[0].replace("_", " ").title()
            },
            "summary": structured_sections.get("summary", ""),
            "experience": [], # To be filled by future experience parser
            "skills": [], # To be filled by future skill parser
            "education": [], # To be filled by future education parser
            "projects": [], # To be filled by future project parser
            "raw_sections": structured_sections,
            "metadata": {
                "source_file": os.path.basename(file_path)
            }
        }

        # Populate structured lists if keys exist in raw_sections
        # Note: This is a bridge. Full parsing logic will follow in other turns.
        if "skills" in structured_sections:
            # Simple split for now as a demonstration
            skills_list = [s.strip() for s in structured_sections["skills"].split(',') if s.strip()]
            resume_data["skills"] = [{"name": s} for s in skills_list]

        return resume_data

def save_resume_json(data: Dict[str, Any], output_path: str):
    """Saves the structured resume data to a JSON file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

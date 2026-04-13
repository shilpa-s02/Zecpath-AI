import re
from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from utils.logger import log

class SectionType(Enum):
    PERSONAL_INFO = "personal_info"
    SUMMARY = "summary"
    WORK_EXPERIENCE = "experience"
    EDUCATION = "education"
    SKILLS = "skills"
    PROJECTS = "projects"
    CERTIFICATIONS = "certifications"
    OTHERS = "others"
    UNKNOWN = "unknown"

@dataclass
class ResumeSection:
    section_type: SectionType
    original_header: str
    content: List[str]

class SectionClassifier:
    """
    Identifies and separates major resume sections using rule-based and heuristic patterns.
    """
    
    # Common headers for each section
    SECTION_KEYWORDS = {
        SectionType.SUMMARY: [
            r"summary", r"professional summary", r"career summary", 
            r"profile", r"professional profile", r"about me", r"objective"
        ],
        SectionType.WORK_EXPERIENCE: [
            r"experience", r"work experience", r"professional experience", 
            r"employment history", r"career history", r"professional background",
            r"work history", r"relevant experience"
        ],
        SectionType.EDUCATION: [
            r"education", r"academic background", r"academic profile", 
            r"academic history", r"qualifications", r"academic qualifications"
        ],
        SectionType.SKILLS: [
            r"skills", r"technical skills", r"core competencies", 
            r"expertise", r"technologies", r"tools", r"technical proficiency",
            r"key skills", r"skill set"
        ],
        SectionType.PROJECTS: [
            r"projects", r"personal projects", r"portfolio", 
            r"academic projects", r"key projects", r"selected projects"
        ],
        SectionType.CERTIFICATIONS: [
            r"certifications", r"awards", r"licenses", 
            r"achievements", r"certifications & awards"
        ]
    }

    # Regex for detecting headers
    # Matches strings that look like headers: short capitalization, optional colon
    HEADER_REGEX = re.compile(r'^([A-Z][A-Za-z&\s]{2,30}):?$')

    def __init__(self):
        # Compile keywords into regex for faster matching
        self.header_patterns = {}
        for section, keywords in self.SECTION_KEYWORDS.items():
            pattern = r'^(?:' + '|'.join(keywords) + r'):?$'
            self.header_patterns[section] = re.compile(pattern, re.IGNORECASE)

    def classify_text(self, text: str) -> List[ResumeSection]:
        """
        Main entry point to segment raw text into ResumeSection objects.
        """
        lines = [line.strip() for line in text.split('\n')]
        sections = []
        
        current_section_type = SectionType.UNKNOWN
        current_header = ""
        current_content = []

        # Start with PERSONAL_INFO by default for the first non-empty lines
        current_section_type = SectionType.PERSONAL_INFO

        for line in lines:
            if not line:
                continue

            detected_type = self._detect_section_header(line)
            
            if detected_type and detected_type != current_section_type:
                # Save previous section if it has content
                if current_content or current_header:
                    sections.append(ResumeSection(
                        section_type=current_section_type,
                        original_header=current_header,
                        content=current_content
                    ))
                
                # Start new section
                current_section_type = detected_type
                current_header = line
                current_content = []
                log.debug(f"Detected section: {detected_type} from header: {line}")
            else:
                current_content.append(line)

        # Append last section
        if current_content or current_header:
            sections.append(ResumeSection(
                section_type=current_section_type,
                original_header=current_header,
                content=current_content
            ))

        return self._post_process(sections)

    def _detect_section_header(self, line: str) -> Optional[SectionType]:
        """
        Heuristic check to see if a line is a section header.
        """
        # A header is usually short
        if len(line.split()) > 4:
            return None
        
        clean_line = line.strip(':').strip()
        
        # Check patterns for each section
        for section, pattern in self.header_patterns.items():
            if pattern.match(clean_line):
                return section
        
        # General header heuristic: ALL CAPS and short
        if clean_line.isupper() and 1 <= len(clean_line.split()) <= 3:
            # If it's all caps but not matched by keywords, it might be a new/unknown section
            # But we only want to return if we are fairly sure.
            # For now, let's just stick to our known keywords or very common ones.
            pass

        return None

    def _post_process(self, sections: List[ResumeSection]) -> List[ResumeSection]:
        """
        Cleans up sections, merges fragments, and handles edge cases.
        """
        processed = []
        for section in sections:
            # Filter out empty lines from content
            section.content = [c for c in section.content if c.strip()]
            
            # If a section was marked UNKNOWN but is at the very top, it's likely PERSONAL_INFO
            if section.section_type == SectionType.UNKNOWN and not processed:
                section.section_type = SectionType.PERSONAL_INFO
            
            processed.append(section)
        
        return processed

    def to_dict(self, sections: List[ResumeSection]) -> Dict[str, Any]:
        """
        Converts the list of ResumeSection objects into a structured dictionary.
        """
        result = {}
        for section in sections:
            key = section.section_type.value
            content_str = "\n".join(section.content)
            
            if key in result:
                # Append if section appears multiple times
                result[key] += "\n" + content_str
            else:
                result[key] = content_str
        
        return result

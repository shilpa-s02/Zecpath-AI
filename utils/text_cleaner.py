import re
import string

def clean_text(text: str) -> str:
    """
    Main cleaning pipeline for resume text.
    - Standardizes whitespace
    - Removes noise symbols
    - Normalizes headings
    - Cleans non-printable characters
    """
    if not text:
        return ""

    # 1. Normalize line endings and whitespace
    text = text.replace('\r', '\n')
    
    # 2. Identify common resume headings and standardize them
    # Example: "S K I L L S" or "EXPERIENCE:" -> "SKILLS", "EXPERIENCE"
    headings = ["SKILLS", "EXPERIENCE", "EDUCATION", "SUMMARY", "CERTIFICATIONS", "LANGUAGES", "PROJECTS", "PERSONAL INFO"]
    for heading in headings:
        # Regex to find heading with varying spaces and potential colon at end
        # Matches "S K I L L S", "Skills:", "SKILLS   "
        pattern = r'(?i)\b' + r'\s*'.join(list(heading)) + r'\s*[:\-]*'
        text = re.sub(pattern, f"\n\n{heading}\n", text)

    # 3. Remove non-printable characters
    printable = set(string.printable)
    text = ''.join(filter(lambda x: x in printable, text))

    # 4. Normalize multiple newlines into double newlines for paragraph separation
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 5. Normalize horizontal whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    
    # 6. Final strip
    text = text.strip()

    return text

def normalize_caps(text: str) -> str:
    """
    Experimental: Standardizes capitalization while trying to preserve proper nouns.
    For now, we keep the original case as it's often better for NER/Parsing.
    """
    return text

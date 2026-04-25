import re

def parse_experience_section(text: str):
    experiences = []
    if not text:
        return experiences

    # Clean PDF noise and artifacts (like non-breaking spaces)
    text = re.sub(r"\(cid:\d+\)", "", text)
    # text = text.replace("", " ").replace("\xa0", " ") # The character might be different
    
    # Let's try more aggressive whitespace normalization
    text = re.sub(r"[\s\xa0\u200b]+", " ", text)
    
    # Normalize various dash types
    text = text.replace("–", "-").replace("—", "-").replace("\u2013", "-").replace("\u2014", "-")

    # Split into lines
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    
    print(f"Total lines: {len(lines)}")

    i = 0
    while i < len(lines):
        line = lines[i]
        print(f"Checking line: {line}")

        # Date Pattern: Month YYYY, MM/YYYY, or Present
        date_part_regex = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s\.\,]*\d{4}|\d{1,2}[/\-]\d{2,4}|Present"
        
        date_matches = re.findall(date_part_regex, line, re.IGNORECASE)
        print(f"Date matches: {date_matches}")

        if date_matches:
            start_date = date_matches[0]
            end_date = date_matches[1] if len(date_matches) > 1 else "Present"

            remaining_text = re.sub(date_part_regex, "", line, flags=re.IGNORECASE).strip()
            remaining_text = re.sub(r"[-|,\u2022]", " ", remaining_text).strip()
            
            role = ""
            company = ""
            
            parts = [p.strip() for p in remaining_text.split() if p.strip()]
            if len(parts) >= 2:
                company = parts[-1]
                role = " ".join(parts[:-1])
            elif len(parts) == 1:
                role = parts[0]
            
            if not role or not company:
                if i > 0:
                    prev_line = lines[i-1]
                    if "|" in prev_line:
                        p_parts = prev_line.split("|")
                        if not role: role = p_parts[0].strip()
                        if not company: company = p_parts[1].strip()
                    elif not role and not company:
                        role = prev_line
                        if i > 1:
                            company = lines[i-2]

            responsibilities = []
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                if re.search(date_part_regex, next_line, re.IGNORECASE):
                    break
                
                if next_line.startswith(("\u2022", "*", "-", "")) or len(next_line.split()) > 3:
                    clean_bullet = re.sub(r"^[\u2022\*\-\\s]+", "", next_line).strip()
                    if clean_bullet:
                        responsibilities.append(clean_bullet)
                j += 1
            
            experiences.append({
                "role": role,
                "company": company,
                "start_date": start_date,
                "end_date": end_date,
                "responsibilities": responsibilities
            })
            i = j - 1
        i += 1
    return experiences

sample_text = """
PROFESSIONAL EXPERIENCE
Senior Project Manager | ABC Corporation Jan 2020  Present
• Led a team of 10 to successfully deliver 5 high-priority software projects ahead of schedule.
• Implemented a new automated reporting system that saved the department 20 hours of manual work per
week.
Operations Specialist | XYZ Solutions June 2017  Dec 2019
• Optimized supply chain logistics, resulting in a 12% reduction in shipping delays.
"""

results = parse_experience_section(sample_text)
print("\nResults:")
import json
print(json.dumps(results, indent=2))

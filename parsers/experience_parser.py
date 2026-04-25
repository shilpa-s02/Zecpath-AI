import re
from datetime import datetime
from dateutil import parser
from utils.logger import log

def clean_date(date_str: str):
    """
    Cleans messy date strings and extracts a parsable date.
    Examples:
    'Jan 2020' -> 'Jan 2020'
    'June 2017' -> 'June 2017'
    'Present' -> 'Present'
    '06/2017' -> '06/2017'
    """
    if not date_str:
        return None
    
    date_str = date_str.strip()
    
    if date_str.lower() == "present":
        return "Present"

    # Extract common date patterns (Month YYYY or MM/YYYY)
    match = re.search(
        r"([A-Za-z]{3,9}\s+\d{4})|(\d{1,2}/\d{2,4})|(\d{1,2}-\d{2,4})", 
        date_str
    )
    
    if match:
        return match.group(0)
    
    return date_str


def calculate_duration(start: str, end: str) -> float:
    """
    Calculates the duration between two dates in years.
    """
    try:
        clean_start = clean_date(start)
        if not clean_start:
            return 0.0
            
        start_date = parser.parse(clean_start)

        clean_end = clean_date(end)
        if not clean_end or clean_end.lower() == "present":
            end_date = datetime.now()
        else:
            end_date = parser.parse(clean_end)

        duration_days = (end_date - start_date).days
        return round(max(0, duration_days / 365.25), 2)
    except Exception as e:
        log.warning(f"Could not calculate duration for {start} to {end}: {e}")
        return 0.0


def enrich_experience(experiences: list):
    """
    Enriches experience objects with duration and calculates total experience.
    """
    total_exp = 0.0
    
    for exp in experiences:
        start = exp.get("start_date", "")
        end = exp.get("end_date", "Present")
        
        duration = calculate_duration(start, end)
        exp["duration"] = duration
        total_exp += duration
        
    return experiences, round(total_exp, 2)
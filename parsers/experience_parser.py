from datetime import datetime
from dateutil import parser

def calculate_duration(start, end):
    start_date = parser.parse(start)

    if end.lower() == "present":
        end_date = datetime.now()
    else:
        end_date = parser.parse(end)

    return round((end_date - start_date).days / 365, 2)


def enrich_experience(experiences):
    total_exp = 0

    for exp in experiences:
        duration = calculate_duration(exp["start_date"], exp["end_date"])
        exp["duration"] = duration
        total_exp += duration

    return experiences, round(total_exp, 2)
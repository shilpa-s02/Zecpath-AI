import re

date_part_regex = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s\.\,]*\d{4}|\d{1,2}[/\-]\d{2,4}|Present"

test_line = " Led a team of 10 to successfully deliver 5 high-priority software projects ahead of schedule."
match = re.search(date_part_regex, test_line, re.IGNORECASE)
if match:
    print(f"Match found: {match.group(0)}")
else:
    print("No match")

test_line_2 = "Operations Specialist | XYZ Solutions June 2017  Dec 2019"
match_2 = re.findall(date_part_regex, test_line_2, re.IGNORECASE)
print(f"Matches for line 2: {match_2}")

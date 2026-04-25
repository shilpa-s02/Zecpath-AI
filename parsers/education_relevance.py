def calculate_education_relevance(education, job_description):
    score = 0

    jd = job_description.lower()

    for edu in education:
        field = edu.get("field", "").lower()
        degree = edu.get("degree", "").lower()

        # Field match
        if field and field in jd:
            score += 0.6

        # Degree weight
        if "master" in degree:
            score += 0.3
        elif "bachelor" in degree:
            score += 0.2

    return round(min(score, 1.0), 2)
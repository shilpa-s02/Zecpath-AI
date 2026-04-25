import re


class EducationParser:
    def __init__(self):
        pass

    # -----------------------------
    # DEGREE NORMALIZATION
    # -----------------------------
    def normalize_degree(self, degree: str):
        degree = degree.lower()

        if "bachelor" in degree or "b.tech" in degree or "bsc" in degree:
            return "Bachelor's"
        if "master" in degree or "m.tech" in degree or "msc" in degree:
            return "Master's"
        if "phd" in degree or "doctor" in degree:
            return "PhD"

        return degree.title()

    # -----------------------------
    # CERTIFICATION CATEGORY TAGGING
    # -----------------------------
    def categorize_certification(self, cert: str):
        cert_lower = cert.lower()

        if any(x in cert_lower for x in ["aws", "azure", "gcp", "cloud"]):
            return "Cloud"
        if any(x in cert_lower for x in ["python", "java", "sql", "programming"]):
            return "Technical"
        if any(x in cert_lower for x in ["pmp", "scrum", "agile"]):
            return "Management"
        if any(x in cert_lower for x in ["data", "machine learning", "ai"]):
            return "Data/AI"

        return "Other"

    # -----------------------------
    # EDUCATION EXTRACTION
    # -----------------------------
    # def extract_education(self, text: str):
    #     education_list = []

    #     if not text:
    #         return education_list

    #     lines = [line.strip() for line in text.split("\n") if line.strip()]

    #     for line in lines:

    #         # 🎯 Pattern: Degree in Field - University (Year)
    #         match = re.search(
    #             r"(Bachelor|Master|B\.Tech|M\.Tech|BSc|MSc|PhD)[^,\n]*"
    #             r"(?:in\s+([A-Za-z ]+))?.*?"
    #             r"(?:from\s+)?([A-Za-z .]+)"
    #             r".*?(\d{4})",
    #             line,
    #             re.IGNORECASE
    #         )

    #         if match:
    #             degree_raw = match.group(1)
    #             field = match.group(2) if match.group(2) else ""
    #             institution = match.group(3)
    #             year = match.group(4)

    #             education_list.append({
    #                 "degree": self.normalize_degree(degree_raw),
    #                 "field": field.strip(),
    #                 "institution": institution.strip(),
    #                 "graduation_year": year
    #             })

    #     return education_list

    def extract_education(self, text: str):
        education_list = []

        if not text:
            return education_list

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        for line in lines:

            # Check if line contains degree + year
            if not re.search(r"\d{4}", line):
                continue

            if not any(word in line.lower() for word in [
                "bachelor", "master", "b.tech", "m.tech", "bsc", "msc", "phd"
            ]):
                continue

            degree = ""
            field = ""
            institution = ""
            year = ""

            # -----------------------------
            # YEAR
            # -----------------------------
            year_match = re.search(r"\d{4}", line)
            if year_match:
                year = year_match.group()

            # -----------------------------
            # DEGREE
            # -----------------------------
            if "bachelor" in line.lower() or "b.tech" in line.lower() or "bsc" in line.lower():
                degree = "Bachelor's"
            elif "master" in line.lower() or "m.tech" in line.lower() or "msc" in line.lower():
                degree = "Master's"
            elif "phd" in line.lower():
                degree = "PhD"

            # -----------------------------
            # FIELD
            # -----------------------------
            field_match = re.search(r"in ([A-Za-z &]+)", line, re.IGNORECASE)
            if field_match:
                field = field_match.group(1).strip()

            # -----------------------------
            # INSTITUTION
            # -----------------------------
            # Try comma-based split first
            parts = line.split(",")

            if len(parts) >= 2:
                institution = parts[-2].strip()
            else:
                # fallback: after "from"
                inst_match = re.search(r"from ([A-Za-z .]+)", line)
                if inst_match:
                    institution = inst_match.group(1).strip()

            education_list.append({
                "degree": degree,
                "field": field,
                "institution": institution,
                "graduation_year": year
            })

        return education_list
    # -----------------------------
    # CERTIFICATION EXTRACTION
    # -----------------------------
    def extract_certifications(self, text: str):
        certifications = []

        if not text:
            return certifications

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        for line in lines:

            # 🎯 Detect certification keywords
            if any(word in line.lower() for word in [
                "certified", "certification", "certificate"
            ]):
                certifications.append({
                    "name": line,
                    "category": self.categorize_certification(line)
                })

        return certifications


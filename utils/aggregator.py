import os
import json
from typing import List, Dict, Any

def aggregate_resume_results(resume_data_dir: str, output_file: str):
    """
    Aggregates individual resume JSON results into a single summary file.
    """
    if not os.path.exists(resume_data_dir):
        return
    
    all_experiences = []
    total_years = 0.0
    
    files = [f for f in os.listdir(resume_data_dir) if f.endswith('.json')]
    
    for filename in files:
        file_path = os.path.join(resume_data_dir, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                exp_list = data.get("experience", [])
                for exp in exp_list:
                    # Capture role, company and duration
                    all_experiences.append({
                        "role": exp.get("role"),
                        "company": exp.get("company"),
                        "years": exp.get("duration", 0),
                        "source": filename
                    })
                
                total_years += data.get("total_experience_years", 0.0)
        except Exception:
            continue

    result = {
        "total_experience": round(total_years, 2),
        "overall_relevance": 100 if all_experiences else 0, # Placeholder logic
        "roles": all_experiences
    }
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    aggregate_resume_results("output/resume_data", "output/day10_results/result.json")

import json
import re
import os
from typing import Dict, List, Any, Set
from utils.logger import log

class SkillExtractor:
    """
    Extracts, normalizes, and scores skills from resume text using a master dictionary.
    Supports synonyms, skill stacks, and section-based confidence scoring.
    """

    def __init__(self, dictionary_path: str = None):
        if dictionary_path is None:
            # Default path relative to project root
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            dictionary_path = os.path.join(base_dir, "data", "vocabulary", "skills.json")
        
        self.dictionary_path = dictionary_path
        self.skills_dict = self._load_dictionary()
        self.patterns = self._prepare_patterns()

    def _load_dictionary(self) -> Dict[str, Any]:
        """Loads and validates the skill dictionary."""
        try:
            if not os.path.exists(self.dictionary_path):
                log.warning(f"Skill dictionary not found at {self.dictionary_path}. Using empty dictionary.")
                return {}
            
            with open(self.dictionary_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            log.error(f"Error loading skill dictionary: {e}")
            return {}

    def _prepare_patterns(self) -> Dict[str, re.Pattern]:
        """
        Creates regex patterns for each canonical skill name and its synonyms.
        Handled as case-insensitive word boundaries.
        """
        patterns = {}
        for skill_name, info in self.skills_dict.items():
            variants = [skill_name] + info.get("synonyms", [])
            # Escape variants and join with OR, ensuring word boundaries
            # Handle special characters like .js, c++, etc.
            escaped_variants = [re.escape(v) for v in variants]
            pattern_str = r'\b(?:' + '|'.join(escaped_variants) + r')\b'
            patterns[skill_name] = re.compile(pattern_str, re.IGNORECASE)
        return patterns

    def extract_skills(self, sections: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Main entry point: Extracts skills from provided text sections.
        Returns a list of structured skill objects with confidence scores.
        """
        extracted = {}

        # Section weights for confidence scoring
        section_weights = {
            "skills": 1.0,
            "experience": 0.8,
            "summary": 0.7,
            "projects": 0.7,
            "certifications": 0.9,
            "others": 0.5
        }

        for section_name, text in sections.items():
            if not text:
                continue
            
            weight = section_weights.get(section_name, 0.5)
            
            for skill_name, pattern in self.patterns.items():
                matches = pattern.findall(text)
                if matches:
                    # Calculate confidence
                    info = self.skills_dict[skill_name]
                    base_priority = info.get("priority", 1.0)
                    
                    # Score = Base Priority * Section Weight
                    # For now, we take the highest score if found in multiple sections
                    score = round(base_priority * weight, 2)
                    
                    # Map confidence to proficiency
                    proficiency = "Expert" if score >= 0.9 else "Intermediate" if score >= 0.6 else "Beginner"
                    
                    if skill_name not in extracted or score > extracted[skill_name].get("_score", 0):
                        extracted[skill_name] = {
                            "name": skill_name,
                            "category": info.get("category", "Technical"),
                            "proficiency": proficiency,
                            "years_of_experience": 0, # Placeholder
                            "_score": score # Internal helper for deduplication
                        }
                    
                    # Expand stacks
                    if "stack" in info:
                        for sub_skill in info["stack"]:
                            if sub_skill in self.skills_dict:
                                sub_info = self.skills_dict[sub_skill]
                                # Sub-skills from stacks get a slight penalty (0.9) to denote they were inferred
                                sub_score = round(sub_info.get("priority", 1.0) * weight * 0.9, 2)
                                sub_proficiency = "Expert" if sub_score >= 0.9 else "Intermediate" if sub_score >= 0.6 else "Beginner"
                                
                                if sub_skill not in extracted or sub_score > extracted[sub_skill].get("_score", 0):
                                    extracted[sub_skill] = {
                                        "name": sub_skill,
                                        "category": sub_info.get("category", "Technical"),
                                        "proficiency": sub_proficiency,
                                        "years_of_experience": 0,
                                        "inferred_from": skill_name,
                                        "_score": sub_score
                                    }

        # Convert dictionary to sorted list by score, then remove internal score
        result = list(extracted.values())
        result.sort(key=lambda x: x["_score"], reverse=True)
        for item in result:
            item.pop("_score", None)
        return result

    def normalize_name(self, skill_variant: str) -> str:
        """Helper to find the canonical name for a variant."""
        for skill_name, pattern in self.patterns.items():
            if pattern.match(skill_variant):
                return skill_name
        return skill_variant

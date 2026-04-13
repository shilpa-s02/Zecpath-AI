import pytest
from parsers.skill_extractor import SkillExtractor

@pytest.fixture
def extractor():
    return SkillExtractor()

def test_basic_extraction(extractor):
    sections = {
        "skills": "Python, JavaScript, and React"
    }
    results = extractor.extract_skills(sections)
    names = [r["name"] for r in results]
    assert "Python" in names
    assert "JavaScript" in names
    assert "React" in names

def test_synonym_matching(extractor):
    sections = {
        "skills": "Experienced with JS and python3"
    }
    results = extractor.extract_skills(sections)
    names = [r["name"] for r in results]
    assert "JavaScript" in names
    assert "Python" in names

def test_stack_expansion(extractor):
    sections = {
        "skills": "Fullstack developer using MERN"
    }
    results = extractor.extract_skills(sections)
    names = [r["name"] for r in results]
    assert "MERN Stack" in names
    assert "MongoDB" in names
    assert "Express.js" in names
    assert "React" in names
    assert "Node.js" in names

def test_confidence_scoring(extractor):
    sections_high = {"skills": "Python"}
    sections_low = {"summary": "Python"}
    
    score_high = extractor.extract_skills(sections_high)[0]["confidence"]
    score_low = extractor.extract_skills(sections_low)[0]["confidence"]
    
    assert score_high > score_low

def test_normalization(extractor):
    assert extractor.normalize_name("JS") == "JavaScript"
    assert extractor.normalize_name("python3") == "Python"
    assert extractor.normalize_name("UnknownSkill") == "UnknownSkill"

def test_multi_word_skill(extractor):
    sections = {
        "experience": "Managed project management tasks and UI design"
    }
    results = extractor.extract_skills(sections)
    names = [r["name"] for r in results]
    assert "Project Management" in names
    assert "User Interface Design" in names

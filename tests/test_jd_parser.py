import pytest
import os
import json
from parsers.jd_parser import JDParser

@pytest.fixture
def parser():
    return JDParser()

@pytest.fixture
def sample_jd_text():
    return """
1. Senior Technical Lead
Role Overview
The Senior Technical Lead will lead the engineering team to build scalable systems.
Key Responsibilities
• Lead architecture design
• Mentor junior developers
Required Skills
• Python
• AWS
Experience
• 10+ years of experience
"""

def test_parse_text(parser, sample_jd_text):
    data = parser.parse_text(sample_jd_text)
    
    assert data["job_title"] == "Senior Technical Lead"
    assert any("architecture design" in r for r in data["responsibilities"])
    assert len(data["requirements"]["skills"]) == 2
    assert any(s["name"] == "Python" for s in data["requirements"]["skills"])
    assert data["requirements"]["experience"]["min_years"] == 10

def test_schema_validity(parser, sample_jd_text):
    import jsonschema
    data = parser.parse_text(sample_jd_text)
    
    with open(parser.schema_path, 'r') as f:
        schema = json.load(f)
        
    # Should not raise exception
    jsonschema.validate(instance=data, schema=schema)

def test_file_parsing(parser, tmp_path):
    d = tmp_path / "test_jd.txt"
    d.write_text("1. Test Lead\nRole Overview\nTest desc\nKey Responsibilities\n• Test resp\nRequired Skills\n• Test skill\nExperience\n• 5 years", encoding='utf-8')
    
    data = parser.parse_file(str(d))
    assert data["job_title"] == "Test Lead"
    assert data["requirements"]["experience"]["min_years"] == 5

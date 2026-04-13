import pytest
import json
import os
from parsers.section_classifier import SectionClassifier, SectionType

def load_samples():
    path = "data/samples/labeled_resumes.json"
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        return json.load(f)

@pytest.fixture
def classifier():
    return SectionClassifier()

def test_section_classification_accuracy(classifier):
    samples = load_samples()
    assert len(samples) > 0, "No samples found for testing"
    
    total_metrics = {
        "correct_sections": 0,
        "total_sections": 0
    }

    for sample in samples:
        raw_text = sample["raw_text"]
        expected = sample["expected_sections"]
        
        sections = classifier.classify_text(raw_text)
        actual_dict = {}
        for s in sections:
            actual_dict[s.section_type.value] = s.content

        for section_name, expected_content in expected.items():
            total_metrics["total_sections"] += 1
            if section_name in actual_dict:
                # Check if all expected lines are in actual content
                # We use a broad check: are at least 80% of lines found?
                actual_content = actual_dict[section_name]
                matches = sum(1 for line in expected_content if line in actual_content)
                if matches / len(expected_content) >= 0.8:
                    total_metrics["correct_sections"] += 1
                else:
                    print(f"Mismatch in {sample['name']} - Section {section_name}")
                    print(f"Expected: {expected_content}")
                    print(f"Actual: {actual_content}")
            else:
                print(f"Missing section in {sample['name']}: {section_name}")

    accuracy = total_metrics["correct_sections"] / total_metrics["total_sections"]
    print(f"\nOverall Section Detection Accuracy: {accuracy * 100:.2f}%")
    assert accuracy >= 0.8  # Expecting at least 80% accuracy for these simple samples

def test_headers_detection(classifier):
    test_cases = [
        ("WORK EXPERIENCE", SectionType.WORK_EXPERIENCE),
        ("Education:", SectionType.EDUCATION),
        ("Technical Skills", SectionType.SKILLS),
        ("Professional Summary", SectionType.SUMMARY),
        ("Projects", SectionType.PROJECTS),
        ("Certifications", SectionType.CERTIFICATIONS)
    ]
    
    for header, expected_type in test_cases:
        assert classifier._detect_section_header(header) == expected_type

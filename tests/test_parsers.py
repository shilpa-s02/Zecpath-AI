import pytest
import os
from utils.text_cleaner import clean_text
from parsers.pdf_parser import extract_text_from_pdf
from parsers.docx_parser import extract_text_from_docx

# --- Text Cleaner Tests ---

def test_clean_text_basic():
    text = "Hello    World\n\n\nNew   Line"
    cleaned = clean_text(text)
    assert cleaned == "Hello World\n\nNew Line"

def test_clean_text_headings():
    text = "S K I L L S\nPython, Java"
    cleaned = clean_text(text)
    assert "SKILLS" in cleaned
    assert "S K I L L S" not in cleaned

def test_clean_text_non_printable():
    text = "Normal Text \x00\x01 Hidden"
    cleaned = clean_text(text)
    assert "\x00" not in cleaned
    assert "Normal Text Hidden" in cleaned

# --- Parser Structural Tests (Mocking file paths isn't easy here, testing simple logic) ---

def test_pdf_no_file():
    # Test error handling
    result = extract_text_from_pdf("non_existent.pdf")
    assert result == ""

def test_docx_no_file():
    # Test error handling
    result = extract_text_from_docx("non_existent.docx")
    assert result == ""

# --- Integration Logic Tests ---

def test_pipeline_ready():
    # Check if necessary directories exist for pipeline
    assert os.path.isdir("parsers")
    assert os.path.isdir("utils")
    assert os.path.exists("main.py")

if __name__ == "__main__":
    pytest.main([__file__])

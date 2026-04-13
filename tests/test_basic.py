# import pytest
import os
from utils.logger import ai_logger

def test_logger_initialization():
    """
    Test if the logger is correctly initialized and can write logs.
    """
    try:
        ai_logger.info("Testing logger initialization...")
        assert True
    except Exception as e:
        pytest.fail(f"Logger failed with error: {e}")

def test_project_structure():
    """
    Test if the key project directories exist relative to the project root.
    """
    # Determine project root relative to this test file
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # Expected directories
    folders = ["data", "parsers", "ats_engine", "screening_ai", "interview_ai", "scoring", "utils", "tests"]
    
    for folder in folders:
        folder_path = os.path.join(project_root, folder)
        assert os.path.exists(folder_path), f"Directory '{folder}' does not exist at {folder_path}"
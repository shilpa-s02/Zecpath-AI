import pytest
from utils.logger import ai_logger

def test_logger_initialization():
    """
    Test if the logger is correctly initialised and can write logs.
    """
    try:
        ai_logger.info("Testing logger initialization...")
        assert True
    except Exception as e:
        pytest.fail(f"Logger failed with error: {e}")

def test_project_structure():
    """
    Test if the key project directories exist.
    """
    import os
    folders = ["data", "parsers", "ats_engine", "screening_ai", "interview_ai", "scoring", "utils", "tests"]
    for folder in folders:
        assert os.path.exists(folder), f"Directory {folder} does not exist"

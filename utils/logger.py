import os
import sys
from loguru import logger

def setup_logger(log_file="logs/ai_system.log"):
    """
    Sets up the logger with common configuration.
    """
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Configure Loguru
    config = {
        "handlers": [
            {"sink": sys.stdout, "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"},
            {"sink": log_file, "serialize": False, "rotation": "10 MB", "retention": "1 week"},
        ],
    }
    logger.configure(**config)
    return logger

# Global logger instance
ai_logger = setup_logger()

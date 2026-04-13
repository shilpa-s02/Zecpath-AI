# import sys
# import os
# from loguru import logger
# from utils.logger import log

# # Initialize a default logger instance

# ai_logger = setup_logger()
# def setup_logger(log_file="logs/extraction.log"):
#     """
#     Configures the logger with console and file handlers.
#     """
#     # Create logs directory if it doesn't exist
#     os.makedirs(os.path.dirname(log_file), exist_ok=True)

#     # Remove default handler
#     logger.remove()

#     # Add console handler with a clean format
#     logger.add(
#         sys.stderr,
#         format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
#         level="INFO"
#     )

#     # Add file handler with rotation and retention for production readiness
#     logger.add(
#         log_file,
#         format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
#         level="DEBUG",
#         rotation="10 MB",
#         retention="1 month",
#         compression="zip"
#     )

#     return logger


# # Initialize a default logger instance
# log = setup_logger()

import sys
import os
from loguru import logger

def setup_logger(log_file="logs/extraction.log"):
    """
    Configures the logger with console and file handlers.
    """
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Remove default handler
    logger.remove()

    # Add console handler
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )

    # Add file handler
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="1 month",
        compression="zip"
    )

    return logger

# ✅ Only one logger instance at module level
ai_logger = setup_logger()
log = ai_logger  # optional alias if you want

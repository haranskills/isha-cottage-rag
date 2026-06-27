import sys
from loguru import logger
from src.config import LOG_LEVEL, LOG_FILE

logger.remove()  # Remove default handler

# Console output
logger.add(
    sys.stdout,
    level=LOG_LEVEL,
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan> - {message}"
)

# File output (rotates at 10MB)
logger.add(
    LOG_FILE,
    level=LOG_LEVEL,
    rotation="10 MB",
    retention="7 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} - {message}"
)
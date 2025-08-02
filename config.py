"""
CuisineCraft Configuration Module
Centralizes all key settings for consistent, maintainable project-wide configuration management.
Loads settings from a .env file if present.
"""

import os
from typing import Final
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file if it exists

# Database file location (relative to project root)
DB_FILENAME: Final[str] = os.getenv("DB_FILENAME", "CuisineCraft.db")
DB_PATH: Final[str] = os.getenv("DB_PATH", "Database")

# Log file location
LOG_FILENAME: Final[str] = os.getenv("LOG_FILENAME", "RecipeManager.log")
LOG_PATH: Final[str] = os.getenv("LOG_PATH", "logs")

# Default export directory for menus and shopping lists
EXPORT_DIR: Final[str] = os.getenv("EXPORT_DIR", "exports")

# Debug mode flag
DEBUG: Final[bool] = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes")

LOGGER_LEVEL: Final[str] = os.getenv("LOGGER_LEVEL", "INFO")

# Default CSV delimiter
CSV_DELIMITER: Final[str] = os.getenv("CSV_DELIMITER", ",")

# Date format for exports
EXPORT_DATE_FORMAT: Final[str] = os.getenv("EXPORT_DATE_FORMAT", "%d-%m-%Y")

"""
Script to clear all LLM caches and model lists for a clean slate.
This removes all cached responses and model lists for all LLMs, allowing you to start fresh with new API calls and model queries. Use this when you want to reset the state of your LLM interactions or if you encounter issues with stale cache data.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import os
import shutil
import logging
from logging.handlers import RotatingFileHandler

# Logging setup
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(ROOT, 'data', 'logs', 'docs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'clear_caches.log')
logger = logging.getLogger("clear_caches")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOG_FILE, maxBytes=512*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)

# List of cache directories or files to remove
CACHE_PATHS = [
    os.path.join("data", "llm"),
    os.path.join("data", "llm_cache"),
    os.path.join("data", "model_lists"),
]

# Remove cache directories/files
logger.info("Starting clear_caches.py script")
for path in CACHE_PATHS:
    if os.path.exists(path):
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
                logger.info(f"Removed directory: {path}")
            else:
                os.remove(path)
                logger.info(f"Removed file: {path}")
        except Exception as e:
            logger.error(f"Could not remove {path}: {e}")
    else:
        logger.warning(f"Not found: {path}")
        
# Final log message
logger.info("clear_caches.py completed successfully.")
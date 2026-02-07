"""
Script to clean up documentation assets.
This is meant to be run before building the documentation to ensure that any old copies of key markdown files
 (like README.md, ROADMAP.md, etc.) are removed from the docs/ directory before new ones are copied over by
 update_docs_assets.py. This helps prevent confusion and ensures that the docs/ directory only contains the
 most up-to-date versions of these files.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
import os
import logging
from logging.handlers import RotatingFileHandler

# Files to remove from docs/
DOC_FILES = [
    "README.md",
    "ROADMAP.md",
    "CHANGE_LOG.md",
    "CODE_OF_CONDUCT.md",
    "SETUP_GUIDE_USER.md",
    "SETUP_GUIDE_DEV.md",
    "API_KEYS.md",
    "CONTRIBUTORS.md",
    "LICENSE.md",
    "requirements.md",
    "requirements-dev.md",
    "SECURITY.md",
    "CONTACT.md",
]

# Paths
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

# Logging setup
LOG_DIR = os.path.join(ROOT, 'data', 'logs', 'docs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'clean_docs_assets.log')
logger = logging.getLogger("clean_docs_assets")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOG_FILE, maxBytes=512*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)

# Remove old copies of doc files from docs/
logger.info("Starting clean_docs_assets.py script")
for fname in DOC_FILES:
    fpath = os.path.join(DOCS, fname)
    try:
        if os.path.exists(fpath):
            os.remove(fpath)
            logger.info(f"Removed: {fname}")
        else:
            logger.warning(f"{fname} not found in docs/.")
    except Exception as e:
        logger.error(f"Could not remove {fname}: {e}")

# Final log message
logger.info("clean_docs_assets.py completed successfully.")
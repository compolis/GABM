"""
Script to clean the project by removing build artifacts and cache files.
This includes removing the Sphinx build directory (docs/_build), all __pycache__ directories, and all .pyc files. This helps ensure that the project is in a clean state before building documentation or running tests, and prevents issues caused by stale build artifacts or cache files.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.1"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import os
import shutil
import logging
from logging.handlers import RotatingFileHandler

# Logging setup
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_DIR = os.path.join(ROOT, 'data', 'logs', 'docs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'clean_project.log')
logger = logging.getLogger("clean_project")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOG_FILE, maxBytes=512*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)


def _rmtree_onexc(func, path, exc_info):
    """Handle rmtree exceptions, ignoring transient missing-file races."""
    err = exc_info[1] if isinstance(exc_info, tuple) else exc_info
    if isinstance(err, FileNotFoundError):
        logger.warning(f"Skipped missing path while deleting {path}: {err}")
        return
    raise err


def _remove_tree(path):
    """Remove a directory tree if present with robust error handling."""
    if os.path.exists(path):
        shutil.rmtree(path, onexc=_rmtree_onexc)
        logger.info(f"Removed: {path}")
    else:
        logger.info(f"Directory not found: {path}")

# Remove docs/_build
docs_build_dir = os.path.join("docs", "_build")
_remove_tree(docs_build_dir)

# Remove dist/ directory
dist_dir = os.path.join(ROOT, "dist")
_remove_tree(dist_dir)

# Remove build/ directory
build_dir = os.path.join(ROOT, "build")
_remove_tree(build_dir)

# Remove src/gabm.egg-info
egg_info_dir = os.path.join("src", "gabm.egg-info")
_remove_tree(egg_info_dir)

# Remove venv-build-test
venv_dir = os.path.join("venv-build-test")
_remove_tree(venv_dir)

# Remove all __pycache__ directories
for root, dirs, files in os.walk("."):
    for d in dirs:
        if d == "__pycache__":
            pyc_dir = os.path.join(root, d)
            try:
                shutil.rmtree(pyc_dir, onexc=_rmtree_onexc)
                logger.info(f"Removed: {pyc_dir}")
            except Exception as e:
                logger.error(f"Could not remove {pyc_dir}: {e}")

# Remove all .pyc files
for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith(".pyc"):
            pyc_file = os.path.join(root, f)
            try:
                os.remove(pyc_file)
                logger.info(f"Removed: {pyc_file}")
            except Exception as e:
                logger.error(f"Could not remove {pyc_file}: {e}")
                
# Final log message
logger.info("clean_project.py completed successfully.")
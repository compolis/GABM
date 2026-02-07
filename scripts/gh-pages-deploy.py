"""
Script to build and deploy documentation to GitHub Pages.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
import os
import shutil
import subprocess
import tempfile
import uuid
import logging
from logging.handlers import RotatingFileHandler

# Logging setup
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(ROOT, 'data', 'logs', 'docs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'gh-pages-deploy.log')
logger = logging.getLogger("gh-pages-deploy")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOG_FILE, maxBytes=512*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)

# Build docs
logger.info("Building Sphinx docs...")
subprocess.run(["python3", "-m", "sphinx", "-b", "html", "docs", "docs/_build/html"], check=True)
logger.info("Docs build complete.")

# Prepare a unique temporary gh-pages directory path (do not create it yet)
gh_pages_dir = os.path.join(tempfile.gettempdir(), f"gh-pages-{uuid.uuid4().hex}")
logger.info(f"Preparing gh-pages worktree at {gh_pages_dir}")

# Git commands to deploy (assumes gh-pages branch exists and is set up)
logger.info("Adding gh-pages worktree...")
subprocess.run(["git", "worktree", "add", gh_pages_dir, "gh-pages"], check=True)

def copy_contents(src, dst):
    """
    Recursively copy contents from src to dst, creating dst if it doesn't exist.
    """
    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            logger.info(f"Copying directory: {s} -> {d}")
            copy_contents(s, d)
        else:
            logger.info(f"Copying file: {s} -> {d}")
            shutil.copy2(s, d)

# Copy built docs to gh-pages directory
src_dir = os.path.join("docs", "_build", "html")
for item in os.listdir(src_dir):
    s = os.path.join(src_dir, item)
    d = os.path.join(gh_pages_dir, item)
    if os.path.isdir(s):
        copy_contents(s, d)
    else:
        logger.info(f"Copying file: {s} -> {d}")
        shutil.copy2(s, d)

# Git commands to commit and push changes
logger.info("Adding files to git...")
subprocess.run(["git", "-C", gh_pages_dir, "add", "."], check=True)
logger.info("Committing changes...")
subprocess.run(["git", "-C", gh_pages_dir, "commit", "-m", "Update docs"], check=True)
logger.info("Pushing to origin gh-pages...")
subprocess.run(["git", "-C", gh_pages_dir, "push", "origin", "gh-pages"], check=True)
logger.info("Removing worktree...")
subprocess.run(["git", "worktree", "remove", gh_pages_dir], check=True)
logger.info("gh-pages-deploy.py completed successfully.")
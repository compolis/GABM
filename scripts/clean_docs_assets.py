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

# Files to remove from docs/
DOC_FILES = [
    "README.md",
    "ROADMAP.md",
    "CHANGE_LOG.md",
    "CODE_OF_CONDUCT.md",
    "SETUP_GUIDE.md",
    "CONTRIBUTORS.md",
    "LICENSE.md",
    "requirements.md",
    "requirements-dev.md",
]

# Paths
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

# Remove old copies of doc files from docs/
for fname in DOC_FILES:
    fpath = os.path.join(DOCS, fname)
    try:
        if os.path.exists(fpath):
            os.remove(fpath)
            print(f"Removed: {fname}")
    except Exception as e:
        print(f"Could not remove {fname}: {e}")

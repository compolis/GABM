"""
Script to clean the project by removing build artifacts and cache files.
This includes removing the Sphinx build directory (docs/_build), all __pycache__ directories, and all .pyc files. This helps ensure that the project is in a clean state before building documentation or running tests, and prevents issues caused by stale build artifacts or cache files.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import os
import shutil

# Remove docs/_build
build_dir = os.path.join("docs", "_build")
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)
    print(f"Removed: {build_dir}")

# Remove all __pycache__ directories
for root, dirs, files in os.walk("."):
    for d in dirs:
        if d == "__pycache__":
            pyc_dir = os.path.join(root, d)
            shutil.rmtree(pyc_dir)
            print(f"Removed: {pyc_dir}")

# Remove all .pyc files
for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith(".pyc"):
            pyc_file = os.path.join(root, f)
            os.remove(pyc_file)
            print(f"Removed: {pyc_file}")

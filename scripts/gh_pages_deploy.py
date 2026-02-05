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

# Build docs
subprocess.run(["python3", "-m", "sphinx", "-b", "html", "docs", "docs/_build/html"], check=True)

# Prepare gh-pages directory
gh_pages_dir = os.path.join("/tmp", "gh-pages")
if os.path.exists(gh_pages_dir):
    shutil.rmtree(gh_pages_dir)
os.makedirs(gh_pages_dir)

# Copy built docs
src_dir = os.path.join("docs", "_build", "html")
for item in os.listdir(src_dir):
    s = os.path.join(src_dir, item)
    d = os.path.join(gh_pages_dir, item)
    if os.path.isdir(s):
        shutil.copytree(s, d)
    else:
        shutil.copy2(s, d)

# Git commands to deploy (assumes gh-pages branch exists and is set up)
subprocess.run(["git", "worktree", "add", gh_pages_dir, "gh-pages"], check=True)
subprocess.run(["git", "-C", gh_pages_dir, "add", "."], check=True)
subprocess.run(["git", "-C", gh_pages_dir, "commit", "-m", "Update docs"], check=True)
subprocess.run(["git", "-C", gh_pages_dir, "push", "origin", "gh-pages"], check=True)
subprocess.run(["git", "worktree", "remove", gh_pages_dir], check=True)

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

# Build docs
subprocess.run(["python3", "-m", "sphinx", "-b", "html", "docs", "docs/_build/html"], check=True)



# Prepare a unique temporary gh-pages directory path (do not create it yet)
gh_pages_dir = os.path.join(tempfile.gettempdir(), f"gh-pages-{uuid.uuid4().hex}")



# Git commands to deploy (assumes gh-pages branch exists and is set up)
subprocess.run(["git", "worktree", "add", gh_pages_dir, "gh-pages"], check=True)

# Copy built docs after worktree is created
src_dir = os.path.join("docs", "_build", "html")

def copy_contents(src, dst):
    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_contents(s, d)
        else:
            shutil.copy2(s, d)

for item in os.listdir(src_dir):
    s = os.path.join(src_dir, item)
    d = os.path.join(gh_pages_dir, item)
    if os.path.isdir(s):
        copy_contents(s, d)
    else:
        shutil.copy2(s, d)

subprocess.run(["git", "-C", gh_pages_dir, "add", "."], check=True)
subprocess.run(["git", "-C", gh_pages_dir, "commit", "-m", "Update docs"], check=True)
subprocess.run(["git", "-C", gh_pages_dir, "push", "origin", "gh-pages"], check=True)
subprocess.run(["git", "worktree", "remove", gh_pages_dir], check=True)

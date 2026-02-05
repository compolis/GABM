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

# List of cache directories or files to remove
CACHE_PATHS = [
    os.path.join("data", "llm"),
    os.path.join("data", "llm_cache"),
    os.path.join("data", "model_lists"),
]

# Remove cache directories/files
for path in CACHE_PATHS:
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
            print(f"Removed directory: {path}")
        else:
            os.remove(path)
            print(f"Removed file: {path}")
    else:
        print(f"Not found: {path}")

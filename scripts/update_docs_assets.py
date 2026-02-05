def clean_code_blocks(md):
    lines = md.splitlines()
    in_code = False
    cleaned = []
    for line in lines:
        if line.strip().startswith('```') or line.strip().startswith('~~~~'):
            in_code = not in_code
            cleaned.append('```')
            continue
        if in_code and line.strip() == '':
            continue
        cleaned.append(line)
    return '\n'.join(cleaned)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to copy key markdown files from the project root to the docs/ directory for inclusion in the
documentation. This ensures that important project information (like README, roadmap, etc.) is easily
accessible from the docs and can be linked to from the API documentation. The script also updates
markdown links within these files to point to the correct locations in the docs/ directory. This is
meant to be run before building the documentation to ensure all assets are up to date.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import os
import shutil
import re

# Files to copy from root to docs/
DOC_FILES = [
    "README.md",
    "ROADMAP.md",
    "CHANGE_LOG.md",
    "CODE_OF_CONDUCT.md",
    "SETUP_GUIDE.md",
    "CONTRIBUTORS.md",
    "LICENSE.md",
]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

# Map of original file names to their new relative links in docs/
LINK_MAP = {name: name for name in DOC_FILES}

# Regex to match markdown links: [text](filename)
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

# Always rewrite links to use just the filename (no ../)
def update_links(text):
    def repl(match):
        label, target = match.groups()
        # If the link is to a known doc file (even if ../ is present), convert to MyST doc cross-reference
        for docfile in LINK_MAP:
            if target.endswith(docfile):
                return f"{{doc}}`{label} <{docfile}>`"
        # If the link is to README (without .md), rewrite to MyST doc cross-reference
        if target == "README":
            return f"{{doc}}`{label} <README.md>`"
        # If the link is a local anchor, keep as is
        if target.startswith('#'):
            return match.group(0)
        return match.group(0)
    return LINK_RE.sub(repl, text)

def fix_header_levels(text):
    # Demote all headings by one level: # -> ##, ## -> ###, ### -> ####, etc.
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.match(r'^(#+) ', line):
            hashes = re.match(r'^(#+)', line).group(1)
            lines[i] = '#' + hashes + line[len(hashes):]
    return '\n'.join(lines)

def fix_toc_links(text):
    # Rewrite ToC links to plain Markdown links (not MyST cross-references)
    # Remove any MyST :ref: or {ref} syntax
    # Example: [Overview](#overview) or [Overview](:ref:`overview`) -> [Overview](#overview)
    # Also handle [Overview]({ref}`overview`) -> [Overview](#overview)
    text = re.sub(r'\[([^\]]+)\]\(:ref:`([^`]+)`\)', r'[\1](#\2)', text)
    text = re.sub(r'\[([^\]]+)\]\(\{ref}`([^`]+)`\)', r'[\1](#\2)', text)
    return text

def main():
    """
    Main function to copy files and update links.
    """
    for fname in DOC_FILES:
        src = os.path.join(ROOT, fname)
        dst = os.path.join(DOCS, fname)
        if not os.path.exists(src):
            print(f"Warning: {src} does not exist, skipping.")
            continue
        with open(src, "r", encoding="utf-8") as f:
            content = f.read()
        new_content = update_links(content)
        if fname == "README.md":
            # Remove badges block and fork maintainer note
            new_content = re.sub(r'<!-- Badges -->.*?</p>\s*> \*\*Note for Fork Maintainers:\*\*[\s\S]*?repo.\n', '', new_content, flags=re.DOTALL)
            new_content = re.sub(r'## Table of Contents[\s\S]*?(?=^## |^# |\Z)', '', new_content, flags=re.MULTILINE)
            new_content = fix_header_levels(new_content)
            new_content = fix_toc_links(new_content)
            new_content = re.sub(r'\[//\]: # \(.*\)', '', new_content)
            # Normalize code blocks to use exactly three backticks and remove extra blank lines inside code blocks
            new_content = re.sub(r'(`{3,}|~{3,})', '```', new_content)
            new_content = clean_code_blocks(new_content)
        with open(dst, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Copied and processed: {fname}")

# Helper functions moved to top level
def convert_headings(md):
    lines = md.splitlines()
    out = []
    for fname in DOC_FILES:
        src = os.path.join(ROOT, fname)
        dst = os.path.join(DOCS, fname)
        if not os.path.exists(src):
            print(f"Warning: {src} does not exist, skipping.")
            continue
        with open(src, "r", encoding="utf-8") as f:
            content = f.read()
        new_content = update_links(content)
        if fname == "README.md":
            # Remove badges block and fork maintainer note
            new_content = re.sub(r'<!-- Badges -->.*?</p>\s*> \*\*Note for Fork Maintainers:\*\*[\s\S]*?repo.\n', '', new_content, flags=re.DOTALL)
            new_content = re.sub(r'## Table of Contents[\s\S]*?(?=^## |^# |\Z)', '', new_content, flags=re.MULTILINE)
            new_content = fix_header_levels(new_content)
            new_content = fix_toc_links(new_content)
            new_content = re.sub(r'\[//\]: # \(.*\)', '', new_content)
            # Normalize code blocks to use exactly three backticks and remove extra blank lines inside code blocks
            new_content = re.sub(r'(`{3,}|~{3,})', '```', new_content)
            new_content = clean_code_blocks(new_content)
        with open(dst, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Copied and processed: {fname}")

    # Always copy CONTRIBUTORS and LICENSE as .md for Sphinx compatibility, with debug output
    special_titles = {"LICENSE.md": "# License\n\n", "CONTRIBUTORS.md": "# Contributors\n\n"}
    for fname in ["CONTRIBUTORS", "LICENSE"]:
        src = os.path.join(ROOT, fname)
        dst = os.path.join(DOCS, fname + ".md")
        print(f"[FORCE COPY] Checking for {src} to copy to {dst}...")
        if os.path.exists(src):
            with open(src, "r", encoding="utf-8") as f:
                content = f.read()
            title = special_titles.get(fname + ".md", "")
            # Remove duplicate heading if present in content
            content = re.sub(r'^# Contributors\s*', '', content, flags=re.MULTILINE)
            content = re.sub(r'^# License\s*', '', content, flags=re.MULTILINE)
            with open(dst, "w", encoding="utf-8") as f:
                f.write(title + content)
            print(f"[FORCE COPY] Copied and renamed with title: {fname} -> {fname}.md")

def force_copy_contributors_license():
    special_titles = {"LICENSE.md": "# License\n\n", "CONTRIBUTORS.md": "# Contributors\n\n"}
    for fname in ["CONTRIBUTORS", "LICENSE"]:
        src = os.path.join(ROOT, fname)
        dst = os.path.join(DOCS, fname + ".md")
        print(f"[FORCE COPY] Checking for {src} to copy to {dst}...")
        if os.path.exists(src):
            with open(src, "r", encoding="utf-8") as f:
                content = f.read()
            title = special_titles.get(fname + ".md", "")
            # Remove duplicate heading if present in content
            content = re.sub(r'^# Contributors\s*', '', content, flags=re.MULTILINE)
            content = re.sub(r'^# License\s*', '', content, flags=re.MULTILINE)
            with open(dst, "w", encoding="utf-8") as f:
                f.write(title + content)
            print(f"[FORCE COPY] Copied and renamed with title: {fname} -> {fname}.md")

if __name__ == "__main__":
    main()
    force_copy_contributors_license()

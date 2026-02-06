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
import logging
from logging.handlers import RotatingFileHandler


# Files to copy from root to docs/
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
    "requirements.txt",
    "requirements-dev.txt",
]

# Files to copy from .github/ to docs/ (if present)
GITHUB_DOC_FILES = [
    "SECURITY.md",
    "CONTACT.md",
]


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

# Logging setup
LOG_DIR = os.path.join(ROOT, 'data', 'logs', 'docs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'update_docs_assets.log')
logger = logging.getLogger("update_docs_assets")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOG_FILE, maxBytes=512*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)

# Map of original file names to their new relative links in docs/
LINK_MAP = {name: name for name in DOC_FILES}

# Regex to match markdown links: [text](filename)
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

# Always rewrite links to use just the filename (no ../)
def update_links(text):
    """
    Rewrite Markdown links to use MyST cross-references for known doc files.
    Args:
        text (str): Markdown content.
    Returns:
        str: Markdown with updated links.
    """
    def repl(match):
        label, target = match.groups()
        # Special case: README.md should always link to the GitHub README in Sphinx
        if target == "README.md":
            logger.debug(f"Rewriting link to README.md as GitHub README")
            return f"[{label}](https://github.com/compolis/GABM#readme)"
        # For files that are copied to docs/ as .md (including those that originally have no .md extension), always link as .md
        for docfile in LINK_MAP:
            if target == docfile or target == docfile.replace('.md', ''):
                logger.debug(f"Rewriting link to {target} as plain Markdown link to {docfile}")
                return f"[{label}]({docfile})"
        # If the link is to README (without .md), rewrite to GitHub README
        if target == "README":
            logger.debug(f"Rewriting link to README as GitHub README")
            return f"[{label}](https://github.com/compolis/GABM#readme)"
        # If the link is a local anchor, keep as is
        if target.startswith('#'):
            return match.group(0)
        return match.group(0)
    return LINK_RE.sub(repl, text)

def clean_code_blocks(md):
    """
    Normalize code blocks to use triple backticks and remove extra blank lines inside code blocks.
    Args:
        md (str): Markdown content.
    Returns:
        str: Cleaned Markdown content.
    """
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

def fix_header_levels(text):
    """
    Demote all Markdown headings by one level (e.g., # to ##) for Sphinx/MyST compatibility.
    Args:
        text (str): Markdown content.
    Returns:
        str: Markdown with demoted headings.
    """
    # Demote all headings by one level: # -> ##, ## -> ###, etc.
    lines = text.splitlines()
    demoted = []
    for line in lines:
        m = re.match(r'^(#+)(\s*)(.*)', line)
        if m:
            hashes, spaces, rest = m.groups()
            new_line = '#' + hashes + spaces + rest
            demoted.append(new_line)
        else:
            demoted.append(line)
    # Debug: log first few lines to verify
    if demoted:
        logger.debug(f'First lines after heading demotion: {demoted[:3]}')
    return '\n'.join(demoted)

def fix_definition_lists_and_blockquotes(content):
    """
    Insert blank lines after definition lists and block quotes for MyST compatibility.
    Args:
        content (str): Markdown content.
    Returns:
        str: Markdown with improved spacing.
    """
    # Insert blank lines after definition lists and block quotes for MyST
    lines = content.splitlines()
    new_lines = []
    for i, line in enumerate(lines):
        new_lines.append(line)
        # Definition list: term followed by colon (not code block)
        if (line.strip().endswith('::') or (':' in line and not line.strip().startswith('#'))) and not line.strip().startswith('```'):
            # If next line is not blank, insert blank line
            if i + 1 < len(lines) and lines[i + 1].strip() != '':
                new_lines.append('')
        # Block quote: line starts with '>'
        if line.strip().startswith('>'):
            if i + 1 < len(lines) and lines[i + 1].strip() != '':
                new_lines.append('')
    return '\n'.join(new_lines)

def fix_toc_links(text):
    """
    Rewrite ToC links to plain Markdown links, removing MyST :ref: or {ref} syntax.
    Args:
        text (str): Markdown content.
    Returns:
        str: Markdown with fixed ToC links.
    """
    # Rewrite ToC links to plain Markdown links (not MyST cross-references)
    # Remove any MyST :ref: or {ref} syntax
    # Example: [Overview](#overview) or [Overview](:ref:`overview`) -> [Overview](#overview)
    # Also handle [Overview]({ref}`overview`) -> [Overview](#overview)
    text = re.sub(r'\[([^\]]+)\]\(:ref:`([^`]+)`\)', r'[\1](#\2)', text)
    text = re.sub(r'\[([^\]]+)\]\(\{ref}`([^`]+)`\)', r'[\1](#\2)', text)
    return text

def force_copy_contributors_license():
    """
    Force copy CONTRIBUTORS and LICENSE files to docs/ with .md extension and appropriate titles, even if they already exist in docs/.
    This ensures that the latest versions of these important files are always included in the documentation, and that they have the correct formatting for Sphinx/MyST.
    """
    special_titles = {"LICENSE.md": "# License\n\n", "CONTRIBUTORS.md": "# Contributors\n\n"}
    for fname in ["CONTRIBUTORS", "LICENSE"]:
        src = os.path.join(ROOT, fname)
        dst = os.path.join(DOCS, fname + ".md")
        logger.info(f"[FORCE COPY] Checking for {src} to copy to {dst}...")
        if os.path.exists(src):
            with open(src, "r", encoding="utf-8") as f:
                content = f.read()
            title = special_titles.get(fname + ".md", "")
            # Remove duplicate heading if present in content
            content = re.sub(r'^# Contributors\s*', '', content, flags=re.MULTILINE)
            content = re.sub(r'^# License\s*', '', content, flags=re.MULTILINE)
            with open(dst, "w", encoding="utf-8") as f:
                f.write(title + content)
            logger.info(f"[FORCE COPY] Copied and renamed with title: {fname} -> {fname}.md")

def main():
    """
    Main function to copy files and update links.
    """
    logger.info("Starting update_docs_assets.py script")
    # Copy files from project root
    for fname in DOC_FILES:
        src = os.path.join(ROOT, fname)
        dst = os.path.join(DOCS, fname)
        if not os.path.exists(src):
            logger.warning(f"{src} does not exist, skipping.")
            continue
        # Special handling for requirements files: copy both .txt and .md versions
        if fname in ["requirements.txt", "requirements-dev.txt"]:
            with open(src, "r", encoding="utf-8") as f:
                content = f.read()
            # Copy the .txt file directly to docs/
            with open(dst, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"Copied: {fname} -> docs/")
            # Generate the .md version for Sphinx
            md_name = fname.replace('.txt', '.md')
            dst_md = os.path.join(DOCS, md_name)
            heading = "# Requirements" if fname == "requirements.txt" else "# Requirements (Developer)"
            note = (
                "> **Note:** This file is for documentation only.\n"
                "> Install dependencies from [requirements.txt](requirements.txt) and [requirements-dev.txt](requirements-dev.txt) in the project root.\n"
            )
            with open(dst_md, "w", encoding="utf-8") as f:
                f.write(f"{heading}\n\n{note}\n\n```")
                f.write(content)
                f.write("\n```")
            logger.info(f"Copied and formatted: {fname} -> {md_name}")
            continue
            # Copy files from .github/ to docs/ (if present)
            GITHUB = os.path.join(ROOT, ".github")
            for fname in GITHUB_DOC_FILES:
                src = os.path.join(GITHUB, fname)
                dst = os.path.join(DOCS, fname)
                if os.path.exists(src):
                    with open(src, "r", encoding="utf-8") as f:
                        content = f.read()
                    # Demote headings for Sphinx compatibility
                    from re import match
                    lines = content.splitlines()
                    if lines and match(r'^# ', lines[0]):
                        lines[0] = '#' + lines[0]
                    content = '\n'.join(lines)
                    with open(dst, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"Copied: .github/{fname} -> docs/{fname}")
        with open(src, "r", encoding="utf-8") as f:
            content = f.read()
        if fname == "README.md":
            # Stricter fixes for README.md (included in index.rst)
            new_content = update_links(content)
            # Convert {doc}`...` references to plain Markdown links
            new_content = re.sub(r'\{doc\}`([^`<>]+)(?:\s*<([^`<>]+)>)?`', lambda m: f'[{m.group(1)}]({m.group(2) if m.group(2) else m.group(1)})', new_content)
            new_content = re.sub(r'<!-- Badges -->.*?</p>\s*> \*\*Note for Fork Maintainers:\*\*[\s\S]*?repo.\n', '', new_content, flags=re.DOTALL)
            new_content = re.sub(r'## Table of Contents[\s\S]*?(?=^## |^# |\Z)', '', new_content, flags=re.MULTILINE)
            new_content = fix_toc_links(new_content)
            new_content = re.sub(r'\[//\]: # \(.*\)', '', new_content)
            new_content = re.sub(r'(`{3,}|~{3,})', '```', new_content)
            new_content = clean_code_blocks(new_content)
            new_content = re.sub(r'^[ \t\-\|\+:]{5,}$', '', new_content, flags=re.MULTILINE)
            # Insert blank lines after definition lists and block quotes
            new_content = fix_definition_lists_and_blockquotes(new_content)
            # Rewrite requirements.txt/dev.txt links to .md for Sphinx
            new_content = re.sub(r'\[requirements\.txt\]\(requirements\.txt\)', '[requirements.md](requirements.md)', new_content)
            new_content = re.sub(r'\[requirements-dev\.txt\]\(requirements-dev.txt\)', '[requirements-dev.md](requirements-dev.md)', new_content)
            # Only close unclosed backticks if the line starts with a backtick and is missing a closing one
            def close_unclosed_backticks(line):
                # Do not add a closing backtick to heading lines
                if line.lstrip().startswith('#'):
                    return line
                if line.startswith('`') and not line.rstrip().endswith('`') and line.count('`') == 1:
                    return line + '`'
                return line
            new_content = '\n'.join([close_unclosed_backticks(l) for l in new_content.splitlines()])
            # Remove logic that appends backtick after colon (fixes unwanted :` in output)
            def fix_indentation(text):
                lines = text.split('\n')
                in_code = False
                for i, line in enumerate(lines):
                    if line.strip().startswith('```'):
                        in_code = not in_code
                    elif not in_code and line.startswith('    '):
                        lines[i] = line.lstrip()
                return '\n'.join(lines)
            new_content = fix_indentation(new_content)
            # Add MyST front matter and ensure first heading is level 2
            lines = new_content.splitlines()
            # Remove any blank lines at the top
            while lines and lines[0].strip() == '':
                lines.pop(0)
            # Remove any empty headings at the top (e.g., '##' or '#')
            while lines and re.match(r'^#+\s*$', lines[0]):
                lines.pop(0)
            # Demote first heading to level 2 if it's not already
            if lines and re.match(r'^#(?!#)', lines[0]):
                lines[0] = '#' + lines[0]
            myst_front_matter = ['---', 'title: Project README', '---', '']
            new_content = '\n'.join(myst_front_matter + lines)
        elif fname == "SETUP_GUIDE.md":
            # Remove the Table of Contents section from SETUP_GUIDE.md for Sphinx
            new_content = fix_header_levels(content)
            # Remove leading blank lines before the first heading
            new_content = re.sub(r'^(\s*\n)+', '', new_content)
            # Remove only the ToC section (from '## Table of Contents' to the next heading, but not blank lines or content after)
            new_content = re.sub(r'## Table of Contents\s*\n(?:- .+\n)*', '', new_content)
            new_content = update_links(new_content)
            new_content = clean_code_blocks(new_content)
        else:
            # Demote headings first for all other non-README.md files
            new_content = fix_header_levels(content)
            # Remove leading blank lines before the first heading
            new_content = re.sub(r'^(\s*\n)+', '', new_content)
            # Then apply other transformations
            new_content = update_links(new_content)
            # Replace {doc}`README.md` references with a link to index.html
            new_content = re.sub(r'\{doc\}`README\\.md(?:\s*<README\\.md>)?`', '[Main Page](index.html)', new_content)
            new_content = clean_code_blocks(new_content)
        with open(dst, "w", encoding="utf-8") as f:
            f.write(new_content)
        logger.info(f"Copied and processed: {fname}")

if __name__ == "__main__":
    try:
        main()
        force_copy_contributors_license()
        logger.info("update_docs_assets.py completed successfully.")
    except Exception as e:
        logger.exception(f"update_docs_assets.py failed: {e}")

"""
Unit tests for scripts/docs.py Markdown transformation functions.

These tests ensure that heading demotion, code block normalization, and link rewriting work as expected,
helping to maintain Sphinx/MyST compatibility for automated documentation builds.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Third-party imports
import pytest
# Standard library imports
import sys
import os
# Local imports
from scripts.docs import fix_header_levels, clean_code_blocks, update_links

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_update_links_internal_doc():
    """
    Test that internal Markdown links are converted to MyST cross-references.
    Returns:
        None
    """
    input_md = "See [Roadmap](ROADMAP.md) and [Guide](SETUP_GUIDE.md)."
    # Should convert to MyST cross-references
    output = update_links(input_md)
    assert "[Roadmap](ROADMAP.md)" in output
    assert "[Guide](SETUP_GUIDE.md)" in output

def test_update_links_external():
    """
    Test that external links are left unchanged.
    Returns:
        None
    """
    input_md = "Visit [Python](https://python.org) for more info."
    output = update_links(input_md)
    assert "[Python](https://python.org)" in output

def test_fix_header_levels_basic():
    """
    Test that header levels are correctly demoted by one.
    Returns:
        None
    """
    input_md = """# Title\n## Subtitle\n### Section\n"""
    expected = """## Title\n### Subtitle\n#### Section\n"""
    assert fix_header_levels(input_md).strip() == expected.strip()

def test_fix_header_levels_no_space():
    """
    Test that headers without a space after the hash are still demoted.
    Returns:
        None
    """
    input_md = """#Title\n##Subtitle\n"""
    expected = """##Title\n###Subtitle\n"""
    assert fix_header_levels(input_md).strip() == expected.strip()

def test_fix_header_levels_leading_blank():
    """
    Test that leading blank lines before the first header are preserved and headers are still demoted.
    Returns:
        None
    """
    input_md = """\n\n# Heading\nText"""
    expected = """\n\n## Heading\nText"""
    assert fix_header_levels(input_md).strip() == expected.strip()

def test_clean_code_blocks_removes_extra_blank():
    """
    Test that extra blank lines within code blocks are removed.
    Returns:
        None
    """
    input_md = """```\n\ncode line\n\n```\n"""
    expected = """```\ncode line\n```\n"""
    assert clean_code_blocks(input_md).strip() == expected.strip()

def test_clean_code_blocks_normalizes_ticks():
    """
    Test that code blocks with unbalanced backticks are normalized to use triple backticks.
    Returns:
        None
    """
    input_md = """~~~~\ncode\n~~~~\n"""
    expected = """```\ncode\n```\n"""
    assert clean_code_blocks(input_md).strip() == expected.strip()

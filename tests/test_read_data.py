#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for read_data module.

@author: Andy Turner<agdturner@gmail.com>
@version: 0.1.0
@copyright: Copyright (c) 2026 GABM contributors, University of Leeds
"""
import pytest
from src.io.read_data import read_api_keys
from pathlib import Path

def test_read_api_keys(tmp_path):
    """
    Test the read_api_keys function.
    @param tmp_path: pytest fixture providing a temporary directory.
    """
    # Create a temporary CSV file
    csv_content = "api,key\nopenai,sk-test\ndeepseek,sk-test2\n"
    test_file = tmp_path / "api_key.csv"
    test_file.write_text(csv_content)

    # Call the function
    result = read_api_keys(test_file)

    # Check the result
    assert result == {"openai": "sk-test", "deepseek": "sk-test2"}

def test_read_api_keys_missing_file():
    """
    Test that FileNotFoundError is raised for a missing file.
    """
    with pytest.raises(FileNotFoundError):
        read_api_keys("nonexistent.csv")

def test_read_api_keys_empty_file(tmp_path):
    """
    Test reading from an empty CSV file (should raise StopIteration).
    @param tmp_path: pytest fixture providing a temporary directory.
    """
    test_file = tmp_path / "empty.csv"
    test_file.write_text("")
    with pytest.raises(StopIteration):
        read_api_keys(test_file)

def test_read_api_keys_header_only(tmp_path):
    """
    Test reading from a CSV file with only a header (should return empty dict).
    @param tmp_path: pytest fixture providing a temporary directory.
    """
    test_file = tmp_path / "header_only.csv"
    test_file.write_text("api,key\n")
    result = read_api_keys(test_file)
    assert result == {}

def test_read_api_keys_malformed_row(tmp_path):
    """
    Test reading from a CSV file with a malformed row (missing key column).
    @param tmp_path: pytest fixture providing a temporary directory.
    """
    csv_content = "api,key\nopenai\n"
    test_file = tmp_path / "malformed.csv"
    test_file.write_text(csv_content)
    result = read_api_keys(test_file)
    assert result == {}

def test_read_api_keys_duplicate_api(tmp_path):
    """
    Test reading from a CSV file with duplicate API names (last one wins).
    @param tmp_path: pytest fixture providing a temporary directory.
    """
    csv_content = "api,key\nopenai,sk-1\nopenai,sk-2\n"
    test_file = tmp_path / "duplicate.csv"
    test_file.write_text(csv_content)
    result = read_api_keys(test_file)
    assert result == {"openai": "sk-2"}

def test_read_api_keys_extra_columns(tmp_path):
    """
    Test reading from a CSV file with extra columns (should ignore extras).
    @param tmp_path: pytest fixture providing a temporary directory.
    """
    csv_content = "api,key,extra\nopenai,sk-test,foo\ndeepseek,sk-test2,bar\n"
    test_file = tmp_path / "extra.csv"
    test_file.write_text(csv_content)
    result = read_api_keys(test_file)
    assert result == {"openai": "sk-test", "deepseek": "sk-test2"}
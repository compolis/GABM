"""
Tests for logging utility module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

from pathlib import Path
from uuid import uuid4

from gabm.utils.logging import setup_module_logger

def test_setup_module_logger_creates_log_file(monkeypatch, tmp_path):
    """
    Test that setup_module_logger creates a log file in the specified directory.

    Args:
        monkeypatch: pytest fixture for modifying the environment.
        tmp_path: pytest fixture providing a temporary directory.
    """
    monkeypatch.chdir(tmp_path)

    logger_name = f"test_logger_{uuid4().hex}"
    log_file_name = f"{logger_name}.log"

    logger = setup_module_logger(logger_name, log_file_name)
    logger.info("hello test log")
    
    for handler in logger.handlers:
        handler.flush()
    
    log_path = Path("data/logs/llm") / log_file_name
    
    assert log_path.exists()
    assert "hello test log" in log_path.read_text(encoding="utf-8")


def test_setup_module_logger_does_not_duplicate_handlers(monkeypatch, tmp_path):
    """
    Test that setup_module_logger does not add duplicate handlers when called multiple times.

    Args:
        monkeypatch: pytest fixture for modifying the environment.
        tmp_path: pytest fixture providing a temporary directory.
    """
    monkeypatch.chdir(tmp_path)
    
    logger_name = f"test_logger_{uuid4().hex}"
    log_file_name = f"{logger_name}.log"
    
    logger = setup_module_logger(logger_name, log_file_name)
    initial_handlers = list(logger.handlers)
    
    logger_again = setup_module_logger(logger_name, log_file_name)
    
    assert logger_again is logger
    assert logger_again.handlers == initial_handlers
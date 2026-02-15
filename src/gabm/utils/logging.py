"""
Centralized logging setup utility for GABM LLM modules.
Import and call setup_module_logger(__name__, log_file_name) at the top of each module/script.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

import logging
from pathlib import Path
import sys

def setup_module_logger(module_name, log_file_name):
    """
    Set up a logger for a module, writing to data/logs/llm/log_file_name and the console.
    Returns a logger instance for use in the module.
    """
    log_dir = Path("data/logs/llm")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / log_file_name
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    # Avoid duplicate handlers if re-imported
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file, mode="a")
        file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
    return logger

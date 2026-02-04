"""
Reads data from various sources.
"""
# Metadata
__author__ = "Andy Turner <agdturner@gmail.com>"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import csv
from pathlib import Path

def read_api_keys(file_path: str | Path) -> dict[str, str]:
    """
    Reads API keys from a CSV file into a dictionary.
    Assumes the CSV has two columns: 'api' and 'key', with a header row.

    Args:
        file_path (str or Path): Path to the CSV file.

    Returns:
        dict[str, str]: Dictionary with API names as keys and their corresponding keys as values.

    Raises:
        ValueError: If file_path is not provided.
        FileNotFoundError: If the specified file does not exist.
    """
    if not file_path:
        raise ValueError("file_path must be provided")
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    api_dict = {}
    with path.open(newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip header
        for row in reader:
            if len(row) >= 2:
                api, key = row[0], row[1]
                api_dict[api] = key
    return api_dict
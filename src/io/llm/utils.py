"""
Utility functions for LLM API error handling, model listing, caching, and validation.

- Provides a decorator for safe API calls.
- Provides utilities to write model lists as both JSON and TXT for all LLMs.
- Provides a loader for model lists from JSON for validation and selection.

This supports a unified workflow for model management across all LLM providers in the project.
"""
# Metadata
__author__ = "Andy Turner <agdturner@gmail.com>"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import functools
import json
from pathlib import Path

def safe_api_call(api_name):
    """
    Decorator to handle exceptions for LLM API calls and log errors gracefully.

    Args:
        api_name (str): Name of the API for logging purposes.

    Returns:
        function: Decorator that wraps the target function, returning None on error.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"[{api_name}] Error: {e}")
                return None
        return wrapper
    return decorator

def list_models_to_txt(models, models_path, formatter, header=None):
    """
    Write a list of models to a text file with a custom formatter.

    Args:
        models (iterable): List of model objects.
        models_path (Path): Path to the output file.
        formatter (callable): Function that takes a model and returns a string.
        header (str, optional): Header string for the file.
    """
    lines = [header] if header else []
    for model in models:
        lines.append(formatter(model))
    output = "\n".join(lines)
    print(output)
    models_path.parent.mkdir(parents=True, exist_ok=True)
    with models_path.open("w", encoding="utf-8") as f:
        f.write(output)

def write_models_json_and_txt(models, models_json_path, models_txt_path, formatter, header=None):
    """
    Write a list of models to both JSON and TXT files for LLM model management.

    Args:
        models (iterable): List of model objects or dicts.
        models_json_path (Path): Path to the output JSON file.
        models_txt_path (Path): Path to the output TXT file.
        formatter (callable): Function that takes a model and returns a string for TXT output.
        header (str, optional): Header string for the TXT file.

    This enables both human-readable and machine-readable model lists for all LLMs.
    """
    # Write JSON
    models_json_path.parent.mkdir(parents=True, exist_ok=True)
    with models_json_path.open("w", encoding="utf-8") as f:
        json.dump([model if isinstance(model, dict) else model.__dict__ for model in models], f, indent=2)
    # Write TXT
    lines = [header] if header else []
    for model in models:
        lines.append(formatter(model))
    output = "\n".join(lines)
    with models_txt_path.open("w", encoding="utf-8") as f:
        f.write(output)

def load_models_from_json(models_json_path):
    """
    Load a list of models from a JSON file for validation and selection.

    Args:
        models_json_path (Path): Path to the JSON file.
    Returns:
        list: List of model dicts.
    """
    if not models_json_path.exists():
        return []
    with models_json_path.open("r", encoding="utf-8") as f:
        return json.load(f)

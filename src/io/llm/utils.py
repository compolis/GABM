"""
Utility functions for LLM API error handling and logging.
"""
# Metadata
__author__ = "Andy Turner <agdturner@gmail.com>"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import functools

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

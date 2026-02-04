"""
For sending prompts to OpenAI, receiving responses, and caching storing and retrieving them.
"""
# Metadata
__author__ = "Andy Turner <agdturner@gmail.com>"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# OpenAI client library
from openai import OpenAI
# Standard library imports
import os
import pickle
from pathlib import Path
# Shared error handling
from .utils import safe_api_call

# Persistent cache for message-response pairs
_cache_path = Path("data/llm/openai/cache.pkl")

# In memory cache
_cache = {}
# Load existing cache if available
if _cache_path.exists():
    try:
        with _cache_path.open("rb") as f:
            _cache = pickle.load(f)
    except Exception as e:
        print(f"[openai.py] Warning: Failed to load cache: {e}")
        _cache = {}

@safe_api_call("openai")
def send(api_key, message, model="gpt-3.5-turbo"):
    """
    Send a prompt to OpenAI and return the response object.

    Args:
        api_key (str): The OpenAI API key.
        message (str): The message to send to OpenAI.
        model (str, optional): The model to use (default is "gpt-3.5-turbo").

    Returns:
        openai.types.ChatCompletion: The full OpenAI response object.
    """
    if not api_key:
        raise RuntimeError("OpenAI API key must be provided.")
    cache_key = (message, model)
    if cache_key in _cache:
        return _cache[cache_key]
    os.environ["OPENAI_API_KEY"] = api_key
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": message}]
    )
    _cache[cache_key] = response
    # Save updated cache
    _cache_path.parent.mkdir(parents=True, exist_ok=True)
    with _cache_path.open("wb") as f:
        pickle.dump(_cache, f)
    return response
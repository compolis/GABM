"""
For sending prompts to Anthropic Claude, receiving responses, and caching them.
"""
__author__ = "Andy Turner <agdturner@gmail.com>"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Anthropic client library
import anthropic
# Standard library imports
import os
import pickle
from pathlib import Path
# Shared error handling
from .utils import safe_api_call

# Persistent cache for message-response pairs
_cache_path = Path("data/llm/anthropic/cache.pkl")
_cache = {}
if _cache_path.exists():
    try:
        with _cache_path.open("rb") as f:
            _cache = pickle.load(f)
    except Exception as e:
        print(f"[anthropic.py] Warning: Failed to load cache: {e}")
        _cache = {}

@safe_api_call("anthropic")
def send(api_key, message, model="claude-3-opus-20240229"):
    """
    Send a prompt to Anthropic Claude and return the response object.

    Parameters
    ----------
    api_key : str
        The Anthropic API key.
    message : str
        The message to send to Claude.
    model : str, optional
        The model to use (default is "claude-3-opus-20240229").

    Returns
    -------
    response : anthropic.types.Message
        The full Anthropic response object.
    """
    if not api_key:
        raise RuntimeError("Anthropic API key must be provided.")
    cache_key = (message, model)
    if cache_key in _cache:
        return _cache[cache_key]
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=100,
        messages=[{"role": "user", "content": message}]
    )
    _cache[cache_key] = response
    # Save updated cache
    _cache_path.parent.mkdir(parents=True, exist_ok=True)
    with _cache_path.open("wb") as f:
        pickle.dump(_cache, f)
    return response

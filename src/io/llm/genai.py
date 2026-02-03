"""
For sending prompts to Google Generative AI (genai), receiving responses, and caching them.
"""
__author__ = "Andy Turner <agdturner@gmail.com>"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Google Generative AI client library
import google.generativeai as genai
# Standard library imports
import os
import pickle
from pathlib import Path
# Shared error handling
from .utils import safe_api_call

# Persistent cache for message-response pairs
_cache_path = Path("data/llm/genai/cache.pkl")
_cache = {}
if _cache_path.exists():
    try:
        with _cache_path.open("rb") as f:
            _cache = pickle.load(f)
    except Exception as e:
        print(f"[genai.py] Warning: Failed to load cache: {e}")
        _cache = {}

@safe_api_call("genai")
def send(api_key, message, model="gemini-pro"):
    """
    Send a prompt to Google Generative AI and return the response object.

    Parameters
    ----------
    api_key : str
        The Google API key.
    message : str
        The message to send to Gemini.
    model : str, optional
        The model to use (default is "gemini-pro").

    Returns
    -------
    response : generativeai.types.GenerationResponse
        The full Gemini response object.
    """
    if not api_key:
        raise RuntimeError("Google API key must be provided.")
    cache_key = (message, model)
    if cache_key in _cache:
        return _cache[cache_key]
    genai.configure(api_key=api_key)
    model_obj = genai.GenerativeModel(model)
    response = model_obj.generate_content(message)
    _cache[cache_key] = response
    # Save updated cache
    _cache_path.parent.mkdir(parents=True, exist_ok=True)
    with _cache_path.open("wb") as f:
        pickle.dump(_cache, f)
    return response

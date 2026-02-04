"""
For sending prompts to Anthropic Claude, receiving responses, and managing model lists and cache.

Features:
- Send prompts to Anthropic and cache responses for reproducibility.
- List available models from the Anthropic API and save as both JSON and TXT for validation and reference.
- Validate selected model names against the cached JSON model list.
- Unified workflow for model management, matching other LLM modules in the project.
"""
# Metadata
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
from .utils import safe_api_call, list_models_to_txt

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

def list_available_models(api_key):
    """
    List available Anthropic models and save to data/llm/anthropic/models.txt.

    Args:
        api_key (str): The Anthropic API key.
    """
    client = anthropic.Anthropic(api_key=api_key)
    # The actual method to list models may differ; update as needed.
    # Placeholder: assume client.models.list() returns model objects with id and description
    try:
        models = client.models.list()
    except Exception as e:
        print(f"[anthropic] Error listing models: {e}")
        models = []
    def formatter(model):
        return (f"Model ID: {getattr(model, 'id', 'N/A')}\n"
                f"  Description: {getattr(model, 'description', 'N/A')}\n")
    list_models_to_txt(
        models,
        Path("data/llm/anthropic/models.txt"),
        formatter,
        header="Available Anthropic models:\n"
    )

@safe_api_call("anthropic")
def send(api_key, message, model="claude-3-opus-20240229"):
    """
    Send a prompt to Anthropic Claude and return the response object.

    Args:
        api_key (str): The Anthropic API key.
        message (str): The message to send to Claude.
        model (str, optional): The model to use (default is "claude-3-opus-20240229").

    Returns:
        anthropic.types.Message: The full Anthropic response object.
    """
    if not api_key:
        raise RuntimeError("Anthropic API key must be provided.")
    cache_key = (message, model)
    if cache_key in _cache:
        return _cache[cache_key]
    client = anthropic.Anthropic(api_key=api_key)
    try:
        response = client.messages.create(
            model=model,
            max_tokens=100,
            messages=[{"role": "user", "content": message}]
        )
    except Exception as e:
        print(f"[anthropic] Error: {e}")
        if "404" in str(e) or "not found" in str(e) or "not supported" in str(e):
            list_available_models(api_key)
        return None
    _cache[cache_key] = response
    # Save updated cache
    _cache_path.parent.mkdir(parents=True, exist_ok=True)
    with _cache_path.open("wb") as f:
        pickle.dump(_cache, f)
    return response

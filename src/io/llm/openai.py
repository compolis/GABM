"""
For sending prompts to OpenAI, receiving responses, and managing model lists and cache.

Features:
- Send prompts to OpenAI and cache responses for reproducibility.
- List available models from the OpenAI API and save as both JSON and TXT for validation and reference.
- Validate selected model names against the cached JSON model list.
- Unified workflow for model management, matching other LLM modules in the project.
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
from .utils import safe_api_call, list_models_to_txt, write_models_json_and_txt

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
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}]
        )
    except Exception as e:
        print(f"[openai] Error: {e}")
        if "404" in str(e) or "not found" in str(e) or "not supported" in str(e):
            list_available_models(api_key)
        return None
    _cache[cache_key] = response
    # Save updated cache
    _cache_path.parent.mkdir(parents=True, exist_ok=True)
    with _cache_path.open("wb") as f:
        pickle.dump(_cache, f)
    return response

def list_available_models(api_key):
    """
    List available OpenAI models and save to data/llm/openai/models.json and models.txt.

    Args:
        api_key (str): The OpenAI API key.
    """
    os.environ["OPENAI_API_KEY"] = api_key
    client = OpenAI()
    models = client.models.list()
    def formatter(model):
        return (f"Model ID: {model.id}\n"
                f"  Owned by: {getattr(model, 'owned_by', 'N/A')}\n"
                f"  Created: {getattr(model, 'created', 'N/A')}\n")
    write_models_json_and_txt(
        models,
        Path("data/llm/openai/models.json"),
        Path("data/llm/openai/models.txt"),
        formatter,
        header="Available OpenAI models:\n"
    )

if __name__ == "__main__":
    import sys
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Set the OPENAI_API_KEY environment variable.")
        sys.exit(1)
    list_available_models(api_key)
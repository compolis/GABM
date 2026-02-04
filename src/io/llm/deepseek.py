"""
For sending prompts to DeepSeek, receiving responses, and managing model lists and cache.

Features:
- Send prompts to DeepSeek and cache responses for reproducibility.
- List available models from the DeepSeek API and save as both JSON and TXT for validation and reference.
- Validate selected model names against the cached JSON model list.
- Unified workflow for model management, matching other LLM modules in the project.
"""
# Metadata
__author__ = "Andy Turner <agdturner@gmail.com>"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Placeholder for DeepSeek client import
try:
    import deepseek
except ImportError:
    deepseek = None

import os
from pathlib import Path

from .utils import safe_api_call
import pickle

_cache_path = Path("data/llm/deepseek/cache.pkl")
_cache = {}
if _cache_path.exists():
    try:
        with _cache_path.open("rb") as f:
            _cache = pickle.load(f)
    except Exception as e:
        print(f"[deepseek.py] Warning: Failed to load cache: {e}")
        _cache = {}

@safe_api_call("deepseek")
def send(api_key, message, model="deepseek-model-1"):
    """
    Send a prompt to DeepSeek and return the response object.

    Args:
        api_key (str): The DeepSeek API key.
        message (str): The message to send to DeepSeek.
        model (str, optional): The model to use (default is "deepseek-model-1").

    Returns:
        object: The DeepSeek response object.
    """
    if not api_key:
        raise RuntimeError("DeepSeek API key must be provided.")
    cache_key = (message, model)
    if cache_key in _cache:
        return _cache[cache_key]
    if deepseek is None:
        print("[deepseek] Python client not installed. Cannot send request.")
        return None
    # TODO: Replace with actual DeepSeek client usage
    # Example:
    # client = deepseek.Client(api_key=api_key)
    # response = client.chat.completions.create(model=model, messages=[{"role": "user", "content": message}])
    # For now, just a placeholder response:
    response = {"model": model, "message": message, "result": "[Placeholder DeepSeek response]"}
    _cache[cache_key] = response
    # Save updated cache
    _cache_path.parent.mkdir(parents=True, exist_ok=True)
    with _cache_path.open("wb") as f:
        pickle.dump(_cache, f)
    return response

def list_available_models(api_key):
    """
    List available DeepSeek models and save to data/llm/deepseek/models.json and models.txt.

    Args:
        api_key (str): The DeepSeek API key.
    """
    if deepseek is None:
        print("[deepseek] Python client not installed. Cannot list models.")
        return
    # TODO: Replace with actual DeepSeek client usage
    # client = deepseek.Client(api_key=api_key)
    # models = client.list_models()
    # For now, just a placeholder:
    models = [
        {"id": "deepseek-model-1", "description": "Example model 1"},
        {"id": "deepseek-model-2", "description": "Example model 2"},
    ]
    from .utils import write_models_json_and_txt
    def formatter(model):
        return (f"Model ID: {model['id']}\n"
                f"  Description: {model.get('description', 'N/A')}\n")
    write_models_json_and_txt(
        models,
        Path("data/llm/deepseek/models.json"),
        Path("data/llm/deepseek/models.txt"),
        formatter,
        header="Available DeepSeek models:\n"
    )

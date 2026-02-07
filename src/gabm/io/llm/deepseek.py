"""
For sending prompts to DeepSeek, receiving responses, and managing model lists and cache.

Features:
- Send prompts to DeepSeek and cache responses for reproducibility.
- List available models from the DeepSeek API and save as both JSON and TXT for validation and reference.
- Validate selected model names against the cached JSON model list.
- Unified workflow for model management, matching other LLM modules in the project.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# DeepSeek client library
import deepseek
# Standard library imports
import os
from pathlib import Path
# Persistent cache for message-response pairs
import pickle
# Shared error handling
from .utils import safe_api_call
# Centralized logging
from .logging_utils import setup_module_logger
logger = setup_module_logger(__name__, "deepseek.log")

_cache_path = Path("data/llm/deepseek/cache.pkl")
_cache = {}
if _cache_path.exists():
    try:
        with _cache_path.open("rb") as f:
            _cache = pickle.load(f)
    except Exception as e:
        logger.warning(f"Failed to load cache: {e}")
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
        logger.error("DeepSeek API key must be provided.")
        raise RuntimeError("DeepSeek API key must be provided.")
    cache_key = (message, model)
    if cache_key in _cache:
        logger.info(f"Cache hit for model={model}, message={message}")
        return _cache[cache_key]
    if deepseek is None:
        logger.error("[deepseek] Python client not installed. Cannot send request.")
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
    try:
        with _cache_path.open("wb") as f:
            pickle.dump(_cache, f)
        logger.info(f"Cache updated for model={model}, message={message}")
    except Exception as e:
        logger.error(f"Failed to write cache: {e}")
    return response

def list_available_models(api_key):
    """
    List available DeepSeek models and save to data/llm/deepseek/models.json and models.txt.

    Args:
        api_key (str): The DeepSeek API key.
    """
    if deepseek is None:
        logger.error("[deepseek] Python client not installed. Cannot list models.")
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
    logger.info("Writing DeepSeek model list to JSON and TXT.")
    write_models_json_and_txt(
        models,
        Path("data/llm/deepseek/models.json"),
        Path("data/llm/deepseek/models.txt"),
        formatter,
        header="Available DeepSeek models:\n"
    )

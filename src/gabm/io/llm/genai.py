"""
For sending prompts to Google Generative AI (genai), receiving responses, and managing model lists and cache.

Features:
- Send prompts to GenAI and cache responses for reproducibility.
- List available models from the GenAI API and save as both JSON and TXT for validation and reference.
- Validate selected model names against the cached JSON model list.
- Unified workflow for model management, matching other LLM modules in the project.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Google Generative AI client library
import google.generativeai as genai
# Standard library imports
import os
# Persistent cache for message-response pairs
import pickle
from pathlib import Path
# Shared error handling
from .utils import safe_api_call, list_models_to_txt, write_models_json_and_txt

# Centralized logging
from .logging_utils import setup_module_logger
logger = setup_module_logger(__name__, "genai.log")

# Persistent cache for message-response pairs
_cache_path = Path("data/llm/genai/cache.pkl")
_cache = {}
if _cache_path.exists():
    try:
        with _cache_path.open("rb") as f:
            _cache = pickle.load(f)
    except Exception as e:
        logger.warning(f"Failed to load cache: {e}")
        _cache = {}

@safe_api_call("genai")
def send(api_key, message, model="models/gemini-2.5-pro"):
    """
    Send a prompt to Google Generative AI and return the response as a dict.

    Args:
        api_key (str): The Google API key.
        message (str): The message to send to Gemini.
        model (str, optional): The model to use (default is "models/gemini-2.5-pro").

    Returns:
        dict: The full Gemini response as a serializable dictionary.
    """
    if not api_key:
        logger.error("Google API key must be provided.")
        raise RuntimeError("Google API key must be provided.")
    cache_key = (message, model)
    if cache_key in _cache:
        logger.info(f"Cache hit for model={model}, message={message}")
        return _cache[cache_key]
    genai.configure(api_key=api_key)
    try:
        model_obj = genai.GenerativeModel(model)
        response = model_obj.generate_content(message)
        # Convert to dict if possible
        if hasattr(response, 'to_dict'):
            response_dict = response.to_dict()
        elif hasattr(response, '__dict__'):
            response_dict = dict(response.__dict__)
        else:
            # Fallback: try to serialize as-is
            response_dict = response
    except Exception as e:
        logger.error(f"[genai] Error: {e}")
        if "404" in str(e) or "not found" in str(e) or "not supported" in str(e):
            list_available_models(api_key)
        return None
    _cache[cache_key] = response_dict
    # Save updated cache
    _cache_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with _cache_path.open("wb") as f:
            pickle.dump(_cache, f)
        logger.info(f"Cache updated for model={model}, message={message}")
    except Exception as e:
        logger.error(f"Failed to write cache: {e}")
    return response_dict

def list_available_models(api_key):
    """
    List available Google Generative AI models and their supported methods.
    Also saves the list to data/llm/genai/models.json and models.txt.

    Args:
        api_key (str): The Google API key.
    """
    genai.configure(api_key=api_key)
    models = list(genai.list_models())
    def formatter(model):
        if isinstance(model, dict):
            name = model.get('name', 'N/A')
            desc = model.get('description', 'N/A')
            methods = model.get('supported_generation_methods', 'N/A')
        else:
            name = getattr(model, 'name', 'N/A')
            desc = getattr(model, 'description', 'N/A')
            methods = getattr(model, 'supported_generation_methods', 'N/A')
        return (f"Model ID: {name}\n"
                f"  Description: {desc}\n"
                f"  Supported methods: {methods}\n")
    logger.info("Writing GenAI model list to JSON and TXT.")
    write_models_json_and_txt(
        models,
        Path("data/llm/genai/models.json"),
        Path("data/llm/genai/models.txt"),
        formatter,
        header="Available GenAI models and supported methods:\n"
    )

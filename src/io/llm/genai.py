"""
For sending prompts to Google Generative AI (genai), receiving responses, and managing model lists and cache.

Features:
- Send prompts to GenAI and cache responses for reproducibility.
- List available models from the GenAI API and save as both JSON and TXT for validation and reference.
- Validate selected model names against the cached JSON model list.
- Unified workflow for model management, matching other LLM modules in the project.
"""
# Metadata
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
from .utils import safe_api_call, list_models_to_txt, write_models_json_and_txt

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

    Args:
        api_key (str): The Google API key.
        message (str): The message to send to Gemini.
        model (str, optional): The model to use (default is "gemini-pro").

    Returns:
        generativeai.types.GenerationResponse: The full Gemini response object.
    """
    if not api_key:
        raise RuntimeError("Google API key must be provided.")
    cache_key = (message, model)
    if cache_key in _cache:
        return _cache[cache_key]
    genai.configure(api_key=api_key)
    try:
        model_obj = genai.GenerativeModel(model)
        response = model_obj.generate_content(message)
    except Exception as e:
        print(f"[genai] Error: {e}")
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
    List available Google Generative AI models and their supported methods.
    Also saves the list to data/llm/genai/models.json and models.txt.

    Args:
        api_key (str): The Google API key.
    """
    genai.configure(api_key=api_key)
    models = genai.list_models()
    def formatter(model):
        return (f"Model ID: {model.name}\n"
                f"  Description: {getattr(model, 'description', 'N/A')}\n"
                f"  Supported methods: {getattr(model, 'supported_generation_methods', 'N/A')}\n")
    write_models_json_and_txt(
        models,
        Path("data/llm/genai/models.json"),
        Path("data/llm/genai/models.txt"),
        formatter,
        header="Available GenAI models and supported methods:\n"
    )

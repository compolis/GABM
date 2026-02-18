"""
For testing LLM integrations, generates model lists, and caches responses, similar to setup-llms.py.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
import os
import sys
import logging
from pathlib import Path
# Third-party imports
import pytest
# Local imports
from gabm.io.read_data import read_api_keys

# Enable/disable LLMs to test
ENABLED_LLMS = {
    "openai": True,
    "genai": True,
    "deepseek": True,
    "publicai": True,
}

# Map LLM names to their service class names
SERVICE_CLASSES = {
    "openai": "OpenAIService",
    "genai": "GenAIService",
    "deepseek": "DeepSeekService",
    "publicai": "PublicAIService",
}

# Default prompts and models for each LLM (remote/API only)
DEFAULT_PROMPTS = {
    "openai": ("gpt-3.5-turbo", "Hello OpenAI!"),
    "genai": ("models/gemini-2.5-pro", "Hello GenAI!"),
    "deepseek": ("deepseek-chat", "Hello DeepSeek!"),
    "publicai": ("swiss-ai/apertus-70b-instruct", "Give me a brief explanation of gravity in simple terms."),
}

def model_list_files_exist(llm_name):
    """
    Check if both the JSON and TXT model list files exist for the given LLM.
    Args:
        llm_name (str): Name of the LLM (e.g., "openai
    Returns:
        bool: True if both files exist, False otherwise.
    """
    base_dir = Path(f"data/llm/{llm_name}")
    json_file = base_dir / "models.json"
    txt_file = base_dir / "models.txt"
    return json_file.exists() and txt_file.exists()

@pytest.mark.parametrize("llm", ["openai", "genai", "deepseek", "publicai"])
def test_llm_model_list(llm):
    api_keys = read_api_keys('data/api_key.csv')
    api_key = api_keys.get(llm)
    if not api_key or api_key.startswith("YOUR_"):
        pytest.skip(f"API key for {llm} not set.")
    module = f"gabm.io.llm.{llm}"
    service_class = SERVICE_CLASSES[llm]
    mod = __import__(module, fromlist=[service_class])
    Service = getattr(mod, service_class)
    service = Service()
    models = service.list_available_models(api_key)
    assert models is not None

@pytest.mark.parametrize("llm", ["openai", "genai", "deepseek", "publicai"])
def test_llm_communication(llm):
    api_keys = read_api_keys('data/api_key.csv')
    api_key = api_keys.get(llm)
    if not api_key or api_key.startswith("YOUR_"):
        pytest.skip(f"API key for {llm} not set.")
    module = f"gabm.io.llm.{llm}"
    service_class = SERVICE_CLASSES[llm]
    model, prompt = DEFAULT_PROMPTS[llm]
    mod = __import__(module, fromlist=[service_class])
    Service = getattr(mod, service_class)
    service = Service()
    resp = service.send(api_key, prompt, model=model)
    assert resp is not None and len(str(resp)) > 0

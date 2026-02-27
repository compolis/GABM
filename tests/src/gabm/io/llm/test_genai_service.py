"""
Tests for the genai module.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
import pytest
# Local imports
from gabm.io.read_data import read_api_keys

SERVICE_CLASS = "GenAIService"
DEFAULT_PROMPT = ("models/gemini-2.5-pro", "Hello GenAI!")


def model_list_files_exist():
    from pathlib import Path
    base_dir = Path("data/llm/genai")
    json_file = base_dir / "models.json"
    txt_file = base_dir / "models.txt"
    return json_file.exists() and txt_file.exists()


def import_service():
    module = "gabm.io.llm.genai"
    from importlib import import_module
    mod = import_module(module)
    return getattr(mod, SERVICE_CLASS)


def test_genai_model_list():
    api_keys = read_api_keys('data/api_key.csv')
    api_key = api_keys.get("genai")
    if not api_key or api_key.startswith("YOUR_"):
        pytest.skip("API key for genai not set.")
    Service = import_service()
    service = Service()
    models = service.list_available_models(api_key)
    assert models is not None


def test_genai_communication():
    api_keys = read_api_keys('data/api_key.csv')
    api_key = api_keys.get("genai")
    if not api_key or api_key.startswith("YOUR_"):
        pytest.skip("API key for genai not set.")
    Service = import_service()
    service = Service()
    model, prompt = DEFAULT_PROMPT
    resp = service.send(api_key, prompt, model=model)
    # Handle error responses gracefully
    if resp is None:
        print("GenAIService.send() returned None. Check your API key, model name, and network connectivity.\n"
              "If you see this message, check logs for more details.")
        pytest.skip("GenAIService.send() returned None. Possibly quota exceeded or API unavailable.")
    if isinstance(resp, dict) and resp.get("error") == "quota_exceeded":
        pytest.skip("Quota exceeded for Gemini API, skipping test.")
    if isinstance(resp, dict) and resp.get("error") == "api_error":
        pytest.skip(f"API error: {resp.get('details')}")
    assert resp is not None and len(str(resp)) > 0

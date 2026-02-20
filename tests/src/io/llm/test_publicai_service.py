import pytest
from gabm.io.read_data import read_api_keys

SERVICE_CLASS = "PublicAIService"
DEFAULT_PROMPT = ("swiss-ai/apertus-70b-instruct", "Give me a brief explanation of gravity in simple terms.")


def model_list_files_exist():
    from pathlib import Path
    base_dir = Path("data/llm/publicai")
    json_file = base_dir / "models.json"
    txt_file = base_dir / "models.txt"
    return json_file.exists() and txt_file.exists()


def import_service():
    module = "gabm.io.llm.publicai"
    from importlib import import_module
    mod = import_module(module)
    return getattr(mod, SERVICE_CLASS)


def test_publicai_model_list():
    api_keys = read_api_keys('data/api_key.csv')
    api_key = api_keys.get("publicai")
    if not api_key or api_key.startswith("YOUR_"):
        pytest.skip("API key for publicai not set.")
    Service = import_service()
    service = Service()
    models = service.list_available_models(api_key)
    assert models is not None


def test_publicai_communication():
    api_keys = read_api_keys('data/api_key.csv')
    api_key = api_keys.get("publicai")
    if not api_key or api_key.startswith("YOUR_"):
        pytest.skip("API key for publicai not set.")
    Service = import_service()
    service = Service()
    model, prompt = DEFAULT_PROMPT
    resp = service.send(api_key, prompt, model=model)
    assert resp is not None and len(str(resp)) > 0

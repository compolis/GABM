"""
Unit tests for OpenAI-compatible endpoint configuration in OpenAIService.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


from types import SimpleNamespace

from gabm.io.llm import openai as openai_module
from gabm.io.llm.openai import OpenAIService


def test_openai_base_url_resolution_from_env(monkeypatch):
    monkeypatch.setenv("OPENAI_BASE_URL", "  http://127.0.0.1:11434/v1  ")
    assert OpenAIService._resolve_base_url() == "http://127.0.0.1:11434/v1"

    monkeypatch.setenv("OPENAI_BASE_URL", "   ")
    assert OpenAIService._resolve_base_url() is None

    monkeypatch.delenv("OPENAI_BASE_URL", raising=False)
    assert OpenAIService._resolve_base_url() is None


def test_openai_make_client_uses_base_url_when_set(monkeypatch):
    captured = {}

    class FakeOpenAI:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    monkeypatch.setattr(openai_module, "OpenAI", FakeOpenAI)

    OpenAIService._make_client(api_key="token", base_url="http://localhost:11434/v1")

    assert captured["api_key"] == "token"
    assert captured["base_url"] == "http://localhost:11434/v1"


def test_openai_list_models_uses_configured_base_url(monkeypatch):
    captured = {}

    class FakeOpenAI:
        def __init__(self, **kwargs):
            captured.update(kwargs)
            self.models = SimpleNamespace(
                list=lambda: [SimpleNamespace(id="qwen3:8b", owned_by="local", created=0)]
            )

    monkeypatch.setenv("OPENAI_BASE_URL", "http://127.0.0.1:11434/v1")
    monkeypatch.setattr(openai_module, "OpenAI", FakeOpenAI)
    monkeypatch.setattr(openai_module, "write_models_json_and_txt", lambda *args, **kwargs: None)

    service = OpenAIService()
    monkeypatch.setattr(service, "_call_with_error_handling", lambda fn, *args, **kwargs: fn())

    models = service.list_available_models(api_key="ollama")

    assert len(models) == 1
    assert models[0].id == "qwen3:8b"
    assert captured["api_key"] == "ollama"
    assert captured["base_url"] == "http://127.0.0.1:11434/v1"

"""
Tests for LLMService base class.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import pickle
from pathlib import Path

# Local imports
from gabm.io.llm.llm_service import LLMService


class _StubLogger:
    def __init__(self):
        self.messages = []

    def error(self, msg, *args):
        self.messages.append(("error", msg % args if args else msg))


class _DummyService(LLMService):
    SERVICE_NAME = "dummy"

    def send(self, api_key, message, model=None):
        return {"api_key": api_key, "message": message, "model": model}

    def list_available_models(self, api_key):
        return ["m1", "m2"]


class _MissingNameService(LLMService):
    def send(self, api_key, message, model=None):
        return None

    def list_available_models(self, api_key):
        return []


def test_llm_service_requires_service_name():
    """
    Test that LLMService raises ValueError if SERVICE_NAME is not set.
    """
    try:
        _MissingNameService()
        assert False, "Expected ValueError"
    except ValueError as e:
        assert "SERVICE_NAME must be set" in str(e)


def test_llm_service_initializes_paths_and_cache(monkeypatch, tmp_path):
    """
    Test that LLMService initializes cache and paths correctly.
    
    Args:
        monkeypatch: pytest fixture for modifying the environment.
        tmp_path: pytest fixture providing a temporary directory.
    """
    monkeypatch.chdir(tmp_path)

    cache_file = tmp_path / "data/llm/dummy/prompt_response_cache.pkl"
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    with cache_file.open("wb") as f:
        pickle.dump({("hello", "m1"): "cached"}, f)

    service = _DummyService()

    assert service.cache_path == cache_file.relative_to(tmp_path)
    assert service.jsonl_path == Path("data/llm/dummy/prompt_response_cache.jsonl")
    assert service.cache == {("hello", "m1"): "cached"}
    assert service.API_KEY_ENV_VAR == "DUMMY_API_KEY"


def test_call_with_error_handling_success_quota_and_generic_error():
    """
    Test that _call_with_error_handling handles success, quota exceeded, and generic errors correctly.
    """
    service = _DummyService(logger=_StubLogger())

    ok = service._call_with_error_handling(lambda x: x + 1, 2)
    assert ok == 3

    quota = service._call_with_error_handling(
        lambda: (_ for _ in ()).throw(RuntimeError("429 RESOURCE_EXHAUSTED"))
    )
    assert quota["error"] == "quota_exceeded"
    assert "429" in quota["details"]

    generic = service._call_with_error_handling(
        lambda: (_ for _ in ()).throw(RuntimeError("some other api error"))
    )
    assert generic["error"] == "api_error"
    assert "some other api error" in generic["details"]

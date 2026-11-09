"""
Tests for llm utility helpers.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import json
import os
import pickle
from pathlib import Path

import pytest

# Local imports
from gabm.io.llm.utils import (
    safe_api_call,
    list_models_to_txt,
    write_models_json_and_txt,
    load_models_from_json,
    load_llm_cache,
    cache_and_log,
    get_llm_cache_paths,
    pre_send_check_and_cache,
    call_and_cache_response,
)


class _ModelObj:
    def __init__(self, name, version):
        self.name = name
        self.version = version


class _StubLogger:
    def __init__(self):
        self.messages = []

    def debug(self, msg, *args):
        self.messages.append(("debug", msg % args if args else msg))

    def info(self, msg, *args):
        self.messages.append(("info", msg % args if args else msg))

    def warning(self, msg, *args):
        self.messages.append(("warning", msg % args if args else msg))

    def error(self, msg, *args):
        self.messages.append(("error", msg % args if args else msg))


def test_safe_api_call_returns_value_on_success():
    """
    Test that safe_api_call returns the correct value when the function succeeds.
    """
    @safe_api_call("test-api")
    def _ok(x):
        return x + 1

    assert _ok(2) == 3


def test_safe_api_call_returns_none_on_exception():
    """
    Test that safe_api_call returns None when the function raises an exception.
    """
    @safe_api_call("test-api")
    def _boom():
        raise ValueError("boom")

    assert _boom() is None


def test_list_models_to_txt_writes_formatted_content(tmp_path):
    """
    Test that list_models_to_txt writes the expected formatted content to a text file.
    
    Args:
        tmp_path: Temporary directory provided by pytest for file output.
    """
    models_path = tmp_path / "models.txt"
    list_models_to_txt(
        models=[{"name": "m1"}, {"name": "m2"}],
        models_path=models_path,
        formatter=lambda m: m["name"],
        header="header",
    )

    assert models_path.exists()
    assert models_path.read_text(encoding="utf-8") == "header\nm1\nm2"


def test_write_models_json_and_txt_handles_dict_string_and_object(tmp_path):
    models_json = tmp_path / "models.json"
    models_txt = tmp_path / "models.txt"

    models = [
        {"name": "dict-model"},
        "string-model",
        _ModelObj("obj-model", 1),
    ]

    write_models_json_and_txt(
        models=models,
        models_json_path=models_json,
        models_txt_path=models_txt,
        formatter=lambda m: (
            m
            if isinstance(m, str)
            else m["name"] if isinstance(m, dict) else m.name
        ),
        header="models",
    )

    data = json.loads(models_json.read_text(encoding="utf-8"))
    assert data[0] == {"name": "dict-model"}
    assert data[1] == "string-model"
    assert data[2] == {"name": "obj-model", "version": 1}
    assert models_txt.read_text(encoding="utf-8") == "models\ndict-model\nstring-model\nobj-model"


def test_load_models_from_json_missing_and_invalid(tmp_path):
    missing = tmp_path / "missing.json"
    assert load_models_from_json(missing) == []

    invalid = tmp_path / "invalid.json"
    invalid.write_text("not-json", encoding="utf-8")
    assert load_models_from_json(invalid) == []


def test_load_llm_cache_handles_missing_non_dict_and_invalid_pickle(tmp_path):
    logger = _StubLogger()

    missing = tmp_path / "cache_missing.pkl"
    assert load_llm_cache(missing, logger) == {}

    not_dict = tmp_path / "cache_not_dict.pkl"
    with not_dict.open("wb") as f:
        pickle.dump([1, 2, 3], f)
    assert load_llm_cache(not_dict, logger) == {}

    bad_pickle = tmp_path / "bad.pkl"
    bad_pickle.write_bytes(b"not-a-pickle")
    assert load_llm_cache(bad_pickle, logger) == {}


def test_cache_and_log_writes_cache_and_jsonl(tmp_path):
    """
    Test that cache_and_log correctly updates the cache and writes to both pickle and JSONL files.
    
    Args:
        tmp_path: Temporary directory provided by pytest for file output.
    """
    cache = {}
    cache_path = tmp_path / "prompt_response_cache.pkl"
    jsonl_path = tmp_path / "prompt_response_cache.jsonl"

    cache_and_log(
        cache=cache,
        cache_key=("prompt", "model-a"),
        response={"answer": 42},
        cache_path=cache_path,
        jsonl_path=jsonl_path,
        prompt="prompt",
        model="model-a",
        extra={"service": "test"},
        logger=_StubLogger(),
        extract_text_from_response=lambda r: f"resp:{r['answer']}",
    )

    assert cache[("prompt", "model-a")] == {"answer": 42}
    with cache_path.open("rb") as f:
        loaded = pickle.load(f)
    assert loaded[("prompt", "model-a")] == {"answer": 42}

    lines = jsonl_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    row = json.loads(lines[0])
    assert row["model"] == "model-a"
    assert row["prompt"] == "prompt"
    assert row["response"] == "resp:42"
    assert row["service"] == "test"


def test_get_llm_cache_paths():
    """
    Test that get_llm_cache_paths returns the correct paths for cache and JSONL files.
    """
    cache_path, jsonl_path = get_llm_cache_paths("openai")

    assert cache_path == Path("data/llm/openai/prompt_response_cache.pkl")
    assert jsonl_path == Path("data/llm/openai/prompt_response_cache.jsonl")


def test_pre_send_check_and_cache_behaviors(monkeypatch):
    """
    Test that pre_send_check_and_cache behaves correctly in different scenarios.
    
    Args:
        monkeypatch: pytest fixture for modifying the environment.
    """
    logger = _StubLogger()
    cache = {("message", "model"): "cached-response"}

    with pytest.raises(RuntimeError):
        pre_send_check_and_cache(
            api_key="",
            message="message",
            model="model",
            cache=cache,
            logger=logger,
            service_name="openai",
            api_key_env_var="OPENAI_API_KEY",
        )

    cached = pre_send_check_and_cache(
        api_key="key",
        message="message",
        model="model",
        cache=cache,
        logger=logger,
        service_name="openai",
        api_key_env_var="OPENAI_API_KEY",
    )
    assert cached == "cached-response"

    cache2 = {}
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    miss = pre_send_check_and_cache(
        api_key="new-key",
        message="other",
        model="other-model",
        cache=cache2,
        logger=logger,
        service_name="openai",
        api_key_env_var="OPENAI_API_KEY",
    )
    assert miss is None
    assert os.environ["OPENAI_API_KEY"] == "new-key"


def test_call_and_cache_response_success_and_error_paths():
    """
    Test that call_and_cache_response correctly handles successful API calls and error scenarios.
    """
    logger = _StubLogger()
    cache = {}
    cache_events = []
    listed_models = []

    def _cache_and_log_func(*args, **kwargs):
        cache_events.append((args, kwargs))

    def _list_models(api_key):
        listed_models.append(api_key)

    ok = call_and_cache_response(
        api_call=lambda: {"ok": True},
        cache_and_log_func=_cache_and_log_func,
        cache=cache,
        cache_key=("prompt", "m"),
        cache_path="cache.pkl",
        jsonl_path="cache.jsonl",
        prompt="prompt",
        model="m",
        api_key="k",
        logger=logger,
        service_name="openai",
        list_available_models_func=_list_models,
        extract_text_from_response=lambda r: str(r),
    )

    assert ok == {"ok": True}
    assert len(cache_events) == 1

    missing_model = call_and_cache_response(
        api_call=lambda: (_ for _ in ()).throw(RuntimeError("404 model not found")),
        cache_and_log_func=_cache_and_log_func,
        cache=cache,
        cache_key=("prompt", "m"),
        cache_path="cache.pkl",
        jsonl_path="cache.jsonl",
        prompt="prompt",
        model="m",
        api_key="k",
        logger=logger,
        service_name="openai",
        list_available_models_func=_list_models,
    )

    assert missing_model is None
    assert listed_models == ["k"]

    other_error = call_and_cache_response(
        api_call=lambda: (_ for _ in ()).throw(RuntimeError("500 internal")),
        cache_and_log_func=_cache_and_log_func,
        cache=cache,
        cache_key=("prompt", "m"),
        cache_path="cache.pkl",
        jsonl_path="cache.jsonl",
        prompt="prompt",
        model="m",
        api_key="k",
        logger=logger,
        service_name="openai",
        list_available_models_func=_list_models,
    )
    assert other_error is None
    assert listed_models == ["k"]

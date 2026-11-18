"""
Tests for mode resolution logic in gabm.__main__.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

from gabm import __main__ as main_mod


def test_resolve_effective_mode_explicit_example():
    """Explicit mode should be used as-is."""
    assert main_mod.resolve_effective_mode("example") == "example"


def test_resolve_effective_mode_auto_prefers_chat_when_credentials(monkeypatch):
    """Auto mode should select chat_opinion when any LLM runtime config is available."""
    monkeypatch.setattr(main_mod, "_has_configured_llm_credentials", lambda: True)
    assert main_mod.resolve_effective_mode("auto") == "chat_opinion"


def test_resolve_effective_mode_auto_falls_back_without_credentials(monkeypatch):
    """Auto mode should fall back to classic example when no credentials are found."""
    monkeypatch.setattr(main_mod, "_has_configured_llm_credentials", lambda: False)
    assert main_mod.resolve_effective_mode("auto") == "example"


def test_resolve_effective_mode_survey_aliases_to_chat_opinion():
    """Survey mode should map to chat_opinion for backward compatibility."""
    assert main_mod.resolve_effective_mode("survey") == "chat_opinion"


def test_has_configured_llm_credentials_accepts_local_openai_endpoint(monkeypatch):
    """OPENAI_BASE_URL alone should enable LLM auto mode selection."""
    monkeypatch.setenv("OPENAI_BASE_URL", "http://127.0.0.1:11434/v1")
    assert main_mod._has_configured_llm_credentials() is True

"""Tests for mode resolution logic in gabm.__main__."""

from gabm import __main__ as main_mod


def test_resolve_effective_mode_explicit_example():
    """Explicit mode should be used as-is."""
    assert main_mod.resolve_effective_mode("example") == "example"


def test_resolve_effective_mode_auto_prefers_chat_when_credentials(monkeypatch):
    """Auto mode should select chat when any LLM credential is available."""
    monkeypatch.setattr(main_mod, "_has_configured_llm_credentials", lambda: True)
    assert main_mod.resolve_effective_mode("auto") == "chat"


def test_resolve_effective_mode_auto_falls_back_without_credentials(monkeypatch):
    """Auto mode should fall back to classic example when no credentials are found."""
    monkeypatch.setattr(main_mod, "_has_configured_llm_credentials", lambda: False)
    assert main_mod.resolve_effective_mode("auto") == "example"

"""
Tests for the chat simulation example script behavior.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Local imports
from gabm.examples.chat.sim import (
    _normalize_utterance,
    build_llm_service,
    build_first_turn_prompt,
    parse_cli_args,
    resolve_llm_api_key,
    resolve_llm_model,
    resolve_llm_seed,
    resolve_llm_service_name,
    resolve_ons_female_file,
    resolve_ons_male_file,
    run,
)


class _FakeLLMService:
    """Minimal fake LLM service for chat simulation testing."""

    def __init__(self, response_text="Hi, I am Alex. What is your name and what are you interested in?"):
        self.response_text = response_text
        self.calls = []

    def send(self, api_key, message, model=None, request_options=None):
        self.calls.append(
            {
                "api_key": api_key,
                "message": message,
                "model": model,
                "request_options": request_options,
            }
        )
        return {"choices": [{"message": {"content": self.response_text}}]}


class _ObjectLLMService:
    """Fake service that returns object-style responses like SDK clients do."""

    class _Message:
        def __init__(self, content):
            self.content = content

    class _Choice:
        def __init__(self, content):
            self.message = _ObjectLLMService._Message(content)

    class _Response:
        def __init__(self, content):
            self.choices = [_ObjectLLMService._Choice(content)]

    def __init__(self, response_text="Object content"):
        self.response_text = response_text
        self.calls = []

    def send(self, api_key, message, model=None, request_options=None):
        self.calls.append(
            {
                "api_key": api_key,
                "message": message,
                "model": model,
                "request_options": request_options,
            }
        )
        return _ObjectLLMService._Response(self.response_text)


class _FingerprintLLMService(_FakeLLMService):
    """Fake service returning OpenAI-like system_fingerprint fields."""

    def __init__(self, response_text="Hi", system_fingerprint="fp_abc123"):
        super().__init__(response_text=response_text)
        self.system_fingerprint = system_fingerprint

    def send(self, api_key, message, model=None, request_options=None):
        self.calls.append(
            {
                "api_key": api_key,
                "message": message,
                "model": model,
                "request_options": request_options,
            }
        )
        return {
            "choices": [{"message": {"content": self.response_text}}],
            "system_fingerprint": self.system_fingerprint,
        }


def test_chat_sim_runs_and_prints_expected_sections(capsys):
    """Test that the chat simulation runs and prints key conversation sections."""
    run(seed=42)

    captured = capsys.readouterr()
    lines = [line for line in captured.out.splitlines() if line.strip()]

    assert len(lines) >= 8
    assert any("years old" in line for line in lines)
    assert any("I am interested in" in line for line in lines)
    assert any("I value " in line for line in lines)
    assert any(line.startswith("Participants:") for line in lines)
    assert any(line.startswith("Round 1:") for line in lines)
    assert any(line.startswith("Round 2:") for line in lines)
    assert any(line.startswith("Round 3:") for line in lines)
    assert any(line.startswith("Round 4:") for line in lines)


def test_build_first_turn_prompt_includes_goal_and_name_fields():
    """Test first-turn prompt includes simulation goal and both names."""
    prompt = build_first_turn_prompt(
        speaker_name="Alex",
        other_name="Jordan",
        speaker_persona="I am a 30 year old person.",
        speaker_interests="I am interested in music.",
        speaker_values="I value kindness.",
        other_persona="I am a 35 year old person.",
    )

    assert "simulate a conversation between two person agents" in prompt.lower()
    assert "Goal: find shared interests" in prompt
    assert "You are Speaker: Alex" in prompt
    assert "Other person: Jordan" in prompt
    assert "introducing yourself or asking the other person's name" in prompt
    assert "Do not prefix the line with the speaker's name" in prompt


def test_build_first_turn_prompt_awkward_mode_changes_goal_text():
    """Awkward mode should produce a less alignment-seeking first-turn prompt."""
    prompt = build_first_turn_prompt(
        speaker_name="Alex",
        other_name="Jordan",
        speaker_persona="I am a 30 year old person.",
        speaker_interests="I am interested in music.",
        speaker_values="I value kindness.",
        other_persona="I am a 35 year old person.",
        conversation_mode="awkward",
    )

    assert "a little awkward" in prompt
    assert "Do not actively search for shared interests" in prompt


def test_normalize_utterance_strips_speaker_prefix():
    """Generated lines prefixed with speaker name should be de-duplicated."""
    assert _normalize_utterance("Amelia", "Amelia: Hi there") == "Hi there"
    assert _normalize_utterance("Amelia", "amelia : Hi there") == "Hi there"


def test_chat_sim_uses_llm_for_first_round(capsys):
    """Test first round uses LLM response when an LLM service is provided."""
    fake = _FakeLLMService("Hello, I'm Alex. What's your name?")

    run(seed=42, llm_service=fake, api_key="key", model="fake-model")

    output = capsys.readouterr().out
    assert len(fake.calls) >= 1
    assert "Round 1:" in output
    assert "Hello, I'm Alex. What's your name?" in output


def test_chat_sim_extracts_text_from_object_llm_response(capsys):
    """Object-style SDK responses should contribute plain text, not object repr."""
    fake = _ObjectLLMService("Hi there from object response")

    run(seed=42, llm_service=fake, api_key="key", model="fake-model")

    output = capsys.readouterr().out
    assert "Round 1:" in output
    assert "Hi there from object response" in output
    assert "ChatCompletion(" not in output

    # Ensure conversation history passed to subsequent prompts is also clean.
    assert len(fake.calls) >= 2
    assert "ChatCompletion(" not in fake.calls[1]["message"]


def test_chat_sim_reproducible_for_same_seed(capsys):
    """Test that running the chat simulation with the same seed prints identical output."""
    run(seed=123)
    first = capsys.readouterr().out

    run(seed=123)
    second = capsys.readouterr().out

    assert first == second


def test_chat_sim_changes_for_different_seeds(capsys):
    """Test that running the chat simulation with different seeds prints different output."""
    run(seed=1)
    transcript_1 = capsys.readouterr().out

    run(seed=2)
    transcript_2 = capsys.readouterr().out

    assert transcript_1 != transcript_2


def test_chat_sim_writes_run_artifacts(tmp_path):
    """Chat simulation should write transcript, console output, and metadata artifacts."""
    run_dir = run(seed=42, output_root=tmp_path, run_id="artifact-check")

    assert run_dir.exists()
    assert (run_dir / "conversation_transcript.txt").exists()
    assert (run_dir / "console_output.txt").exists()
    assert (run_dir / "run_metadata.json").exists()
    assert (run_dir / "prompt_response_cache_delta.jsonl").exists()


def test_chat_sim_same_seed_same_transcript_files(tmp_path):
    """Runs with same seed and no LLM should produce identical transcripts."""
    run_dir_a = run(seed=123, output_root=tmp_path, run_id="seed-123-a")
    run_dir_b = run(seed=123, output_root=tmp_path, run_id="seed-123-b")

    transcript_a = (run_dir_a / "conversation_transcript.txt").read_text(encoding="utf-8")
    transcript_b = (run_dir_b / "conversation_transcript.txt").read_text(encoding="utf-8")

    assert transcript_a == transcript_b


def test_parse_cli_args_reads_ons_file_seed_and_year():
    """Test CLI parser reads ONS file paths, seed, and year options."""
    args = parse_cli_args(
        [
            "--ons-male-file",
            "male.csv",
            "--ons-female-file",
            "female.csv",
            "--seed",
            "7",
            "--year",
            "2030",
        ]
    )

    assert str(args.ons_male_file) == "male.csv"
    assert str(args.ons_female_file) == "female.csv"
    assert args.seed == 7
    assert args.year == 2030


def test_parse_cli_args_reads_llm_options():
    """Test CLI parser reads LLM-related options."""
    args = parse_cli_args(
        [
            "--llm-service",
            "openai",
            "--model",
            "gpt-4o-mini",
            "--llm-seed",
            "42",
            "--api-key",
            "sk-test",
            "--api-key-file",
            "keys.csv",
        ]
    )

    assert args.llm_service == "openai"
    assert args.model == "gpt-4o-mini"
    assert args.llm_seed == 42
    assert args.api_key == "sk-test"
    assert str(args.api_key_file) == "keys.csv"


def test_parse_cli_args_reads_output_options():
    """Test CLI parser reads output root and run id options."""
    args = parse_cli_args(["--output-root", "out/chat", "--run-id", "run-001"])

    assert str(args.output_root) == "out/chat"
    assert args.run_id == "run-001"


def test_parse_cli_args_reads_no_cache_flag():
    """Test CLI parser reads the no-cache switch."""
    args = parse_cli_args(["--no-cache"])

    assert args.no_cache is True


def test_resolve_ons_male_file_prefers_cli_over_env(monkeypatch, tmp_path):
    """CLI male file path should override environment setting."""
    env_file = tmp_path / "env_male.csv"
    cli_file = tmp_path / "cli_male.csv"
    monkeypatch.setenv("GABM_CHAT_ONS_MALE_FILE", str(env_file))

    resolved = resolve_ons_male_file(cli_file)

    assert resolved == cli_file


def test_resolve_ons_female_file_uses_env_when_cli_missing(monkeypatch, tmp_path):
    """Environment female file path should be used when CLI path is missing."""
    env_file = tmp_path / "env_female.csv"
    monkeypatch.setenv("GABM_CHAT_ONS_FEMALE_FILE", str(env_file))

    resolved = resolve_ons_female_file(None)

    assert resolved == env_file


def test_resolve_llm_service_name_prefers_cli_over_env(monkeypatch):
    """CLI service name should override environment setting."""
    monkeypatch.setenv("GABM_CHAT_LLM_SERVICE", "deepseek")

    resolved = resolve_llm_service_name("openai")

    assert resolved == "openai"


def test_resolve_llm_model_uses_env_when_cli_missing(monkeypatch):
    """Environment model should be used when CLI model is not provided."""
    monkeypatch.setenv("GABM_CHAT_LLM_MODEL", "models/gemini-2.5-pro")

    resolved = resolve_llm_model(None)

    assert resolved == "models/gemini-2.5-pro"


def test_resolve_llm_seed_uses_env_when_cli_missing(monkeypatch):
    """Environment LLM seed should be used when CLI seed is not provided."""
    monkeypatch.setenv("GABM_CHAT_LLM_SEED", "123")

    resolved = resolve_llm_seed(None)

    assert resolved == 123


def test_resolve_llm_seed_ignores_invalid_env(monkeypatch):
    """Invalid environment seed should be ignored and treated as missing."""
    monkeypatch.setenv("GABM_CHAT_LLM_SEED", "not-an-int")

    resolved = resolve_llm_seed(None)

    assert resolved is None


def test_resolve_llm_api_key_prefers_cli_over_file(tmp_path):
    """CLI API key should override key values in API key CSV file."""
    api_file = tmp_path / "api_key.csv"
    api_file.write_text("api,key\nopenai,sk-file\n", encoding="utf-8")

    resolved = resolve_llm_api_key("sk-cli", "openai", api_file)

    assert resolved == "sk-cli"


def test_resolve_llm_api_key_uses_file_when_cli_missing(tmp_path):
    """API key should be loaded from file when CLI override is missing."""
    api_file = tmp_path / "api_key.csv"
    api_file.write_text("api,key\nopenai,sk-file\n", encoding="utf-8")

    resolved = resolve_llm_api_key(None, "openai", api_file)

    assert resolved == "sk-file"


def test_build_llm_service_rejects_unknown_service():
    """Unknown LLM service names should raise ValueError."""
    import pytest

    with pytest.raises(ValueError):
        build_llm_service("not-a-service")


def test_chat_metadata_records_cache_enabled_flag(tmp_path):
    """Run metadata should reflect current cache setting on the llm service."""
    fake = _FakeLLMService("Hi")
    fake.SERVICE_NAME = "fake"
    fake.use_cache = False

    run_dir = run(
        seed=42,
        llm_service=fake,
        api_key="key",
        model="fake-model",
        output_root=tmp_path,
        run_id="metadata-cache-flag",
    )

    import json

    metadata = json.loads((run_dir / "run_metadata.json").read_text(encoding="utf-8"))
    assert metadata["cache_enabled"] is False


def test_chat_sim_passes_llm_seed_to_request_options(capsys):
    """Configured llm_seed should be forwarded as provider request options."""
    fake = _FakeLLMService("Hello")

    run(seed=42, llm_service=fake, api_key="key", model="fake-model", llm_seed=99)
    _ = capsys.readouterr().out

    assert len(fake.calls) >= 1
    assert fake.calls[0]["request_options"] == {"seed": 99}


def test_chat_metadata_records_system_fingerprint_and_llm_seed(tmp_path):
    """Run metadata should include OpenAI-like fingerprints and llm_seed."""
    fake = _FingerprintLLMService(response_text="Hi", system_fingerprint="fp_test")
    fake.SERVICE_NAME = "openai"

    run_dir = run(
        seed=42,
        llm_service=fake,
        api_key="key",
        model="gpt-4o-mini",
        llm_seed=42,
        output_root=tmp_path,
        run_id="metadata-seed-fingerprint",
    )

    import json

    metadata = json.loads((run_dir / "run_metadata.json").read_text(encoding="utf-8"))
    assert metadata["llm_seed"] == 42
    assert metadata["openai_system_fingerprints"] == ["fp_test"]


def test_chat_metadata_records_awkward_mode_fields(tmp_path):
    """Awkward-mode run should record mode and awkwardness metadata fields."""
    run_dir = run(
        seed=42,
        output_root=tmp_path,
        run_id="awkward-meta",
        conversation_mode="awkward",
    )

    import json

    metadata = json.loads((run_dir / "run_metadata.json").read_text(encoding="utf-8"))
    assert metadata["conversation_mode"] == "awkward"
    assert "pair_dissimilarity_score" in metadata
    assert "awkward_marker_count" in metadata
    assert "disagreement_marker_count" in metadata


def test_max_dissimilarity_pairing_increases_pair_dissimilarity(tmp_path):
    """Max-dissimilarity pairing should not be less dissimilar than random pairing for same seed."""
    random_dir = run(
        seed=77,
        output_root=tmp_path,
        run_id="pair-random",
        pairing_strategy="random",
        candidate_pool_size=8,
    )
    max_dir = run(
        seed=77,
        output_root=tmp_path,
        run_id="pair-max",
        pairing_strategy="max_dissimilarity",
        candidate_pool_size=8,
    )

    import json

    random_meta = json.loads((random_dir / "run_metadata.json").read_text(encoding="utf-8"))
    max_meta = json.loads((max_dir / "run_metadata.json").read_text(encoding="utf-8"))

    assert max_meta["pair_dissimilarity_score"] >= random_meta["pair_dissimilarity_score"]

"""
Tests for the chat-opinion simulation example.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


import json

from gabm.abm.environment import Environment
from gabm.abm.agent import PersonID, Person
from gabm.examples.chat_opinion.sim import (
    _get_person_opinion_about,
    _set_person_opinion_about,
    parse_cli_args,
    run,
)


class _FakeLLMService:
    SERVICE_NAME = "fake"

    def __init__(self, response_text="Thanks, that's interesting!"):
        self.response_text = response_text
        self.calls = []
        self.use_cache = True

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


def test_parse_cli_args_reads_rounds():
    args = parse_cli_args(["--rounds", "12"])
    assert args.rounds == 12


def test_parse_cli_args_reads_awkward_pairing_flags():
    args = parse_cli_args(
        [
            "--conversation-mode",
            "awkward",
            "--pairing-strategy",
            "max_dissimilarity",
            "--candidate-pool-size",
            "10",
        ]
    )
    assert args.conversation_mode == "awkward"
    assert args.pairing_strategy == "max_dissimilarity"
    assert args.candidate_pool_size == 10


def test_chat_opinion_run_writes_expected_artifacts(tmp_path):
    run_dir = run(seed=42, rounds=6, output_root=tmp_path, run_id="chat-opinion-artifacts")

    assert (run_dir / "conversation_transcript.txt").exists()
    assert (run_dir / "console_output.txt").exists()
    assert (run_dir / "run_metadata.json").exists()
    assert (run_dir / "opinion_history.json").exists()
    assert (run_dir / "opinion_change.png").exists()

    metadata = json.loads((run_dir / "run_metadata.json").read_text(encoding="utf-8"))
    assert metadata["rounds"] == 6


def test_chat_opinion_run_is_deterministic_without_llm(tmp_path):
    run_a = run(seed=123, rounds=8, output_root=tmp_path, run_id="det-a")
    run_b = run(seed=123, rounds=8, output_root=tmp_path, run_id="det-b")

    history_a = (run_a / "opinion_history.json").read_text(encoding="utf-8")
    history_b = (run_b / "opinion_history.json").read_text(encoding="utf-8")
    transcript_a = (run_a / "conversation_transcript.txt").read_text(encoding="utf-8")
    transcript_b = (run_b / "conversation_transcript.txt").read_text(encoding="utf-8")

    assert history_a == history_b
    assert transcript_a == transcript_b


def test_chat_opinion_passes_llm_seed_request_options(tmp_path):
    fake = _FakeLLMService()
    run(
        seed=42,
        rounds=4,
        llm_service=fake,
        api_key="key",
        model="fake-model",
        llm_seed=77,
        output_root=tmp_path,
        run_id="llm-seed-pass",
    )

    assert len(fake.calls) >= 1
    assert fake.calls[0]["request_options"] == {"seed": 77}


def test_chat_opinion_helpers_store_values_on_person_attributes():
    env = Environment(year=2026)
    person_a = Person(PersonID(1), environment=env, year_of_birth=1990, gender_id=None)
    person_b = Person(PersonID(2), environment=env, year_of_birth=1992, gender_id=None)

    assert _get_person_opinion_about(person_a, person_b, default=-0.1) == -0.1

    _set_person_opinion_about(person_a, person_b, 0.75)
    value = _get_person_opinion_about(person_a, person_b)

    assert value == 0.75
    assert len(person_a.opinions) == 1


def test_chat_opinion_metadata_records_opinion_topic_ids(tmp_path):
    run_dir = run(seed=42, rounds=4, output_root=tmp_path, run_id="topic-id-meta")
    metadata = json.loads((run_dir / "run_metadata.json").read_text(encoding="utf-8"))

    assert "opinion_topic_id_a_about_b" in metadata
    assert "opinion_topic_id_b_about_a" in metadata


def test_chat_opinion_awkward_mode_records_metadata(tmp_path):
    run_dir = run(
        seed=42,
        rounds=4,
        output_root=tmp_path,
        run_id="awkward-opinion-meta",
        conversation_mode="awkward",
        pairing_strategy="max_dissimilarity",
        candidate_pool_size=8,
    )
    metadata = json.loads((run_dir / "run_metadata.json").read_text(encoding="utf-8"))

    assert metadata["conversation_mode"] == "awkward"
    assert metadata["pairing_strategy"] == "max_dissimilarity"
    assert metadata["candidate_pool_size"] == 8
    assert "pair_dissimilarity_score" in metadata
    assert "awkward_marker_count" in metadata
    assert "disagreement_marker_count" in metadata

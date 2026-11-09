"""
Two-agent chat example with evolving interpersonal opinions.
This module simulates a conversation between two person agents, 
where their opinions of each other evolve based on the content 
of their dialogue. The simulation can optionally use a large 
language model (LLM) service to generate the dialogue, and it 
produces output artifacts including a conversation transcript, 
console output, and metadata about the run.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

import argparse
import itertools
import json
import random
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

from gabm.abm.environment import Environment
from gabm.abm.data.names_ons import get_default_ons_name_paths
from gabm.abm.attributes.opinion import Opinion, OpinionTopicID
from gabm.examples.chat.sim import (
    _extract_text_from_llm_response,
    _normalize_utterance,
    _build_run_dir_name,
    _jsonl_line_count,
    _read_jsonl_slice,
    build_llm_service,
    build_first_turn_prompt,
    build_follow_up_prompt,
    resolve_llm_api_key,
    resolve_llm_model,
    resolve_llm_seed,
    resolve_llm_service_name,
    resolve_ons_female_file,
    resolve_ons_male_file,
)

_DEFAULT_ONS_MALE_FILE, _DEFAULT_ONS_FEMALE_FILE = get_default_ons_name_paths()
_DEFAULT_OUTPUT_ROOT = Path("data/output/examples/chat_opinion")
_DEFAULT_API_KEY_FILE = Path("data/api_key.csv")


def parse_cli_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line options for the chat-opinion simulation script."""
    parser = argparse.ArgumentParser(description="Run chat-opinion simulation example.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducible simulation output.")
    parser.add_argument("--year", type=int, default=2026, help="Simulation year used by the environment.")
    parser.add_argument("--rounds", type=int, default=8, help="Number of conversation rounds to run.")
    parser.add_argument("--ons-male-file", type=Path, default=_DEFAULT_ONS_MALE_FILE)
    parser.add_argument("--ons-female-file", type=Path, default=_DEFAULT_ONS_FEMALE_FILE)
    parser.add_argument("--llm-service", type=str, default=None)
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--llm-seed", type=int, default=None)
    parser.add_argument("--api-key", type=str, default=None)
    parser.add_argument("--api-key-file", type=Path, default=_DEFAULT_API_KEY_FILE)
    parser.add_argument("--output-root", type=Path, default=_DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--run-id", type=str, default=None)
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--conversation-mode", type=str, choices=["normal", "awkward"], default="normal")
    parser.add_argument("--pairing-strategy", type=str, choices=["random", "max_dissimilarity"], default="random")
    parser.add_argument("--candidate-pool-size", type=int, default=8)
    return parser.parse_args(argv)


def _fallback_turn_line(rng: random.Random, speaker_name: str, other_name: str, round_num: int) -> str:
    if round_num == 1:
        return f"Hi {other_name}, I'm {speaker_name}. What do you enjoy doing?"
    options = [
        f"I like how you put that, {other_name}.",
        f"That makes sense, {other_name}. Tell me more.",
        f"Interesting point, {other_name}. I can relate.",
        f"Thanks for sharing that, {other_name}.",
    ]
    return rng.choice(options)


def _clamp_opinion(value: float) -> float:
    return max(-2.0, min(2.0, value))


def _extract_topic_tokens(summary: str) -> set[str]:
    cleaned = summary.lower().replace(".", " ").replace(",", " ")
    stop_words = {
        "i", "am", "interested", "in", "and", "not", "have", "no", "currently", "don", "t", "what", "my"
    }
    return {token for token in cleaned.split() if len(token) > 2 and token not in stop_words}


def _compute_opinion_delta(utterance: str, shared_interest_score: float) -> float:
    text = utterance.lower()
    positive_tokens = ["great", "thanks", "love", "nice", "interesting", "awesome", "agree", "happy"]
    negative_tokens = ["boring", "hate", "bad", "annoying", "disagree", "awful"]

    delta = 0.0
    if "?" in utterance:
        delta += 0.2
    if any(token in text for token in positive_tokens):
        delta += 0.2
    if any(token in text for token in negative_tokens):
        delta -= 0.3

    # Shared interests provide a persistent positive drift, capped to avoid runaway.
    delta += min(0.3, max(0.0, shared_interest_score))
    return delta


def _write_opinion_plot(run_dir: Path, rounds: list[int], a_about_b: list[float], b_about_a: list[float]):
    fig_path = run_dir / "opinion_change.png"
    plt.figure(figsize=(8, 4.5))
    plt.plot(rounds, a_about_b, marker="o", label="Person A opinion of B")
    plt.plot(rounds, b_about_a, marker="o", label="Person B opinion of A")
    plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    plt.ylim(-2.1, 2.1)
    plt.xlabel("Round")
    plt.ylabel("Opinion score")
    plt.title("Interpersonal opinion change over conversation")
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_path)
    plt.close()


def _compute_pair_similarity(person_a, person_b, shared_interest_score: float) -> dict:
    """Compute a coarse pair-similarity score for analysis and ensemble grouping."""
    age_a = person_a.get_age()
    age_b = person_b.get_age()
    if age_a is None or age_b is None:
        age_similarity = 0.5
    else:
        # Age differences above 40 years are treated as maximally dissimilar.
        age_similarity = max(0.0, 1.0 - min(40.0, abs(age_a - age_b)) / 40.0)

    gender_a = person_a.get_gender().strip().lower()
    gender_b = person_b.get_gender().strip().lower()
    if gender_a in {"none", "unknown"} or gender_b in {"none", "unknown"}:
        gender_similarity = 0.5
    else:
        gender_similarity = 1.0 if gender_a == gender_b else 0.0

    interest_similarity = max(0.0, min(1.0, shared_interest_score))

    # Weighted blend: interests influence most, then age, then gender.
    similarity_score = (0.40 * interest_similarity) + (0.35 * age_similarity) + (0.25 * gender_similarity)
    return {
        "score": round(similarity_score, 4),
        "dissimilarity_score": round(1.0 - similarity_score, 4),
        "age_similarity": round(age_similarity, 4),
        "gender_similarity": round(gender_similarity, 4),
        "interest_similarity": round(interest_similarity, 4),
    }


def _pair_shared_interest_score(person_a, person_b) -> float:
    tokens_a = _extract_topic_tokens(person_a.get_interests_summary())
    tokens_b = _extract_topic_tokens(person_b.get_interests_summary())
    if not tokens_a and not tokens_b:
        return 0.0
    return len(tokens_a & tokens_b) / max(1, len(tokens_a | tokens_b))


def _select_pair_by_dissimilarity(candidates: list):
    """Select the most dissimilar pair from candidate people."""
    best_pair = None
    best_score = -1.0
    for person_a, person_b in itertools.combinations(candidates, 2):
        shared_score = _pair_shared_interest_score(person_a, person_b)
        pair_metrics = _compute_pair_similarity(person_a, person_b, shared_score)
        score = pair_metrics["dissimilarity_score"]
        if score > best_score:
            best_pair = (person_a, person_b)
            best_score = score
    if best_pair is None:
        raise ValueError("Unable to select participant pair from candidate pool")
    return best_pair[0], best_pair[1]


def _opinion_topic_id_for_target(target_person) -> OpinionTopicID:
    """Map a target person to a stable synthetic opinion topic ID."""
    target_id_num = target_person.id.id if hasattr(target_person.id, "id") else int(target_person.id)
    return OpinionTopicID(10_000 + target_id_num)


def _set_person_opinion_about(person, target_person, value: float):
    """Persist one person's opinion of another on person.opinions."""
    topic_id = _opinion_topic_id_for_target(target_person)
    person.opinions[topic_id] = Opinion(topic_id, opinion_values=None, value=round(value, 4))


def _get_person_opinion_about(person, target_person, default: float = 0.0) -> float:
    """Read one person's opinion of another from person.opinions."""
    topic_id = _opinion_topic_id_for_target(target_person)
    opinion = person.opinions.get(topic_id)
    if opinion is None:
        return default
    return float(opinion.value)


def run(
    seed: int = 42,
    year: int = 2026,
    rounds: int = 8,
    llm_service=None,
    api_key: str | None = None,
    model: str | None = None,
    llm_seed: int | None = None,
    ons_male_file: Path | None = None,
    ons_female_file: Path | None = None,
    output_root: Path | None = None,
    run_id: str | None = None,
    emit_console_output: bool = True,
    conversation_mode: str = "normal",
    pairing_strategy: str = "random",
    candidate_pool_size: int = 8,
):
    """Run a two-agent conversation with evolving opinions and visualization."""
    if rounds < 1:
        raise ValueError("rounds must be >= 1")
    if candidate_pool_size < 2:
        raise ValueError("candidate_pool_size must be >= 2")

    rng = random.Random(seed)
    console_lines: list[str] = []

    service_name = None
    if llm_service is not None:
        service_name = getattr(llm_service, "SERVICE_NAME", None)
    if service_name is None:
        service_name = "no-llm"

    resolved_output_root = Path(output_root) if output_root is not None else _DEFAULT_OUTPUT_ROOT
    run_dir_name = _build_run_dir_name(seed=seed, llm_service_name=service_name, run_id=run_id)
    run_dir = resolved_output_root / run_dir_name
    run_dir.mkdir(parents=True, exist_ok=True)

    cache_jsonl_path = None
    if llm_service is not None:
        jsonl_raw = getattr(llm_service, "jsonl_path", None)
        if jsonl_raw:
            cache_jsonl_path = Path(jsonl_raw)
    cache_line_count_before = _jsonl_line_count(cache_jsonl_path)

    def emit(line: str):
        if emit_console_output:
            print(line)
        console_lines.append(line)

    # Create environment and random candidates with interests
    env = Environment(year=year)
    candidate_count = 2 if pairing_strategy == "random" else candidate_pool_size
    people = env.create_random_people(
        count=candidate_count,
        start_person_id=1,
        seed=seed,
        with_interests=True,
        ons_male_file=ons_male_file or _DEFAULT_ONS_MALE_FILE,
        ons_female_file=ons_female_file or _DEFAULT_ONS_FEMALE_FILE,
    )

    if pairing_strategy == "max_dissimilarity":
        person_a, person_b = _select_pair_by_dissimilarity(people)
    else:
        person_a, person_b = people[0], people[1]
    name_a, name_b = person_a.get_name(), person_b.get_name()

    emit(str(person_a))
    emit(person_a.get_self_description())
    interests_a = person_a.get_interests_summary()
    interests_b = person_b.get_interests_summary()
    emit(interests_a)
    emit(person_a.get_values_summary())

    emit(str(person_b))
    emit(person_b.get_self_description())
    emit(interests_b)
    emit(person_b.get_values_summary())
    emit(f"Participants: {name_a} and {name_b}")

    tokens_a = _extract_topic_tokens(interests_a)
    tokens_b = _extract_topic_tokens(interests_b)
    shared_interest_score = 0.0
    if tokens_a or tokens_b:
        shared_interest_score = len(tokens_a & tokens_b) / max(1, len(tokens_a | tokens_b))
    pair_similarity = _compute_pair_similarity(person_a, person_b, shared_interest_score)

    _set_person_opinion_about(person_a, person_b, -0.2 + shared_interest_score)
    _set_person_opinion_about(person_b, person_a, -0.2 + shared_interest_score)

    history_lines: list[str] = []
    round_axis: list[int] = [0]
    series_a_about_b: list[float] = [round(_get_person_opinion_about(person_a, person_b), 4)]
    series_b_about_a: list[float] = [round(_get_person_opinion_about(person_b, person_a), 4)]

    request_options = {"seed": llm_seed} if llm_seed is not None else None
    first_shared_interest_round = None
    awkward_marker_count = 0
    disagreement_marker_count = 0
    awkward_markers = ["awkward", "uh", "hmm", "not sure", "anyway", "right", "fine"]
    disagreement_markers = ["disagree", "not really", "different", "not my thing", "don't think", "however"]

    for round_num in range(1, rounds + 1):
        if round_num % 2 == 1:
            speaker, other = person_a, person_b
            speaker_name, other_name = name_a, name_b
        else:
            speaker, other = person_b, person_a
            speaker_name, other_name = name_b, name_a

        current_opinion = _get_person_opinion_about(speaker, other)

        speaker_persona = speaker.get_self_description()
        speaker_interests = speaker.get_interests_summary()
        speaker_values = speaker.get_values_summary()
        other_persona = other.get_self_description()

        opinion_hint = f"Your current opinion of {other_name} is {current_opinion:.2f} on a scale from -2 to 2."
        if round_num == 1:
            prompt = build_first_turn_prompt(
                speaker_name=speaker_name,
                other_name=other_name,
                speaker_persona=speaker_persona,
                speaker_interests=speaker_interests,
                speaker_values=speaker_values,
                other_persona=other_persona,
                conversation_mode=conversation_mode,
            )
        else:
            prompt = build_follow_up_prompt(
                speaker_name=speaker_name,
                other_name=other_name,
                speaker_persona=speaker_persona,
                speaker_interests=speaker_interests,
                speaker_values=speaker_values,
                other_persona=other_persona,
                history_lines=history_lines,
                conversation_mode=conversation_mode,
                round_num=round_num,
            )
        prompt = f"{prompt}\n{opinion_hint}"

        utterance = ""
        if llm_service is not None and api_key:
            response = llm_service.send(api_key, prompt, model=model, request_options=request_options)
            utterance = _extract_text_from_llm_response(response)

        if not utterance:
            if conversation_mode == "awkward":
                if round_num == 1:
                    utterance = f"Hi {other_name}. I'm {speaker_name}."
                else:
                    utterance = rng.choice(
                        [
                            "I see. I'm not sure what to add yet.",
                            "That's different from what I usually do.",
                            "Hmm, fair enough. I suppose that works for you.",
                        ]
                    )
            else:
                utterance = _fallback_turn_line(rng, speaker_name, other_name, round_num)

        utterance = _normalize_utterance(speaker_name, utterance)
        utterance_lower = utterance.lower()
        if first_shared_interest_round is None:
            if any(marker in utterance_lower for marker in ["same", "also", "too", "both", "common", "me too"]):
                first_shared_interest_round = round_num
        awkward_marker_count += sum(1 for marker in awkward_markers if marker in utterance_lower)
        disagreement_marker_count += sum(1 for marker in disagreement_markers if marker in utterance_lower)
        line = f"Round {round_num}: {speaker_name}: {utterance}"
        emit(line)
        history_lines.append(line)

        delta = _compute_opinion_delta(utterance, shared_interest_score)
        if round_num % 2 == 1:
            updated = _clamp_opinion(_get_person_opinion_about(person_b, person_a) + delta)
            _set_person_opinion_about(person_b, person_a, updated)
        else:
            updated = _clamp_opinion(_get_person_opinion_about(person_a, person_b) + delta)
            _set_person_opinion_about(person_a, person_b, updated)

        round_axis.append(round_num)
        opinion_a_about_b = _get_person_opinion_about(person_a, person_b)
        opinion_b_about_a = _get_person_opinion_about(person_b, person_a)
        series_a_about_b.append(round(opinion_a_about_b, 4))
        series_b_about_a.append(round(opinion_b_about_a, 4))
        emit(
            f"Opinion state after round {round_num}: "
            f"{name_a}-> {name_b}={opinion_a_about_b:.2f}, {name_b}-> {name_a}={opinion_b_about_a:.2f}"
        )

    _write_opinion_plot(run_dir, round_axis, series_a_about_b, series_b_about_a)

    transcript_path = run_dir / "conversation_transcript.txt"
    transcript_path.write_text("\n".join(history_lines) + "\n", encoding="utf-8")

    console_path = run_dir / "console_output.txt"
    console_path.write_text("\n".join(console_lines) + "\n", encoding="utf-8")

    opinion_history_path = run_dir / "opinion_history.json"
    opinion_history_path.write_text(
        json.dumps(
            {
                "round": round_axis,
                "opinion_a_about_b": series_a_about_b,
                "opinion_b_about_a": series_b_about_a,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    cache_delta_lines = _read_jsonl_slice(cache_jsonl_path, cache_line_count_before)
    cache_delta_path = run_dir / "prompt_response_cache_delta.jsonl"
    cache_delta_path.write_text("".join(cache_delta_lines), encoding="utf-8")

    metadata_path = run_dir / "run_metadata.json"
    metadata_path.write_text(
        json.dumps(
            {
                "seed": seed,
                "year": year,
                "rounds": rounds,
                "llm_service": service_name,
                "llm_seed": llm_seed,
                "cache_enabled": None if llm_service is None else bool(getattr(llm_service, "use_cache", True)),
                "model": model,
                "conversation_mode": conversation_mode,
                "pairing_strategy": pairing_strategy,
                "candidate_pool_size": candidate_count,
                "participants": [name_a, name_b],
                "shared_interest_score": round(shared_interest_score, 4),
                "pair_similarity_score": pair_similarity["score"],
                "pair_dissimilarity_score": pair_similarity["dissimilarity_score"],
                "pair_similarity_components": {
                    "age_similarity": pair_similarity["age_similarity"],
                    "gender_similarity": pair_similarity["gender_similarity"],
                    "interest_similarity": pair_similarity["interest_similarity"],
                },
                "first_shared_interest_round": first_shared_interest_round,
                "awkward_marker_count": awkward_marker_count,
                "disagreement_marker_count": disagreement_marker_count,
                "opinion_topic_id_a_about_b": _opinion_topic_id_for_target(person_b).id,
                "opinion_topic_id_b_about_a": _opinion_topic_id_for_target(person_a).id,
                "run_dir": str(run_dir),
                "created_at": datetime.now().isoformat(timespec="seconds"),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    return run_dir


if __name__ == "__main__":
    args = parse_cli_args()
    llm_service_name = resolve_llm_service_name(args.llm_service)
    llm_service = build_llm_service(llm_service_name)
    if llm_service is not None and args.no_cache:
        llm_service.use_cache = False

    api_key = resolve_llm_api_key(args.api_key, llm_service_name, args.api_key_file)
    model = resolve_llm_model(args.model)
    llm_seed = resolve_llm_seed(args.llm_seed)

    run(
        seed=args.seed,
        year=args.year,
        rounds=args.rounds,
        llm_service=llm_service,
        api_key=api_key,
        model=model,
        llm_seed=llm_seed,
        ons_male_file=resolve_ons_male_file(args.ons_male_file),
        ons_female_file=resolve_ons_female_file(args.ons_female_file),
        output_root=args.output_root,
        run_id=args.run_id,
        conversation_mode=args.conversation_mode,
        pairing_strategy=args.pairing_strategy,
        candidate_pool_size=args.candidate_pool_size,
    )

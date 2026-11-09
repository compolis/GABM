"""Tests for chat_opinion ensemble similarity sweep."""

import csv
import json

from gabm.examples.chat_opinion.ensembles.similarity_sweep import parse_cli_args, run_sweep


def test_parse_cli_args_reads_n_runs():
    args = parse_cli_args(
        [
            "--n-runs",
            "7",
            "--start-seed",
            "11",
            "--conversation-mode",
            "awkward",
            "--pairing-strategy",
            "max_dissimilarity",
            "--candidate-pool-size",
            "9",
        ]
    )
    assert args.n_runs == 7
    assert args.start_seed == 11
    assert args.conversation_mode == "awkward"
    assert args.pairing_strategy == "max_dissimilarity"
    assert args.candidate_pool_size == 9


def test_similarity_sweep_writes_expected_artifacts(tmp_path):
    sweep_dir = run_sweep(
        start_seed=10,
        n_runs=3,
        rounds=4,
        output_root=tmp_path,
        run_id="sweep-a",
        conversation_mode="awkward",
        pairing_strategy="max_dissimilarity",
        candidate_pool_size=8,
    )

    assert (sweep_dir / "similarity_sweep_results.csv").exists()
    assert (sweep_dir / "similarity_bin_summary.json").exists()
    assert (sweep_dir / "similarity_vs_final_opinion.png").exists()
    assert (sweep_dir / "sweep_metadata.json").exists()

    rows_path = sweep_dir / "similarity_sweep_results.csv"
    with rows_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 3
    assert "pair_dissimilarity_score" in rows[0]
    assert "first_shared_interest_round" in rows[0]
    assert "awkward_marker_count" in rows[0]

    summary = json.loads((sweep_dir / "similarity_bin_summary.json").read_text(encoding="utf-8"))
    assert len(summary) == 5


def test_similarity_sweep_is_reproducible_for_same_seed_window(tmp_path):
    sweep_dir_a = run_sweep(start_seed=20, n_runs=2, rounds=4, output_root=tmp_path, run_id="sweep-b-a")
    sweep_dir_b = run_sweep(start_seed=20, n_runs=2, rounds=4, output_root=tmp_path, run_id="sweep-b-b")

    with (sweep_dir_a / "similarity_sweep_results.csv").open("r", encoding="utf-8", newline="") as handle_a:
        rows_a = list(csv.DictReader(handle_a))
    with (sweep_dir_b / "similarity_sweep_results.csv").open("r", encoding="utf-8", newline="") as handle_b:
        rows_b = list(csv.DictReader(handle_b))

    stable_fields = [
        "seed",
        "pair_similarity_score",
        "pair_dissimilarity_score",
        "age_similarity",
        "gender_similarity",
        "interest_similarity",
        "first_shared_interest_round",
        "awkward_marker_count",
        "disagreement_marker_count",
        "initial_mean_opinion",
        "final_mean_opinion",
        "delta_mean_opinion",
        "final_opinion_gap",
        "conversation_mode",
        "pairing_strategy",
        "similarity_bin",
    ]
    projected_a = [{key: row[key] for key in stable_fields} for row in rows_a]
    projected_b = [{key: row[key] for key in stable_fields} for row in rows_b]
    assert projected_a == projected_b

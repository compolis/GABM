"""Tests for chat ensemble similarity sweep."""

import csv
import json

from gabm.examples.chat.ensembles.similarity_sweep import parse_cli_args, run_sweep


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
            "10",
        ]
    )
    assert args.n_runs == 7
    assert args.start_seed == 11
    assert args.conversation_mode == "awkward"
    assert args.pairing_strategy == "max_dissimilarity"
    assert args.candidate_pool_size == 10


def test_similarity_sweep_writes_expected_artifacts(tmp_path):
    sweep_dir = run_sweep(
        start_seed=10,
        n_runs=3,
        output_root=tmp_path,
        run_id="chat-sweep-a",
        conversation_mode="awkward",
        pairing_strategy="max_dissimilarity",
        candidate_pool_size=8,
    )

    assert (sweep_dir / "similarity_sweep_results.csv").exists()
    assert (sweep_dir / "similarity_bin_summary.json").exists()
    assert (sweep_dir / "similarity_vs_transcript_size.png").exists()
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
    sweep_dir_a = run_sweep(start_seed=20, n_runs=2, output_root=tmp_path, run_id="chat-sweep-b-a")
    sweep_dir_b = run_sweep(start_seed=20, n_runs=2, output_root=tmp_path, run_id="chat-sweep-b-b")

    with (sweep_dir_a / "similarity_sweep_results.csv").open("r", encoding="utf-8", newline="") as handle_a:
        rows_a = list(csv.DictReader(handle_a))
    with (sweep_dir_b / "similarity_sweep_results.csv").open("r", encoding="utf-8", newline="") as handle_b:
        rows_b = list(csv.DictReader(handle_b))

    stable_fields = [
        "seed",
        "shared_interest_score",
        "transcript_line_count",
        "transcript_char_count",
        "cache_delta_line_count",
        "llm_service",
        "model",
        "fingerprint_count",
        "similarity_bin",
    ]
    projected_a = [{key: row[key] for key in stable_fields} for row in rows_a]
    projected_b = [{key: row[key] for key in stable_fields} for row in rows_b]
    assert projected_a == projected_b

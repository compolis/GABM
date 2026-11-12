"""
Tests for chat_opinion run summary utility.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

import json

from analysis.chat_opinion.summarize_runs import parse_cli_args, summarize_runs


def test_parse_cli_args_reads_prefix_and_run_ids(tmp_path):
    args = parse_cli_args(
        [
            "--root",
            str(tmp_path),
            "--run-id",
            "run_a",
            "--run-id",
            "run_b",
            "--prefix",
            "review_",
        ]
    )

    assert args.root == tmp_path
    assert args.run_id == ["run_a", "run_b"]
    assert args.prefix == "review_"


def test_summarize_runs_aggregates_ranges(tmp_path):
    root = tmp_path / "chat_opinion"
    root.mkdir(parents=True, exist_ok=True)

    run_a = root / "review_a"
    run_b = root / "review_b"
    run_a.mkdir()
    run_b.mkdir()

    (run_a / "run_metadata.json").write_text(
        json.dumps(
            {
                "seed": 42,
                "conversation_mode": "normal",
                "pairing_strategy": "random",
                "initial_mean_opinion": 0.2,
                "final_mean_opinion": 1.6,
                "delta_mean_opinion": 1.4,
                "final_opinion_gap": 0.1,
                "pair_dissimilarity_score": 0.4,
                "awkward_marker_count": 0,
                "disagreement_marker_count": 0,
            }
        ),
        encoding="utf-8",
    )
    (run_b / "run_metadata.json").write_text(
        json.dumps(
            {
                "seed": 43,
                "conversation_mode": "awkward",
                "pairing_strategy": "max_dissimilarity",
                "initial_mean_opinion": -0.2,
                "final_mean_opinion": 0.8,
                "delta_mean_opinion": 1.0,
                "final_opinion_gap": 0.5,
                "pair_dissimilarity_score": 0.8,
                "awkward_marker_count": 2,
                "disagreement_marker_count": 1,
            }
        ),
        encoding="utf-8",
    )

    summary = summarize_runs(root=root, prefix="review_")
    assert summary["n_runs"] == 2
    assert len(summary["rows"]) == 2
    assert summary["ranges"]["final_mean_opinion"] == [0.8, 1.6]
    assert summary["ranges"]["delta_mean_opinion"] == [1.0, 1.4]
    assert summary["ranges"]["final_opinion_gap"] == [0.1, 0.5]
    assert summary["stats"]["final_mean_opinion"]["mean"] == 1.2
    assert summary["stats"]["final_mean_opinion"]["stddev"] == 0.4
    assert summary["stats"]["delta_mean_opinion"]["mean"] == 1.2
    assert summary["stats"]["delta_mean_opinion"]["stddev"] == 0.2
    assert summary["stats"]["final_opinion_gap"]["mean"] == 0.3
    assert summary["stats"]["final_opinion_gap"]["stddev"] == 0.2

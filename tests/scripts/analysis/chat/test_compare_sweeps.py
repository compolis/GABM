"""Tests for ensemble sweep comparison utility."""

import csv
import json

import pytest

from analysis.chat.compare_sweeps import compare_sweeps, parse_cli_args


def _write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def test_parse_cli_args_reads_paths_and_labels(tmp_path):
    sweep_a = tmp_path / "a"
    sweep_b = tmp_path / "b"
    args = parse_cli_args([
        "--sweep-a",
        str(sweep_a),
        "--sweep-b",
        str(sweep_b),
        "--label-a",
        "hosted",
        "--label-b",
        "hpc",
    ])

    assert args.sweep_a == sweep_a
    assert args.sweep_b == sweep_b
    assert args.label_a == "hosted"
    assert args.label_b == "hpc"


def test_compare_sweeps_writes_report_and_summary(tmp_path):
    sweep_a = tmp_path / "sweep_a"
    sweep_b = tmp_path / "sweep_b"
    sweep_a.mkdir(parents=True, exist_ok=True)
    sweep_b.mkdir(parents=True, exist_ok=True)

    rows_a = [
        {
            "seed": 1,
            "shared_interest_score": 0.2,
            "transcript_char_count": 100,
            "similarity_bin": "0.2-0.4",
        },
        {
            "seed": 2,
            "shared_interest_score": 0.4,
            "transcript_char_count": 120,
            "similarity_bin": "0.4-0.6",
        },
    ]
    rows_b = [
        {
            "seed": 1,
            "shared_interest_score": 0.2,
            "transcript_char_count": 110,
            "similarity_bin": "0.2-0.4",
        },
        {
            "seed": 2,
            "shared_interest_score": 0.4,
            "transcript_char_count": 130,
            "similarity_bin": "0.4-0.6",
        },
    ]
    _write_csv(sweep_a / "similarity_sweep_results.csv", rows_a)
    _write_csv(sweep_b / "similarity_sweep_results.csv", rows_b)

    summary_a = [
        {"similarity_bin": "0.2-0.4", "count": 1, "avg_transcript_char_count": 100},
        {"similarity_bin": "0.4-0.6", "count": 1, "avg_transcript_char_count": 120},
    ]
    summary_b = [
        {"similarity_bin": "0.2-0.4", "count": 1, "avg_transcript_char_count": 110},
        {"similarity_bin": "0.4-0.6", "count": 1, "avg_transcript_char_count": 130},
    ]
    (sweep_a / "similarity_bin_summary.json").write_text(json.dumps(summary_a), encoding="utf-8")
    (sweep_b / "similarity_bin_summary.json").write_text(json.dumps(summary_b), encoding="utf-8")

    out_dir = compare_sweeps(
        sweep_a=sweep_a,
        sweep_b=sweep_b,
        label_a="hosted",
        label_b="hpc",
        output_root=tmp_path / "out",
        run_id="cmp_01",
    )

    report_path = out_dir / "comparison_report.json"
    summary_path = out_dir / "comparison_summary.txt"
    assert report_path.exists()
    assert summary_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["labels"]["a"] == "hosted"
    assert report["labels"]["b"] == "hpc"
    assert report["row_counts"]["a"] == 2
    assert report["row_counts"]["b"] == 2

    delta = report["column_deltas"]["transcript_char_count"]["delta_mean_b_minus_a"]
    assert delta == 10.0


def test_compare_sweeps_hpc_dir_hint_when_sweep_artifacts_missing(tmp_path):
    sweep_a = tmp_path / "run_1"
    sweep_b = tmp_path / "run_2"
    sweep_a.mkdir(parents=True, exist_ok=True)
    sweep_b.mkdir(parents=True, exist_ok=True)

    # Mimic HPC run folder structure that users often pass by mistake.
    (sweep_a / "clients").mkdir()
    (sweep_b / "clients").mkdir()
    (sweep_a / "launcher_summary.log").write_text("job summary", encoding="utf-8")
    (sweep_b / "launcher_summary.log").write_text("job summary", encoding="utf-8")

    with pytest.raises(FileNotFoundError, match="compare-hpc-chat-runs"):
        compare_sweeps(sweep_a=sweep_a, sweep_b=sweep_b)

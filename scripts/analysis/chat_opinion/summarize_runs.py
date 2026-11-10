#!/usr/bin/env python3
"""Summarize chat_opinion run metadata for quick calibration checks."""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path


def parse_cli_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize chat_opinion run metadata and outcome ranges."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("data/output/examples/chat_opinion"),
        help="Directory containing run folders.",
    )
    parser.add_argument(
        "--run-id",
        action="append",
        default=[],
        help="Run folder name to include. May be supplied multiple times.",
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default=None,
        help="Optional prefix filter for run folder names.",
    )
    return parser.parse_args(argv)


def _discover_run_dirs(root: Path, run_ids: list[str], prefix: str | None) -> list[Path]:
    if run_ids:
        return [root / run_id for run_id in run_ids]

    run_dirs = [
        entry for entry in sorted(root.iterdir())
        if entry.is_dir() and (entry / "run_metadata.json").exists()
    ]
    if prefix is not None:
        run_dirs = [entry for entry in run_dirs if entry.name.startswith(prefix)]
    return run_dirs


def summarize_runs(root: Path, run_ids: list[str] | None = None, prefix: str | None = None) -> dict:
    run_ids = run_ids or []
    root = root.resolve()
    run_dirs = _discover_run_dirs(root, run_ids, prefix)

    rows: list[dict] = []
    for run_dir in run_dirs:
        metadata_path = run_dir / "run_metadata.json"
        if not metadata_path.exists():
            raise FileNotFoundError(f"Missing run metadata: {metadata_path}")

        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        rows.append(
            {
                "run_id": run_dir.name,
                "seed": metadata.get("seed"),
                "conversation_mode": metadata.get("conversation_mode"),
                "pairing_strategy": metadata.get("pairing_strategy"),
                "initial_mean_opinion": metadata.get("initial_mean_opinion"),
                "final_mean_opinion": metadata.get("final_mean_opinion"),
                "delta_mean_opinion": metadata.get("delta_mean_opinion"),
                "final_opinion_gap": metadata.get("final_opinion_gap"),
                "pair_dissimilarity_score": metadata.get("pair_dissimilarity_score"),
                "awkward_marker_count": metadata.get("awkward_marker_count"),
                "disagreement_marker_count": metadata.get("disagreement_marker_count"),
            }
        )

    summary: dict[str, object] = {"root": str(root), "n_runs": len(rows), "rows": rows}
    if rows:
        final_means = [float(row["final_mean_opinion"]) for row in rows]
        deltas = [float(row["delta_mean_opinion"]) for row in rows]
        final_gaps = [float(row["final_opinion_gap"]) for row in rows]
        summary["ranges"] = {
            "final_mean_opinion": [round(min(final_means), 4), round(max(final_means), 4)],
            "delta_mean_opinion": [round(min(deltas), 4), round(max(deltas), 4)],
            "final_opinion_gap": [round(min(final_gaps), 4), round(max(final_gaps), 4)],
        }
        summary["stats"] = {
            "final_mean_opinion": {
                "mean": round(statistics.fmean(final_means), 4),
                "stddev": round(statistics.pstdev(final_means), 4),
            },
            "delta_mean_opinion": {
                "mean": round(statistics.fmean(deltas), 4),
                "stddev": round(statistics.pstdev(deltas), 4),
            },
            "final_opinion_gap": {
                "mean": round(statistics.fmean(final_gaps), 4),
                "stddev": round(statistics.pstdev(final_gaps), 4),
            },
        }
    return summary


def _format_row(row: dict) -> str:
    return (
        f"{row['run_id']}: seed={row['seed']} mode={row['conversation_mode']} "
        f"pair={row['pairing_strategy']} initial={row['initial_mean_opinion']} "
        f"final={row['final_mean_opinion']} "
        f"delta={row['delta_mean_opinion']} "
        f"gap={row['final_opinion_gap']} dissim={row['pair_dissimilarity_score']} "
        f"awk={row['awkward_marker_count']} disagr={row['disagreement_marker_count']}"
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_cli_args(argv)
    summary = summarize_runs(args.root, args.run_id, args.prefix)

    print(f"root={summary['root']}")
    print(f"n_runs={summary['n_runs']}")
    for row in summary["rows"]:
        print(_format_row(row))

    ranges = summary.get("ranges")
    if ranges:
        print("ranges:")
        print(f"  final_mean_opinion={ranges['final_mean_opinion'][0]}..{ranges['final_mean_opinion'][1]}")
        print(f"  delta_mean_opinion={ranges['delta_mean_opinion'][0]}..{ranges['delta_mean_opinion'][1]}")
        print(f"  final_opinion_gap={ranges['final_opinion_gap'][0]}..{ranges['final_opinion_gap'][1]}")
    stats = summary.get("stats")
    if stats:
        print("stats:")
        print(
            "  final_mean_opinion mean/stddev="
            f"{stats['final_mean_opinion']['mean']}/"
            f"{stats['final_mean_opinion']['stddev']}"
        )
        print(
            "  delta_mean_opinion mean/stddev="
            f"{stats['delta_mean_opinion']['mean']}/"
            f"{stats['delta_mean_opinion']['stddev']}"
        )
        print(
            "  final_opinion_gap mean/stddev="
            f"{stats['final_opinion_gap']['mean']}/"
            f"{stats['final_opinion_gap']['stddev']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

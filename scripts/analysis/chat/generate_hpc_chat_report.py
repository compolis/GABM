#!/usr/bin/env python3
"""Generate a Markdown report for Calder/HPC chat run comparisons.

This utility combines:
- pairwise reproducibility comparisons (transcript/metadata/cache)
- launcher summary extraction for concurrency/failed-run context

It is intended to make reproducibility updates easy to regenerate from a set of
run directories or job IDs.
"""

from __future__ import annotations

# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

import argparse
from datetime import datetime, timezone
from itertools import combinations
import re
from pathlib import Path

from compare_chat_runs import (
    discover_runs,
    load_normalized_metadata,
    resolve_run_path,
    sha256_of_file,
)
from generate_concurrency_rows import extract_error_pattern, parse_launcher_summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a Markdown report with pairwise reproducibility comparison "
            "results and launcher concurrency summaries."
        )
    )
    parser.add_argument("--job-id", action="append", default=[], help="Job ID to include (repeatable).")
    parser.add_argument("--run", action="append", default=[], help="Run path or run_<id> (repeatable).")
    parser.add_argument(
        "--pair",
        action="append",
        default=[],
        help=(
            "Explicit pair to compare in the form A,B. A and B may be job IDs, "
            "run_<id> values, or paths. Repeatable."
        ),
    )
    parser.add_argument(
        "--working-dir",
        default=f"/flash-calder/users/{Path.home().name}/gabm",
        help="Base working directory used for job-id/run-name resolution.",
    )
    parser.add_argument(
        "--title",
        default="Calder HPC Chat Reproducibility Report",
        help="Markdown H1 title for the generated report.",
    )
    parser.add_argument(
        "--output",
        help="Write markdown to this file path. If omitted, prints to stdout.",
    )
    return parser.parse_args()


def _job_id_from_path(run_dir: Path) -> str:
    name = run_dir.name
    if name.startswith("run_"):
        return name.removeprefix("run_")
    return name


def _safe_cell(value: str) -> str:
    return str(value).replace("|", "\\|")


def _build_input_run_list(args: argparse.Namespace) -> list[Path]:
    raw_values = [*args.job_id, *args.run]
    if not raw_values:
        raise ValueError("Provide at least one --job-id or --run input.")

    run_dirs: list[Path] = []
    for value in raw_values:
        run_dirs.append(resolve_run_path(value, args.working_dir))

    # Deduplicate while preserving order.
    deduped: list[Path] = []
    seen: set[Path] = set()
    for run_dir in run_dirs:
        if run_dir in seen:
            continue
        deduped.append(run_dir)
        seen.add(run_dir)
    return deduped


def _compute_pair_summary(run_a: Path, run_b: Path) -> dict[str, str | int]:
    _, a_runs = discover_runs(run_a)
    _, b_runs = discover_runs(run_b)
    shared_keys = sorted(set(a_runs) & set(b_runs))

    transcript_equal = 0
    metadata_equal = 0
    cache_equal = 0
    cache_available = 0

    for key in shared_keys:
        a = a_runs[key]
        b = b_runs[key]

        if sha256_of_file(a["transcript"]) == sha256_of_file(b["transcript"]):
            transcript_equal += 1

        if load_normalized_metadata(a["metadata"]) == load_normalized_metadata(b["metadata"]):
            metadata_equal += 1

        a_cache = a["cache_delta"]
        b_cache = b["cache_delta"]
        if a_cache.exists() and b_cache.exists():
            cache_available += 1
            if sha256_of_file(a_cache) == sha256_of_file(b_cache):
                cache_equal += 1

    cache_cell = f"{cache_equal}/{cache_available}" if cache_available > 0 else "n/a"
    determinism_signal = "all_match" if shared_keys and transcript_equal == len(shared_keys) else "differ"
    if not shared_keys:
        determinism_signal = "inconclusive_no_shared_run_ids"

    return {
        "a_job": _job_id_from_path(run_a),
        "b_job": _job_id_from_path(run_b),
        "shared": len(shared_keys),
        "transcript": f"{transcript_equal}/{len(shared_keys)}",
        "metadata": f"{metadata_equal}/{len(shared_keys)}",
        "cache": cache_cell,
        "signal": determinism_signal,
    }


def _resolve_explicit_pairs(args: argparse.Namespace) -> list[tuple[Path, Path]]:
    pairs: list[tuple[Path, Path]] = []
    for raw_pair in args.pair:
        chunks = [c.strip() for c in raw_pair.split(",", maxsplit=1)]
        if len(chunks) != 2 or not chunks[0] or not chunks[1]:
            raise ValueError(f"Invalid --pair value '{raw_pair}'. Expected format: A,B")
        run_a = resolve_run_path(chunks[0], args.working_dir)
        run_b = resolve_run_path(chunks[1], args.working_dir)
        pairs.append((run_a, run_b))
    return pairs


def _run_manifest_rows(run_dirs: list[Path]) -> list[str]:
    rows: list[str] = []
    for run_dir in run_dirs:
        summary_path = run_dir / "launcher_summary.log"
        if summary_path.is_file():
            summary = parse_launcher_summary(summary_path)
            seed_mode = summary.get("SEED_MODE", "?")
            concurrency = summary.get("CONCURRENCY", "?")
            n_runs = summary.get("N_RUNS", "?")
            successful = summary.get("SUCCESSFUL_RUNS", "?")
            failed = summary.get("FAILED_RUNS", "?")
        else:
            seed_mode = concurrency = n_runs = successful = failed = "n/a"
        rows.append(
            "| {job} | `{path}` | {seed_mode} | {concurrency} | {n_runs} | {successful} | {failed} |".format(
                job=_safe_cell(_job_id_from_path(run_dir)),
                path=_safe_cell(str(run_dir)),
                seed_mode=_safe_cell(seed_mode),
                concurrency=_safe_cell(concurrency),
                n_runs=_safe_cell(n_runs),
                successful=_safe_cell(successful),
                failed=_safe_cell(failed),
            )
        )
    return rows


def _concurrency_rows(run_dirs: list[Path]) -> list[str]:
    rows: list[str] = []
    for run_dir in run_dirs:
        summary_path = run_dir / "launcher_summary.log"
        if not summary_path.is_file():
            rows.append(
                f"| {_safe_cell(_job_id_from_path(run_dir))} | n/a | n/a | n/a | n/a | n/a | launcher_summary_missing |"
            )
            continue

        summary = parse_launcher_summary(summary_path)
        failed = summary.get("FAILED_RUNS", "?")
        error_pattern = extract_error_pattern(run_dir, failed)
        rows.append(
            "| {job} | {concurrency} | {n_runs} | {successful} | {failed} | n/a | {error_pattern} |".format(
                job=_safe_cell(_job_id_from_path(run_dir)),
                concurrency=_safe_cell(summary.get("CONCURRENCY", "?")),
                n_runs=_safe_cell(summary.get("N_RUNS", "?")),
                successful=_safe_cell(summary.get("SUCCESSFUL_RUNS", "?")),
                failed=_safe_cell(failed),
                error_pattern=_safe_cell(error_pattern),
            )
        )
    return rows


def _format_markdown(
    *,
    title: str,
    run_dirs: list[Path],
    pair_summaries: list[dict[str, str | int]],
) -> str:
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"_Generated: {generated_at} (UTC)_")
    lines.append("")
    lines.append("## Runs included")
    lines.append("")
    lines.append("| Job ID | Run path | Seed mode | Concurrency | N runs | Successful runs | Failed runs |")
    lines.append("|---:|---|---|---:|---:|---:|---:|")
    lines.extend(_run_manifest_rows(run_dirs))
    lines.append("")
    lines.append("## Pairwise comparison summary")
    lines.append("")
    lines.append("| A job | B job | Shared run IDs | Transcript exact matches | Metadata core matches | Cache-delta exact matches | Determinism signal |")
    lines.append("|---|---|---:|---:|---:|---:|---|")
    for item in pair_summaries:
        lines.append(
            "| {a_job} | {b_job} | {shared} | {transcript} | {metadata} | {cache} | {signal} |".format(
                a_job=_safe_cell(str(item["a_job"])),
                b_job=_safe_cell(str(item["b_job"])),
                shared=item["shared"],
                transcript=_safe_cell(str(item["transcript"])),
                metadata=_safe_cell(str(item["metadata"])),
                cache=_safe_cell(str(item["cache"])),
                signal=_safe_cell(str(item["signal"])),
            )
        )
    lines.append("")
    lines.append("## Concurrency/stress summary")
    lines.append("")
    lines.append("| Job ID | Concurrency | N runs | Successful runs | Failed runs | Mean runtime per run (if measured) | Error pattern |")
    lines.append("|---:|---:|---:|---:|---:|---|---|")
    lines.extend(_concurrency_rows(run_dirs))
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()

    try:
        run_dirs = _build_input_run_list(args)
        explicit_pairs = _resolve_explicit_pairs(args)
    except (FileNotFoundError, ValueError) as err:
        print(str(err))
        return 1

    if explicit_pairs:
        pairs = explicit_pairs
    else:
        pairs = list(combinations(run_dirs, 2))

    pair_summaries = [_compute_pair_summary(run_a, run_b) for run_a, run_b in pairs]

    markdown = _format_markdown(
        title=args.title,
        run_dirs=run_dirs,
        pair_summaries=pair_summaries,
    )

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
        print(f"Wrote report to: {output_path}")
    else:
        print(markdown)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

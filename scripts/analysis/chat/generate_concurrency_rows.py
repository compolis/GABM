#!/usr/bin/env python3
"""Generate markdown rows for concurrency/stress summaries.

Reads Calder launcher_summary.log outputs and prints markdown rows suitable for
documentation/reproducibility/REPRODUCIBILITY_QWEN3_14B.md.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate markdown table rows from run launcher summaries for "
            "reproducibility notes."
        )
    )
    parser.add_argument("--job-id", action="append", default=[], help="Slurm job ID (repeatable).")
    parser.add_argument("--run", action="append", default=[], help="Run path or run_<id> (repeatable).")
    parser.add_argument(
        "--working-dir",
        default=f"/flash-calder/users/{Path.home().name}/gabm",
        help="Base working directory used for job-id/run-name resolution.",
    )
    parser.add_argument("--header", action="store_true", help="Print markdown header before rows.")
    return parser.parse_args()


def resolve_run_dir(value: str, working_dir: str) -> Path:
    raw = Path(value)
    if raw.is_dir():
        candidate = raw
    elif value.startswith("run_") and value[4:].isdigit():
        candidate = Path(working_dir) / "gabm_runs" / value
    elif value.isdigit():
        candidate = Path(working_dir) / "gabm_runs" / f"run_{value}"
    else:
        candidate = raw

    if not candidate.is_dir():
        raise FileNotFoundError(f"Run directory not found: {candidate}")
    return candidate.resolve()


def parse_launcher_summary(summary_path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in summary_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip()
    return data


def extract_error_pattern(run_dir: Path, failed: str) -> str:
    if failed == "0":
        return "none"

    clients_dir = run_dir / "clients"
    if not clients_dir.is_dir():
        return "see logs"

    pattern = re.compile(r"Traceback|Exception|ERROR|RuntimeError|ConnectionError|timed out", re.IGNORECASE)

    for log_file in sorted(clients_dir.glob("*.log")):
        with log_file.open("r", encoding="utf-8", errors="replace") as handle:
            for idx, line in enumerate(handle, start=1):
                if pattern.search(line):
                    msg = f"{log_file.name}:{idx}:{line.strip()}"
                    return msg.replace("|", "\\|")

    return "failed_workers_no_signature"


def main() -> int:
    args = parse_args()

    if not args.job_id and not args.run:
        print("Provide at least one --job-id or --run input.", file=sys.stderr)
        return 1

    run_dirs: list[Path] = []
    try:
        run_dirs.extend(resolve_run_dir(job_id, args.working_dir) for job_id in args.job_id)
        run_dirs.extend(resolve_run_dir(run_input, args.working_dir) for run_input in args.run)
    except FileNotFoundError as err:
        print(str(err), file=sys.stderr)
        return 1

    if args.header:
        print("| Job ID | Concurrency | N runs | Successful runs | Failed runs | Mean runtime per run (if measured) | Error pattern |")
        print("|---:|---:|---:|---:|---:|---|---|")

    for run_dir in run_dirs:
        summary_path = run_dir / "launcher_summary.log"
        if not summary_path.is_file():
            print(f"Missing launcher summary: {summary_path}", file=sys.stderr)
            return 1

        summary = parse_launcher_summary(summary_path)
        job_id = run_dir.name.removeprefix("run_") if run_dir.name.startswith("run_") else run_dir.name

        concurrency = summary.get("CONCURRENCY", "?")
        n_runs = summary.get("N_RUNS", "?")
        successful = summary.get("SUCCESSFUL_RUNS", "?")
        failed = summary.get("FAILED_RUNS", "?")

        mean_runtime = "n/a"  # Not currently emitted by launcher logs.
        error_pattern = extract_error_pattern(run_dir, failed)

        print(
            f"| {job_id} | {concurrency} | {n_runs} | {successful} | {failed} | "
            f"{mean_runtime} | {error_pattern} |"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

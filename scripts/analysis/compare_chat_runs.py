#!/usr/bin/env python3
"""Compare two GABM chat run outputs and report reproducibility signals.

This utility supports run path inputs from local output folders or HPC work dirs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

VOLATILE_METADATA_KEYS = {
    "created_at",
    "run_dir",
    "cache_jsonl_path",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare two run directories by transcript/cache hash and normalized "
            "metadata equality."
        )
    )
    parser.add_argument("--run-a", required=True, help="First run identifier/path.")
    parser.add_argument("--run-b", required=True, help="Second run identifier/path.")
    parser.add_argument(
        "--working-dir",
        default=f"/flash-calder/users/{Path.home().name}/gabm",
        help="Base working directory used for job-id/run-name resolution.",
    )
    return parser.parse_args()


def resolve_run_path(value: str, working_dir: str) -> Path:
    candidate: Path
    raw = Path(value)
    if raw.is_dir():
        candidate = raw
    elif value.isdigit():
        candidate = Path(working_dir) / "gabm_runs" / f"run_{value}"
    elif value.startswith("run_") and value[4:].isdigit():
        candidate = Path(working_dir) / "gabm_runs" / value
    else:
        candidate = raw

    if not candidate.is_dir():
        raise FileNotFoundError(f"Run directory not found: {candidate}")
    return candidate.resolve()


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_normalized_metadata(path: Path) -> Any:
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return data
    return {k: v for k, v in sorted(data.items()) if k not in VOLATILE_METADATA_KEYS}


def discover_runs(root: Path) -> tuple[Path, dict[str, dict[str, Path]]]:
    # Concurrency launcher outputs to <run>/clients/<run_id>/..., while older runs
    # can write directly under <run>/<run_id>/....
    base = root / "clients" if (root / "clients").is_dir() else root
    found: dict[str, dict[str, Path]] = {}

    for transcript in sorted(base.rglob("conversation_transcript.txt")):
        run_dir = transcript.parent
        key = run_dir.relative_to(base).as_posix()
        found[key] = {
            "run_dir": run_dir,
            "transcript": transcript,
            "metadata": run_dir / "run_metadata.json",
            "cache_delta": run_dir / "prompt_response_cache_delta.jsonl",
        }

    return base, found


def main() -> int:
    args = parse_args()

    try:
        run_a = resolve_run_path(args.run_a, args.working_dir)
        run_b = resolve_run_path(args.run_b, args.working_dir)
    except FileNotFoundError as err:
        print(str(err), file=sys.stderr)
        return 1

    print("Comparing runs:")
    print(f"  A: {run_a}")
    print(f"  B: {run_b}")

    a_base, a_runs = discover_runs(run_a)
    b_base, b_runs = discover_runs(run_b)

    if not a_runs:
        print(f"No run artifacts found under A base: {a_base}")
        return 2
    if not b_runs:
        print(f"No run artifacts found under B base: {b_base}")
        return 2

    shared_keys = sorted(set(a_runs) & set(b_runs))
    only_a = sorted(set(a_runs) - set(b_runs))
    only_b = sorted(set(b_runs) - set(a_runs))

    print("\nDiscovery summary")
    print(f"  A run count: {len(a_runs)}")
    print(f"  B run count: {len(b_runs)}")
    print(f"  Shared run IDs: {len(shared_keys)}")
    print(f"  Only in A: {len(only_a)}")
    print(f"  Only in B: {len(only_b)}")

    if only_a:
        print("\nRun IDs only in A:")
        for key in only_a:
            print(f"  - {key}")

    if only_b:
        print("\nRun IDs only in B:")
        for key in only_b:
            print(f"  - {key}")

    transcript_equal = 0
    metadata_equal = 0
    cache_equal = 0
    cache_na = 0

    transcript_mismatches: list[str] = []
    metadata_mismatches: list[str] = []
    cache_mismatches: list[str] = []

    for key in shared_keys:
        a = a_runs[key]
        b = b_runs[key]

        if sha256_of_file(a["transcript"]) == sha256_of_file(b["transcript"]):
            transcript_equal += 1
        else:
            transcript_mismatches.append(key)

        if load_normalized_metadata(a["metadata"]) == load_normalized_metadata(b["metadata"]):
            metadata_equal += 1
        else:
            metadata_mismatches.append(key)

        a_cache = a["cache_delta"]
        b_cache = b["cache_delta"]
        if a_cache.exists() and b_cache.exists():
            if sha256_of_file(a_cache) == sha256_of_file(b_cache):
                cache_equal += 1
            else:
                cache_mismatches.append(key)
        else:
            cache_na += 1

    print("\nComparison summary (shared run IDs)")
    print(f"  Transcript exact matches: {transcript_equal}/{len(shared_keys)}")
    print(f"  Metadata core matches: {metadata_equal}/{len(shared_keys)}")
    if len(shared_keys) - cache_na > 0:
        print(f"  Cache delta exact matches: {cache_equal}/{len(shared_keys) - cache_na}")
    else:
        print("  Cache delta exact matches: n/a")

    if transcript_mismatches:
        print("\nTranscript mismatches:")
        for key in transcript_mismatches:
            print(f"  - {key}")

    if metadata_mismatches:
        print("\nMetadata mismatches (after volatile-key filtering):")
        for key in metadata_mismatches:
            print(f"  - {key}")

    if cache_mismatches:
        print("\nCache-delta mismatches:")
        for key in cache_mismatches:
            print(f"  - {key}")

    if shared_keys and transcript_equal == len(shared_keys):
        print("\nDeterminism signal: all shared transcripts match exactly.")
        return 0

    if not shared_keys:
        print("\nDeterminism signal: inconclusive (no shared run IDs to compare).")
        return 3

    print("\nDeterminism signal: one or more shared transcripts differ.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

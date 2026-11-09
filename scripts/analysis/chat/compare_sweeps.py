"""Compare two ensemble sweep directories and summarize metric differences."""

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path

_DEFAULT_OUTPUT_ROOT = Path("data/output/examples/ensembles/compare")


def parse_cli_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two ensemble sweep result directories.")
    parser.add_argument("--sweep-a", type=Path, required=True, help="Path to first sweep directory.")
    parser.add_argument("--sweep-b", type=Path, required=True, help="Path to second sweep directory.")
    parser.add_argument("--label-a", type=str, default="sweep_a")
    parser.add_argument("--label-b", type=str, default="sweep_b")
    parser.add_argument("--output-root", type=Path, default=_DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--run-id", type=str, default=None)
    return parser.parse_args(argv)


def _to_float(value) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        candidate = value.strip()
        if not candidate:
            return None
        try:
            return float(candidate)
        except ValueError:
            return None
    return None


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


def _std(values: list[float], mean_value: float) -> float:
    if len(values) < 2:
        return 0.0
    variance = sum((value - mean_value) ** 2 for value in values) / len(values)
    return math.sqrt(variance)


def _load_csv_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _load_bin_summary(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def _find_numeric_columns(rows: list[dict]) -> set[str]:
    if not rows:
        return set()

    all_keys = set(rows[0].keys())
    numeric_columns = set()
    for key in all_keys:
        values = [row.get(key) for row in rows]
        float_values = [_to_float(value) for value in values]
        if all(value is not None for value in float_values):
            numeric_columns.add(key)
    return numeric_columns


def _numeric_series(rows: list[dict], key: str) -> list[float]:
    series = []
    for row in rows:
        value = _to_float(row.get(key))
        if value is not None:
            series.append(value)
    return series


def _compute_column_stats(rows: list[dict], columns: set[str]) -> dict[str, dict]:
    stats = {}
    for column in sorted(columns):
        series = _numeric_series(rows, column)
        if not series:
            continue
        mean_value = _mean(series)
        stats[column] = {
            "mean": round(mean_value, 6),
            "std": round(_std(series, mean_value), 6),
            "min": round(min(series), 6),
            "max": round(max(series), 6),
        }
    return stats


def _index_bin_summary(summary_rows: list[dict]) -> dict[str, dict]:
    result = {}
    for row in summary_rows:
        bin_name = str(row.get("similarity_bin", "")).strip()
        if bin_name:
            result[bin_name] = row
    return result


def _compute_bin_comparison(summary_a: list[dict], summary_b: list[dict]) -> dict[str, dict]:
    by_bin_a = _index_bin_summary(summary_a)
    by_bin_b = _index_bin_summary(summary_b)
    all_bins = sorted(set(by_bin_a.keys()) | set(by_bin_b.keys()))

    comparison = {}
    for bin_name in all_bins:
        row_a = by_bin_a.get(bin_name, {})
        row_b = by_bin_b.get(bin_name, {})
        metric_keys = sorted((set(row_a.keys()) | set(row_b.keys())) - {"similarity_bin"})

        metric_deltas = {}
        for key in metric_keys:
            a_value = _to_float(row_a.get(key))
            b_value = _to_float(row_b.get(key))
            if a_value is None or b_value is None:
                metric_deltas[key] = {"a": a_value, "b": b_value, "delta_b_minus_a": None}
            else:
                metric_deltas[key] = {
                    "a": round(a_value, 6),
                    "b": round(b_value, 6),
                    "delta_b_minus_a": round(b_value - a_value, 6),
                }

        comparison[bin_name] = metric_deltas

    return comparison


def _safe_slug(text: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in text.strip())
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    return cleaned.strip("_") or "sweep"


def _looks_like_hpc_chat_run(path: Path) -> bool:
    probe_names = {
        "clients",
        "launcher_summary.log",
        "gpu_memory.log",
        "vllm_server.log",
    }
    return any((path / name).exists() for name in probe_names)


def compare_sweeps(
    sweep_a: Path,
    sweep_b: Path,
    label_a: str = "sweep_a",
    label_b: str = "sweep_b",
    output_root: Path | None = None,
    run_id: str | None = None,
):
    csv_a = Path(sweep_a) / "similarity_sweep_results.csv"
    csv_b = Path(sweep_b) / "similarity_sweep_results.csv"
    summary_a = Path(sweep_a) / "similarity_bin_summary.json"
    summary_b = Path(sweep_b) / "similarity_bin_summary.json"

    missing = [path for path in [csv_a, csv_b, summary_a, summary_b] if not path.exists()]
    if missing:
        missing_text = ", ".join(str(path) for path in missing)
        extra_hint = ""
        if _looks_like_hpc_chat_run(Path(sweep_a)) or _looks_like_hpc_chat_run(Path(sweep_b)):
            extra_hint = (
                " Detected HPC chat-run style directories. "
                "For those outputs use: make compare-hpc-chat-runs RUN_A=<run|id|path> RUN_B=<run|id|path>."
            )
        raise FileNotFoundError(f"Missing required sweep artifact(s): {missing_text}.{extra_hint}")

    rows_a = _load_csv_rows(csv_a)
    rows_b = _load_csv_rows(csv_b)
    summary_rows_a = _load_bin_summary(summary_a)
    summary_rows_b = _load_bin_summary(summary_b)

    numeric_columns_a = _find_numeric_columns(rows_a)
    numeric_columns_b = _find_numeric_columns(rows_b)
    common_numeric_columns = sorted(numeric_columns_a & numeric_columns_b)

    stats_a = _compute_column_stats(rows_a, set(common_numeric_columns))
    stats_b = _compute_column_stats(rows_b, set(common_numeric_columns))

    column_deltas = {}
    for column in common_numeric_columns:
        a_mean = stats_a.get(column, {}).get("mean")
        b_mean = stats_b.get(column, {}).get("mean")
        if a_mean is None or b_mean is None:
            continue
        column_deltas[column] = {
            "mean_a": a_mean,
            "mean_b": b_mean,
            "delta_mean_b_minus_a": round(b_mean - a_mean, 6),
            "std_a": stats_a[column]["std"],
            "std_b": stats_b[column]["std"],
            "delta_std_b_minus_a": round(stats_b[column]["std"] - stats_a[column]["std"], 6),
        }

    report = {
        "labels": {"a": label_a, "b": label_b},
        "inputs": {"sweep_a": str(sweep_a), "sweep_b": str(sweep_b)},
        "row_counts": {"a": len(rows_a), "b": len(rows_b), "delta_b_minus_a": len(rows_b) - len(rows_a)},
        "common_numeric_columns": common_numeric_columns,
        "column_deltas": column_deltas,
        "bin_comparison": _compute_bin_comparison(summary_rows_a, summary_rows_b),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }

    root = Path(output_root) if output_root is not None else _DEFAULT_OUTPUT_ROOT
    comparison_name = run_id or f"compare_{_safe_slug(label_a)}_vs_{_safe_slug(label_b)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    out_dir = root / comparison_name
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "comparison_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        f"Compare Ensembles: {label_a} vs {label_b}",
        f"Sweep A: {sweep_a}",
        f"Sweep B: {sweep_b}",
        f"Rows: A={len(rows_a)}, B={len(rows_b)}, delta={len(rows_b) - len(rows_a)}",
        "",
        "Mean deltas (B - A):",
    ]
    for column in common_numeric_columns:
        delta = column_deltas.get(column)
        if delta is None:
            continue
        lines.append(f"- {column}: {delta['delta_mean_b_minus_a']}")

    (out_dir / "comparison_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_dir


if __name__ == "__main__":
    args = parse_cli_args()
    compare_sweeps(
        sweep_a=args.sweep_a,
        sweep_b=args.sweep_b,
        label_a=args.label_a,
        label_b=args.label_b,
        output_root=args.output_root,
        run_id=args.run_id,
    )

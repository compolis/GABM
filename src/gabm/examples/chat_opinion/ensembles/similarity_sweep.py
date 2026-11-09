"""Ensemble runner for chat-opinion similarity sweeps."""

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

from gabm.examples.chat_opinion.sim import run as run_chat_opinion
from gabm.examples.chat.sim import (
    build_llm_service,
    resolve_llm_api_key,
    resolve_llm_model,
    resolve_llm_seed,
    resolve_llm_service_name,
)

_DEFAULT_OUTPUT_ROOT = Path("data/output/examples/chat_opinion/ensembles")


def parse_cli_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run an ensemble similarity sweep for chat_opinion example.")
    parser.add_argument("--start-seed", type=int, default=100)
    parser.add_argument("--n-runs", type=int, default=25)
    parser.add_argument("--rounds", type=int, default=8)
    parser.add_argument("--year", type=int, default=2026)
    parser.add_argument("--output-root", type=Path, default=_DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--run-id", type=str, default=None)
    parser.add_argument("--llm-service", type=str, default=None)
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--llm-seed", type=int, default=None)
    parser.add_argument("--api-key", type=str, default=None)
    parser.add_argument("--api-key-file", type=Path, default=Path("data/api_key.csv"))
    parser.add_argument("--ons-male-file", type=Path, default=None)
    parser.add_argument("--ons-female-file", type=Path, default=None)
    parser.add_argument("--conversation-mode", type=str, choices=["normal", "awkward"], default="normal")
    parser.add_argument("--pairing-strategy", type=str, choices=["random", "max_dissimilarity"], default="random")
    parser.add_argument("--candidate-pool-size", type=int, default=8)
    parser.add_argument("--no-cache", action="store_true")
    return parser.parse_args(argv)


def _similarity_bin(score: float) -> str:
    if score < 0.2:
        return "0.0-0.2"
    if score < 0.4:
        return "0.2-0.4"
    if score < 0.6:
        return "0.4-0.6"
    if score < 0.8:
        return "0.6-0.8"
    return "0.8-1.0"


def _write_scatter_plot(path: Path, rows: list[dict]):
    plt.figure(figsize=(8, 4.8))
    x = [row["pair_similarity_score"] for row in rows]
    y = [row["final_mean_opinion"] for row in rows]
    plt.scatter(x, y, alpha=0.75)
    plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    plt.xlabel("Pair similarity score")
    plt.ylabel("Final mean opinion")
    plt.title("Similarity vs final mean opinion")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def run_sweep(
    start_seed: int = 100,
    n_runs: int = 25,
    rounds: int = 8,
    year: int = 2026,
    output_root: Path | None = None,
    run_id: str | None = None,
    llm_service=None,
    api_key: str | None = None,
    model: str | None = None,
    llm_seed: int | None = None,
    ons_male_file: Path | None = None,
    ons_female_file: Path | None = None,
    conversation_mode: str = "normal",
    pairing_strategy: str = "random",
    candidate_pool_size: int = 8,
):
    if n_runs < 1:
        raise ValueError("n_runs must be >= 1")

    root = Path(output_root) if output_root is not None else _DEFAULT_OUTPUT_ROOT
    sweep_name = run_id or f"sweep_{datetime.now().strftime('%Y%m%d_%H%M%S')}_seed{start_seed}_n{n_runs}"
    sweep_dir = root / sweep_name
    runs_dir = sweep_dir / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    for index in range(n_runs):
        seed = start_seed + index
        run_dir = run_chat_opinion(
            seed=seed,
            year=year,
            rounds=rounds,
            llm_service=llm_service,
            api_key=api_key,
            model=model,
            llm_seed=llm_seed,
            ons_male_file=ons_male_file,
            ons_female_file=ons_female_file,
            output_root=runs_dir,
            run_id=f"seed{seed}",
            emit_console_output=False,
            conversation_mode=conversation_mode,
            pairing_strategy=pairing_strategy,
            candidate_pool_size=candidate_pool_size,
        )

        metadata = json.loads((run_dir / "run_metadata.json").read_text(encoding="utf-8"))
        opinion_history = json.loads((run_dir / "opinion_history.json").read_text(encoding="utf-8"))

        initial_mean = (opinion_history["opinion_a_about_b"][0] + opinion_history["opinion_b_about_a"][0]) / 2.0
        final_mean = (opinion_history["opinion_a_about_b"][-1] + opinion_history["opinion_b_about_a"][-1]) / 2.0
        final_gap = abs(opinion_history["opinion_a_about_b"][-1] - opinion_history["opinion_b_about_a"][-1])

        score = float(metadata.get("pair_similarity_score", metadata.get("shared_interest_score", 0.0)))
        components = metadata.get("pair_similarity_components", {})
        row = {
            "seed": seed,
            "run_dir": str(run_dir),
            "pair_similarity_score": round(score, 4),
            "pair_dissimilarity_score": round(float(metadata.get("pair_dissimilarity_score", 0.0)), 4),
            "age_similarity": round(float(components.get("age_similarity", 0.0)), 4),
            "gender_similarity": round(float(components.get("gender_similarity", 0.0)), 4),
            "interest_similarity": round(float(components.get("interest_similarity", metadata.get("shared_interest_score", 0.0))), 4),
            "first_shared_interest_round": int(metadata["first_shared_interest_round"]) if metadata.get("first_shared_interest_round") is not None else -1,
            "awkward_marker_count": int(metadata.get("awkward_marker_count", 0)),
            "disagreement_marker_count": int(metadata.get("disagreement_marker_count", 0)),
            "initial_mean_opinion": round(initial_mean, 4),
            "final_mean_opinion": round(final_mean, 4),
            "delta_mean_opinion": round(final_mean - initial_mean, 4),
            "final_opinion_gap": round(final_gap, 4),
            "conversation_mode": str(metadata.get("conversation_mode", conversation_mode)),
            "pairing_strategy": str(metadata.get("pairing_strategy", pairing_strategy)),
            "similarity_bin": _similarity_bin(score),
        }
        rows.append(row)

    csv_path = sweep_dir / "similarity_sweep_results.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    grouped = defaultdict(list)
    for row in rows:
        grouped[row["similarity_bin"]].append(row)

    bin_summary = []
    for bin_name in ["0.0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"]:
        group = grouped.get(bin_name, [])
        if group:
            avg_final = sum(item["final_mean_opinion"] for item in group) / len(group)
            avg_delta = sum(item["delta_mean_opinion"] for item in group) / len(group)
            avg_gap = sum(item["final_opinion_gap"] for item in group) / len(group)
        else:
            avg_final = avg_delta = avg_gap = None
        bin_summary.append(
            {
                "similarity_bin": bin_name,
                "count": len(group),
                "avg_final_mean_opinion": None if avg_final is None else round(avg_final, 4),
                "avg_delta_mean_opinion": None if avg_delta is None else round(avg_delta, 4),
                "avg_final_opinion_gap": None if avg_gap is None else round(avg_gap, 4),
            }
        )

    summary_path = sweep_dir / "similarity_bin_summary.json"
    summary_path.write_text(json.dumps(bin_summary, indent=2), encoding="utf-8")

    scatter_path = sweep_dir / "similarity_vs_final_opinion.png"
    _write_scatter_plot(scatter_path, rows)

    meta = {
        "start_seed": start_seed,
        "n_runs": n_runs,
        "rounds": rounds,
        "year": year,
        "conversation_mode": conversation_mode,
        "pairing_strategy": pairing_strategy,
        "candidate_pool_size": candidate_pool_size,
        "sweep_dir": str(sweep_dir),
    }
    (sweep_dir / "sweep_metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    return sweep_dir


if __name__ == "__main__":
    args = parse_cli_args()

    llm_service_name = resolve_llm_service_name(args.llm_service)
    llm_service = build_llm_service(llm_service_name)
    if llm_service is not None and args.no_cache:
        llm_service.use_cache = False

    api_key = resolve_llm_api_key(args.api_key, llm_service_name, args.api_key_file)
    model = resolve_llm_model(args.model)
    llm_seed = resolve_llm_seed(args.llm_seed)

    run_sweep(
        start_seed=args.start_seed,
        n_runs=args.n_runs,
        rounds=args.rounds,
        year=args.year,
        output_root=args.output_root,
        run_id=args.run_id,
        llm_service=llm_service,
        api_key=api_key,
        model=model,
        llm_seed=llm_seed,
        ons_male_file=args.ons_male_file,
        ons_female_file=args.ons_female_file,
        conversation_mode=args.conversation_mode,
        pairing_strategy=args.pairing_strategy,
        candidate_pool_size=args.candidate_pool_size,
    )

# Running Chat Ensembles and HPC Comparisons

This guide provides deeper operational guidance for running chat and
chat_opinion ensembles, estimating hosted-provider cost, and comparing hosted
vs HPC outcomes.

## Running Simple Chat Ensembles

For multi-run analysis of the simple chat simulation, run a seed-window sweep:

```bash
make run-example-chat-ensemble
```

Run a smaller exploratory sweep:

```bash
make run-example-chat-ensemble START_SEED=42 N_RUNS=5 RUN_ID=chat_small_01
```

Run a deliberately awkward, high-dissimilarity sweep:

```bash
make run-example-chat-ensemble START_SEED=42 N_RUNS=5 RUN_ID=chat_awkward_small CONVERSATION_MODE=awkward PAIRING_STRATEGY=max_dissimilarity CANDIDATE_POOL_SIZE=12
```

Default outputs are written under `data/output/examples/chat/ensembles/<sweep-directory>/`:

- `similarity_sweep_results.csv` (one row per run)
- `similarity_bin_summary.json` (aggregated metrics by shared-interest bin)
- `similarity_vs_transcript_size.png` (scatter plot)
- `sweep_metadata.json` (sweep configuration)
- `runs/` (full per-run artifacts from underlying chat runs)

Awkward-mode controls:

- `CONVERSATION_MODE=awkward` reduces explicit "find common ground quickly"
  behavior in prompts.
- `PAIRING_STRATEGY=max_dissimilarity` selects the most dissimilar pair from a
  generated candidate pool.
- `CANDIDATE_POOL_SIZE` controls how many candidates are generated before
  selecting the pair (must be `>= 2`; larger values increase chance of sharper
  contrast).

Useful columns in `similarity_sweep_results.csv` for awkward runs:

- `pair_dissimilarity_score`
- `first_shared_interest_round` (`-1` means no explicit shared-interest marker detected)
- `awkward_marker_count`
- `disagreement_marker_count`

## Running Chat + Opinion Ensembles

For multi-run analysis, the ensemble sweep runs many chat+opinion simulations
across a seed window and aggregates similarity/outcome metrics.

Run with defaults:

```bash
make run-example-chat-opinion-ensemble
```

Run with explicit sweep settings:

```bash
make run-example-chat-opinion-ensemble START_SEED=100 N_RUNS=50 ROUNDS=10 RUN_ID=sim_sweep_01
```

Run an awkward, dissimilar pairing sweep:

```bash
make run-example-chat-opinion-ensemble START_SEED=100 N_RUNS=20 ROUNDS=10 RUN_ID=sim_sweep_awkward CONVERSATION_MODE=awkward PAIRING_STRATEGY=max_dissimilarity CANDIDATE_POOL_SIZE=12
```

Run a sweep with custom drift calibration:

```bash
make run-example-chat-opinion-ensemble \
  START_SEED=200 \
  N_RUNS=6 \
  ROUNDS=6 \
  RUN_ID=sweep_mid_normal \
  CONVERSATION_MODE=normal \
  PAIRING_STRATEGY=random \
  NO_CACHE=1 \
  QUESTION_BONUS=0.12 \
  POSITIVE_TOKEN_BONUS=0.14 \
  NEGATIVE_TOKEN_PENALTY=0.38 \
  SHARED_INTEREST_CAP=0.18
```

Default outputs are written under
`data/output/examples/chat_opinion/ensembles/<sweep-directory>/`:

- `similarity_sweep_results.csv` (one row per run)
- `similarity_bin_summary.json` (aggregated metrics by similarity bin)
- `similarity_vs_final_opinion.png` (scatter plot)
- `sweep_metadata.json` (sweep configuration)
- `runs/` (full per-run artifacts from underlying chat+opinion runs)

Notes:

- `pair_similarity_score` blends age similarity, gender similarity, and
  shared-interest overlap.
- The sweep is deterministic for fixed seeds when cache behavior and model
  backend remain stable.
- Use `NO_CACHE=1` when you specifically want to observe live-provider
  variability.
- `CONVERSATION_MODE=awkward` and `PAIRING_STRATEGY=max_dissimilarity` can
  produce slower rapport formation and more uneven dialogue.
- Additional per-run columns include `pair_dissimilarity_score`,
  `first_shared_interest_round`, `awkward_marker_count`, and
  `disagreement_marker_count`.
- `sweep_metadata.json` records the drift config used for the full sweep
  (`opinion_drift_config`).

To summarize selected run outputs quickly:

```bash
make summarize-chat-opinion-runs INPUTS='--run-id calib_base_normal --run-id calib_mid_normal --run-id calib_base_awkward --run-id calib_mid_awkward'
```

## Cost and HPC Guidance for Ensembles

Ensemble runs can consume API credits quickly when using hosted LLM services.

Why this happens:

- Each run creates multiple prompts, and total prompt count scales approximately
  with `N_RUNS x ROUNDS`.
- Conversation histories diverge quickly across seeds, so cache hits are often
  limited in ensemble workloads.
- Running with `NO_CACHE=1` sends every prompt live to the provider.

Recommended practice:

- Start with very small pilots (for example `N_RUNS=3` to `N_RUNS=10`) before
  scaling.
- Prefer local LLM execution for larger sweeps where possible.
- If you have access to HPC resources, use them for local-model ensembles and
  reserve hosted APIs for targeted validation runs.
- Keep hosted and local comparison runs aligned on configuration (seed windows,
  rounds, model settings, cache mode).

Suggested staged workflow:

1. Run a small hosted baseline for `chat` and `chat_opinion` ensembles.
2. Run matching local/HPC ensembles with the same seed window.
3. Compare aggregate outputs (`similarity_sweep_results.csv`, bin summaries,
   plots) across environments.
4. Scale up only after confirming the signal you care about is stable.

## Compare Hosted vs HPC Ensembles

Use the comparison utility to quantify differences between two sweep directories
(for example hosted API vs local/HPC model runs):

```bash
make compare-ensemble-sweeps \
    SWEEP_A=data/output/examples/chat/ensembles/chat_small_01 \
    SWEEP_B=data/output/examples/chat/ensembles/chat_hpc_01 \
    LABEL_A=hosted \
    LABEL_B=hpc \
    RUN_ID=chat_compare_01
```

You can also compare chat_opinion sweeps the same way by pointing `SWEEP_A` and
`SWEEP_B` to chat_opinion ensemble directories.

Outputs are written under
`data/output/examples/ensembles/compare/<comparison-directory>/`:

- `comparison_report.json` (machine-readable deltas and per-bin comparisons)
- `comparison_summary.txt` (quick human-readable summary)

Interpretation tip:

- Treat exact transcript equality as non-goal across hosted vs local/HPC
  models.
- Focus on aggregate deltas in shared metrics (for example means and
  variability) and similarity-bin behavior.

## Compare Individual HPC Chat Runs

When comparing two individual HPC chat run directories (for example same seed
across different server initializations), use:

```bash
make compare-hpc-chat-runs RUN_A=run_511621 RUN_B=run_511679
```

You can also pass full paths:

```bash
make compare-hpc-chat-runs RUN_A=/path/to/run_511621 RUN_B=/path/to/run_511679
```

If needed, override working directory resolution used for job IDs and
`run_<id>` values:

```bash
make compare-hpc-chat-runs RUN_A=511621 RUN_B=511679 WORKING_DIR=/flash-calder/users/<user>/gabm
```

To generate markdown rows for reproducibility stress/concurrency summaries:

```bash
make summarize-hpc-concurrency INPUTS='--header --job-id 511621 --job-id 511679'
```

To generate a single markdown report that includes run manifest details,
pairwise comparison summaries, and concurrency rows:

```bash
make report-hpc-chat-runs \
  INPUTS='--run /path/to/run_835891 --run /path/to/run_836062 --run /path/to/run_836067 --run /path/to/run_839326 --run /path/to/run_839328 --run /path/to/run_839329 --title Calder_HPC_reproducibility_report_Qwen3-14B' \
  OUTPUT=data/output/examples/chat/hpc/Calder/repro_report.md
```

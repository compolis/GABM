# Reproducibility Experiments for Qwen3-14B (Calder and Aire HPC)

This document defines reproducibility experiments for `Qwen3-14B` in GABM using University of Leeds HPC environments (Calder and Aire).
It is intended for release preparation and for ongoing model-behavior monitoring.

Related documents:

- `../release/RELEASE_PREP.md`: release gates/checklist that consume evidence captured here.
- `../handovers/HANDOVER_2026-10-30.md`: historical snapshot of this workstream state at handover time.

## Why this document exists

LLM reproducibility is often partial rather than absolute.
Even with fixed seeds and fixed prompts, exact-token replay may depend on:

- backend implementation details
- kernel/runtime choices
- distributed scheduling behavior under load
- model serving stack/version changes

For this reason, we distinguish:

1. exact reproducibility (bit-for-bit or exact-text equality)
2. practical reproducibility (stable aggregate behavior and stable key metrics)

## Scope

- Model: `Qwen3-14B`
- Environment: Calder H200 and Aire L40S, local vLLM serving via Apptainer
- Workload: `src/gabm/examples/chat/sim.py` and small concurrent ensembles

## Current scripts used

- Single-run launcher: `scripts/hpc/calder/run.sh`
- Concurrent launcher (single server, many clients): `scripts/hpc/calder/chat/run_chat_concurrency.sh`
- Run comparison utility: `scripts/analysis/chat/compare_chat_runs.py`
- Concurrency table-row utility: `scripts/analysis/chat/generate_concurrency_rows.py`
- One-command markdown report utility: `scripts/analysis/chat/generate_hpc_chat_report.py`

## Repro report workflow (recommended)

To make reruns easy for collaborators, generate one markdown report from a set of runs:

```bash
make report-hpc-chat-runs \
  INPUTS="--run /path/to/run_835891 --run /path/to/run_836062 --run /path/to/run_836067 --run /path/to/run_839326 --run /path/to/run_839328 --run /path/to/run_839329 --title Calder_HPC_reproducibility_report_Qwen3-14B" \
  OUTPUT=data/output/examples/chat/hpc/Calder/repro_report.md
```

This produces a report with:

1. run manifest (seed mode, concurrency, successful/failed runs),
2. pairwise transcript/metadata/cache match table,
3. concurrency/stress summary rows.

## Experiment goals

1. Test same-instance determinism.
2. Test cross-initialization determinism (fresh server start).
3. Test diversity across seed windows.
4. Test stability under concurrency scaling.

## Experimental matrix

### E1: Same server instance, same seeds (determinism)

Purpose:
- Check whether repeated runs produce exact same transcripts when all inputs are fixed.

Run:

```bash
sbatch scripts/hpc/calder/chat/run_chat_concurrency.sh \
  --example chat \
  --model Qwen3-14B \
  --sif vllm-openai_latest.sif \
  --n-runs 8 \
  --concurrency 4 \
  --seed-mode fixed \
  --seed 42 \
  --llm-seed 42
```

Note:
- `run_chat_concurrency.sh` defaults to `--no-cache` for live inference reproducibility testing.
- `--example chat` is the default mode.

Optional chat+opinion determinism variant:

```bash
sbatch scripts/hpc/calder/chat/run_chat_concurrency.sh \
  --example chat_opinion \
  --rounds 8 \
  --model Qwen3-14B \
  --sif vllm-openai_latest.sif \
  --n-runs 8 \
  --concurrency 4 \
  --seed-mode fixed \
  --seed 42 \
  --llm-seed 42
```

### E2: Fresh server initialization, same seeds (cross-init determinism)

Purpose:
- Check if two separate server initializations yield identical outputs for same inputs.

Run:
- Execute E1 twice as separate jobs.
- Compare outputs using:

```bash
python3 scripts/analysis/chat/compare_chat_runs.py --run-a <job_id_a> --run-b <job_id_b>
```

### E3: Seed-window variety (ensemble diversity)

Purpose:
- Verify that changing simulation seeds yields meaningful diversity in participants and dialogue.

Run:

```bash
sbatch scripts/hpc/calder/chat/run_chat_concurrency.sh \
  --example chat \
  --model Qwen3-14B \
  --sif vllm-openai_latest.sif \
  --n-runs 12 \
  --concurrency 4 \
  --seed-mode increment \
  --seed 42
```

### E4: Concurrency stress ladder

Purpose:
- Identify practical concurrency limits and behavior changes under load.

Run staged jobs:

1. `--concurrency 4`
2. `--concurrency 8`
3. `--concurrency 12`
4. optional: `--concurrency 16`

Keep `--n-runs` large enough to observe steady-state behavior.

## What to record per run

- Slurm job ID, node, and timestamp
- vLLM log (`vllm_server.log`)
- launcher summary (`launcher_summary.log`)
- per-client logs under `clients/`
- chat transcripts and `run_metadata.json`

## Primary acceptance checks

For E1 and E2:

1. Exact transcript match rate across shared run IDs.
2. Metadata core match rate (ignoring volatile fields).
3. Presence/consistency of `openai_system_fingerprints` where available.
4. Failure count (`FAILED_RUNS`) from launcher summary.

For E3 and E4:

1. Non-zero diversity in participants and transcript content.
2. No systematic worker failures at target concurrency.
3. Stable completion behavior as concurrency scales.

## Interpretation guidance

- Exact reproducibility may fail even when seeds are fixed.
- A mismatch does not automatically indicate a bug in GABM logic.
- If exact-match rates drop suddenly between similar runs, inspect:
  - model/container version changes
  - server startup flags
  - backend fingerprints
  - runtime warnings/errors in vLLM logs

## Release 0.3.0 use

Use this document as the reproducibility evidence protocol for local/HPC model checks.
Include key outcomes in release notes:

- exact-match rates (same instance and cross-init)
- observed diversity in seed-window ensembles
- practical concurrency ceiling with acceptable failure rate

## Results capture template

Use this template while jobs are running.

### Run log

| Experiment | Job ID | Date | Model | Seed mode | Seed / Start seed | N runs | Concurrency | Cache mode | LLM seed | Notes |
|---|---:|---|---|---|---|---:|---:|---|---|---|
| E1 same-instance determinism (run A) |  |  | Qwen3-14B | fixed | 42 | 8 | 4 | no-cache | 42 |  |
| E1 same-instance determinism (run B) |  |  | Qwen3-14B | fixed | 42 | 8 | 4 | no-cache | 42 |  |
| E2 cross-init determinism (run C) |  |  | Qwen3-14B | fixed | 42 | 8 | 4 | no-cache | 42 | fresh init |
| E2 cross-init determinism (run D) |  |  | Qwen3-14B | fixed | 42 | 8 | 4 | no-cache | 42 | fresh init |
| E3 diversity baseline |  |  | Qwen3-14B | increment | 42 | 12 | 4 | no-cache |  |  |
| E4 stress level 1 |  |  | Qwen3-14B | increment | 42 | 24 | 4 | no-cache |  |  |
| E4 stress level 2 |  |  | Qwen3-14B | increment | 42 | 24 | 8 | no-cache |  |  |
| E4 stress level 3 |  |  | Qwen3-14B | increment | 42 | 24 | 12 | no-cache |  |  |

### Determinism comparison summary

For each pair, run:

```bash
python3 scripts/analysis/chat/compare_chat_runs.py --run-a <job_id_a> --run-b <job_id_b>
```

| Comparison | Shared run IDs | Transcript exact matches | Metadata core matches | Cache-delta exact matches | Determinism signal |
|---|---:|---:|---:|---:|---|
| E1 run A vs run B |  |  |  |  |  |
| E2 run C vs run D |  |  |  |  |  |

### Concurrency/stress summary

Capture from `launcher_summary.log` and worker outputs.

Helper to generate markdown rows from job IDs:

```bash
python3 scripts/analysis/chat/generate_concurrency_rows.py --header --job-id <job_id_1> --job-id <job_id_2>
```

| Job ID | Concurrency | N runs | Successful runs | Failed runs | Mean runtime per run (if measured) | Error pattern |
|---:|---:|---:|---:|---:|---|---|
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |

### Release evidence notes

- Same-instance exact reproducibility statement:
  - 
- Cross-initialization exact reproducibility statement:
  - 
- Practical reproducibility statement (aggregate behavior stable/unstable):
  - 
- Recommended default concurrency for release runs:
  - 

## Observed results (2026-11-02)

Local copied Calder outputs currently available under `data/output/examples/chat/hpc/Calder/`:

- `run_494869/chat_seed42`
- `run_511621/run_511621/chat_seed42`
- `run_511679/run_511679/chat_seed43`

Pairwise transcript comparison matrix:

| A job | B job | A run_id | B run_id | seed relation | transcript exact match | note |
|---|---|---|---|---|---|---|
| run_494869 | run_511621 | chat_seed42 | chat_seed42 | same | yes | - |
| run_494869 | run_511679 | chat_seed42 | chat_seed43 | different | no | - |
| run_511621 | run_511679 | chat_seed42 | chat_seed43 | different | no | - |

Summary metrics:

- Same-seed exact transcript match rate: `1/1`
- Different-seed exact transcript match count: `0/2`

Interpretation:

- Current evidence supports same-seed reproducibility for the available Qwen3-14B pair.
- Different seeds produce non-identical transcripts, consistent with expected diversity.
- One copied run layout is nested (`run_<id>/run_<id>/...`), so comparisons should point to the inner run directory when needed.

## Observed results (2026-11-08, additional Calder sweeps)

Additional local copied Calder outputs under `data/output/examples/chat/hpc/Calder/`:

- `run_835891` (`seed-mode=increment`, seeds 42..49)
- `run_836062` (`seed-mode=fixed`, seed 42)
- `run_836067` (`seed-mode=fixed`, seed 42)
- `run_839326` (`seed-mode=fixed`, seed 42, `ROUNDS=16`)
- `run_839328` (`seed-mode=increment`, seeds 42..49, `ROUNDS=16`)
- `run_839329` (`seed-mode=increment`, seeds 42..49, `ROUNDS=16`)

Pairwise comparison summary (via `scripts/analysis/chat/compare_chat_runs.py`):

| A job | B job | Shared run IDs | Transcript exact matches | Metadata core matches | Cache-delta exact matches | Determinism signal |
|---|---|---:|---:|---:|---:|---|
| run_836062 | run_836067 | 8 | 0/8 | 0/8 | 0/8 | differ |
| run_839328 | run_839329 | 8 | 0/8 | 0/8 | 0/8 | differ |
| run_835891 | run_839328 | 8 | 0/8 | 1/8 | 0/8 | differ |
| run_835891 | run_839329 | 8 | 0/8 | 0/8 | 0/8 | differ |
| run_836062 | run_839326 | 8 | 0/8 | 0/8 | 0/8 | differ |

Concurrency launcher summaries (via `scripts/analysis/chat/generate_concurrency_rows.py`):

| Job ID | Concurrency | N runs | Successful runs | Failed runs | Mean runtime per run (if measured) | Error pattern |
|---:|---:|---:|---:|---:|---|---|
| 835891 | 4 | 8 | 8 | 0 | n/a | none |
| 836062 | 4 | 8 | 8 | 0 | n/a | none |
| 836067 | 4 | 8 | 8 | 0 | n/a | none |
| 839326 | 4 | 8 | 8 | 0 | n/a | none |
| 839328 | 4 | 8 | 8 | 0 | n/a | none |
| 839329 | 4 | 8 | 8 | 0 | n/a | none |

Interpretation:

- For this newer sweep batch, all compared run pairs showed `0/8` exact transcript matches (except metadata `1/8` in one increment/increment pair).
- Operational stability was strong at tested concurrency (`FAILED_RUNS=0` for all listed jobs).
- Current evidence suggests practical stability in completion behavior under these settings, but weak exact replay across independent run initializations.

## Observed results (2026-11-12, Aire compatibility + determinism classification)

Initial Aire bring-up findings:

- Using `vllm-openai_latest.sif` failed during engine initialization with a driver/runtime mismatch on Aire (`RuntimeError: The NVIDIA driver on your system is too old (found version 12060)`).
- Switching to an older Aire-compatible SIF resolved startup failures.

Smoke validation:

- `run_9431441` (`chat_opinion`, `n-runs=2`, `concurrency=1`, fixed seed + `llm-seed=42`) completed with `SUCCESSFUL_RUNS=2`, `FAILED_RUNS=0`.

Paired fixed-seed determinism checks (`chat_opinion`, `n-runs=8`, `seed=42`, `llm-seed=42`):

| A job | B job | Concurrency | Shared run IDs | Transcript exact matches | Metadata core matches | Cache-delta exact matches | Determinism signal |
|---|---|---:|---:|---:|---:|---:|---|
| run_9431809 | run_9431810 | 2 | 8 | 0/8 | 6/8 | 0/8 | differ |
| run_9432287 | run_9432288 | 1 | 8 | 8/8 | 8/8 | 0/8 | exact replay |

Interpretation:

- Aire operational completion is stable at both tested concurrency levels (`FAILED_RUNS=0`).
- On the current Aire-compatible runtime stack, exact replay is concurrency-sensitive:
  - `concurrency=1`: exact transcript replay observed (`8/8`)
  - `concurrency=2`: exact transcript replay not observed (`0/8`)
- For reproducibility-critical Aire evidence runs, use `--concurrency 1`.

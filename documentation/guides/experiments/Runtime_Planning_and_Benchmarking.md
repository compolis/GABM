# Runtime Planning and Benchmarking

Use this guide to estimate runtime before large runs and decide whether to run
locally, via hosted APIs, on HPC, or on cloud infrastructure.

## 1) Quick runtime estimate from a pilot

Run a small pilot first, then project.

Example pilot timing (`chat_opinion`, 2 rounds):

```bash
time PYTHONPATH=src python3 src/gabm/examples/chat_opinion/sim.py \
  --llm-service openai \
  --model qwen3:8b \
  --api-key ollama \
  --seed 42 \
  --year 2026 \
  --rounds 2 \
  --run-id pilot_rounds2
```

First-pass projection:

- projected time ≈ pilot time × (target rounds / pilot rounds)
- for ensemble sweeps, multiply again by `N_RUNS`

## 2) Practical decision framework

Use this default approach:

- **Local + Ollama:** setup checks, smoke tests, and small exploratory runs.
- **Hosted APIs:** quick experiments where convenience matters more than strict
  cost/latency control.
- **HPC + vLLM:** larger ensemble production runs where throughput and
  queue-managed reproducibility are important.
- **Cloud self-hosted inference:** an option for teams without HPC access, but
  typically a larger setup/operations task.

If projected runtime is high (for example near or above 24 hours), strongly
consider moving from local execution to HPC or cloud.

## 3) Long-run reliability guidance

For long jobs, split work into smaller batches to reduce restart risk and keep
incremental outputs.

Example batch pattern:

```bash
# batch 1
make run-example-chat-ensemble START_SEED=100 N_RUNS=10 RUN_ID=local_batch_1

# batch 2
make run-example-chat-ensemble START_SEED=110 N_RUNS=10 RUN_ID=local_batch_2
```

## 4) Benchmark log template

Record a benchmark before scaling up so contributors can compare platforms with
evidence.

```text
Date:
Contributor:
Device / environment:
  - CPU:
  - GPU (if any):
  - RAM:
  - OS:
Execution mode:
  - Local Ollama / Hosted API / HPC vLLM / Cloud self-hosted
Model:
Pilot command:
Pilot size:
  - rounds:
  - n_runs:
Elapsed pilot time:
Projected target size:
  - rounds:
  - n_runs:
Projection method:
Projected total runtime:
Recommendation:
  - Keep local / Split into batches / Move to HPC / Evaluate cloud option
Notes:
```

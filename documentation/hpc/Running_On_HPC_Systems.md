# Running On HPC Systems

Some LLM workloads need more compute than a typical laptop or desktop can provide. This guide outlines a general approach for running GABM-related model serving and experiments on High Performance Computing (HPC) systems.

The examples in this repository currently use:
- Slurm for job scheduling
- Apptainer for container runtime
- vLLM for model serving

You can adapt the same pattern to your institution's HPC environment.

## Recommended Script Location

Keep HPC scripts under:
- `scripts/hpc/`

Current Calder examples:
- `scripts/hpc/calder/run_concurrency.sh` (preferred generic entrypoint)
- `scripts/hpc/calder/run.sh`
- `scripts/hpc/calder/run_server.sh`
- `scripts/hpc/calder/run_client.sh`
- `scripts/hpc/calder/chat/run_chat_concurrency.sh`
- `scripts/hpc/calder/chat_opinion/run_chat_opinion_concurrency.sh`

Current Aire examples:
- `scripts/hpc/aire/run_concurrency.sh` (preferred generic entrypoint)
- `scripts/hpc/aire/run_concurrency_flash.sh` (preferred for heavier runs using `/flash` staging)
- `scripts/hpc/aire/chat/run_chat_concurrency.sh`
- `scripts/hpc/aire/chat_opinion/run_chat_opinion_concurrency.sh`

Compatibility note:
- Prefer `run_concurrency.sh` under each HPC system directory for new workflows.
- Existing `chat/` and `chat_opinion/` launchers remain available as compatibility entrypoints.

Usage note:
- `run_concurrency.sh` is the preferred generic entrypoint.
- Select workload explicitly with `--example chat` or `--example chat_opinion`.
- Existing `chat/` and `chat_opinion/` script paths remain available as compatibility wrappers.

## One-time setup on a login node

The following setup snippets are intended as practical starting points and can
be adapted to site policy changes.

### Calder

Calder data can be stored more persistently under `/flash-calder`.

```bash
HPC="calder"
DIR_S="/scratch-calder/users/$USER"
DIR_F="/flash-calder/users/$USER"
VLLM_V=0.11.0
HF_HUB="$DIR_F/gabm/huggingface/hub"

cd "$DIR_F"
module load calder/hopper
module load miniforge3

# Optional prebuilt Apertus image
apptainer pull apertus15.sif docker://ghcr.io/swiss-ai/vllm_apertus_1.5_release:latest-amd64
```

### Aire

On Aire, flash scratch is job-local/ephemeral and not suitable as durable
storage.
Use `/mnt/scratch/$USER` for persistent assets and outputs.

For heavier or longer-running jobs, performance is often better if model and
container assets are staged to job flash at job start (NVMe-local I/O), then
run from flash, and finally copy outputs back to `/mnt/scratch/$USER` before
job completion.

Per Aire storage docs, use `$TMP_SHARED` when available (typically
`/mnt/flash/tmp/job.<JOB-ID>`), not `/flash/$USER`.

For lighter runs, using `/mnt/scratch/$USER` directly is simpler.

When you want this behavior automatically, use
`scripts/hpc/aire/run_concurrency_flash.sh`, which stages SIF/model assets to a
writable flash path (preferring `$TMP_SHARED`), runs via the standard Aire
launcher, then copies run outputs back to persistent scratch before job exit.

```bash
HPC="aire"
DIR_S="/mnt/scratch/$USER"
VLLM_V=0.33.0
HF_HUB="$DIR_S/gabm/huggingface/hub"

cd "$DIR_S"
module load apptainer
module load miniforge
```

### Shared setup steps (both systems)

```bash
# Pull vLLM OpenAI image
apptainer pull docker://vllm/vllm-openai:v$VLLM_V

# Prepare model cache directory
mkdir -p "$HF_HUB"

# Install Hugging Face CLI (one-time per user environment)
curl -LsSf https://hf.co/cli/install.sh | bash

# Download model snapshots
hf download swiss-ai/Apertus-8B-2509 --local-dir "$HF_HUB/Apertus-8B-2509"
hf download swiss-ai/Apertus-70B-2509 --local-dir "$HF_HUB/Apertus-70B-2509"
hf download swiss-ai/Apertus-v1.5-8B --local-dir "$HF_HUB/Apertus-v1.5-8B"
hf download swiss-ai/Apertus-v1.5-70B --local-dir "$HF_HUB/Apertus-v1.5-70B"
hf download Qwen/Qwen3-14B --local-dir "$HF_HUB/Qwen3-14B"

# Clone and prepare environment
git clone https://github.com/compolis/GABM.git
cd GABM
conda create -n "gabm-$HPC" -y python=3.14
conda activate "gabm-$HPC"
pip install --upgrade pip setuptools wheel
```

## Typical Workflow

1. Prepare environment and model assets
- Confirm access to GPUs and scheduler partition/queue.
- Confirm model files are available on shared or node-local storage.
- Confirm container image availability and path.

2. Submit model-serving job
- Use a Slurm script in `scripts/hpc/` as the starting template.
- Tune resources: GPUs, CPUs, memory, walltime.
- Set model-serving options such as tensor parallel size and max context length.

3. Validate service health
- Check scheduler output/error logs.
- Verify GPU utilization and memory.
- Confirm endpoint reachability from your experiment environment.

4. Run GABM experiments
- Run small pilot sweeps first.
- Capture run metadata and output artifacts for reproducibility.
- Compare hosted vs local/HPC behavior using ensemble comparison tools.

## Calder + Apertus Known-Working Notes (historical reference)

The previous dedicated Calder/Apertus note has been consolidated here. Use this section as a practical baseline rather than a strict requirement.

Tested stack snapshots:
- Calder H200 (Grace Hopper) nodes
- Apptainer
- vLLM (0.23.1 and 0.23.1rc1 observed in prior runs)
- Apertus-v1.5-70B

Observed serving settings from successful runs:
- `tensor_parallel_size=4`
- `gpu_memory_utilization=0.8`
- `max_model_len=262144`
- `fuse_allreduce_rms=false`

Observed operational characteristics:
- Startup time around 148 seconds (environment-dependent)
- Reported KV cache around 983,456 tokens in one prior setup
- Reported max concurrency at full context around 3.75 requests in one prior setup

Resource profiles recorded in prior notes:
- Profile A: 1 node, 4 H200 GPUs, 64 CPU cores
- Profile B: 1 node, 4 H200 GPUs, 112 CPUs

These values are useful as starting points. Re-tune for your partition limits, model revisions, and scheduler policy.

## Portability Checklist

When moving between HPC systems, review these items:
- Module names and versions (CUDA, NCCL, etc.)
- Container runtime options (`apptainer` flags)
- Filesystem paths for models and logs
- Scheduler directives (`#SBATCH` lines)
- Available GPU types and counts
- Network and firewall constraints for service ports
- Stage-in/stage-out conventions for node-local storage (for Aire, the
  concurrency launcher stages `src/` and `data/input/` to `${TMPDIR}` and
  syncs run outputs back to shared storage at job exit)
- Whether high-performance local NVMe storage is available (for Aire, prefer
  `$TMP_SHARED` / `/mnt/flash/tmp/job.<JOB-ID>` for heavy runs; treat it as
  ephemeral and stage outputs back to persistent scratch before job completion)

## Operational Guidance

- Start with conservative resource settings, then scale.
- Prefer explicit environment variables for tunables.
- Keep memory and GPU monitoring enabled for long runs.
- Record exact model, runtime, and scheduler settings with experiment outputs.

## Security and Cost Notes

- Treat API keys and credentials as secrets; do not hardcode them in scripts.
- For large ensemble runs, local/HPC inference can be more cost-effective than repeated hosted API calls.
- Pilot with small `N_RUNS` before scaling to larger sweeps.

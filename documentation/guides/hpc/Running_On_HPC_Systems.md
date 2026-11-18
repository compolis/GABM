# Running On HPC Systems

Some LLM workloads need more compute than a typical laptop or desktop can provide. This guide outlines a general approach for running GABM-related model serving and experiments on High Performance Computing (HPC) systems.

Whilst Graphics Processing Units (GPUs) are not necessarily needed to use smaller Large Language Models (LLMs) like Apertus 1.5 8B with around 8 billion parameters, they are effectively needed for the larger models like Apertus 1.5 70B with 70 billion parameters.

HPC systems typically have a scheduler that manages jobs submitted by multiple users. The examples here currently use:
- [Slurm](https://slurm.schedmd.com/) for job scheduling
- [Apptainer](https://apptainer.org/) for container runtime
- [vLLM](https://vllm.ai/) as the LLM serving inference engine


## Recommended Script Location

Keep HPC scripts under:
- `scripts/hpc/`

## University of Leeds HPC Systems

### Aire

[Aire documentation](https://arcdocs.leeds.ac.uk/aire/)

Aire has 28 GPU nodes each with 3 [NVIDIA L40S GPU](https://www.nvidia.com/en-gb/data-center/l40s/)s for use with 8 CPU cores each and a share of around 1.2 TB of Memory (https://arcdocs.leeds.ac.uk/aire/system/compute_node_types.html#gpu-node).

[Data Center Driver for Linux aarch64 560.35.03 | Linux aarch64](https://www.nvidia.com/en-us/drivers/details/231403/) is available for [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit-archive) 12.6. [CUDA Toolkit 12.6.2](https://docs.nvidia.com/cuda/archive/12.6.2/) is available via the module system.

On Aire, NVMe flash storage is only available for running jobs as `$TMP_SHARED` or (`/mnt/flash/tmp/job.<JOB-ID>`). `/mnt/scratch/$USER` is to be used for persistent assets and outputs.

Performance may be better if model and container assets are staged to flash at the start, and outputs copied back to `/mnt/scratch/$USER` before job completion.
If writable shared flash is unavailable on a node, the Aire flash wrapper can fall back to a writable local path (for example in `/tmp`).

### Calder

[Calder documentation](https://arcdocs.leeds.ac.uk/calder)

Calder has 7 GPU nodes each with 8 [NVIDIA H200 NVL GPU](https://www.nvidia.com/en-gb/data-center/h200/)s for use with 16 CPU cores each and a share of 1.5 TB of Memory (https://arcdocs.leeds.ac.uk/calder/system/node_types.html#gpu-node).

[Data Center Driver for Linux aarch64 595.112.07 | Linux aarch64 RHEL 9](https://www.nvidia.com/en-us/drivers/details/283243) is available for [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit-archive) 13.2. [CUDA Toolkit 13.3.0](https://docs.nvidia.com/cuda/archive/13.3.0/) is available via the module system.

Calder data can be stored more persistently on NVMe storage under `/flash-calder`.


## Example scripts for running on Leeds HPC

### Aire Examples
- `scripts/hpc/aire/run_concurrency.sh` (preferred generic entrypoint)
- `scripts/hpc/aire/run_concurrency_flash.sh` (preferred for heavier runs using `/flash` staging)
- `scripts/hpc/aire/chat/run_chat_concurrency.sh`
- `scripts/hpc/aire/chat_opinion/run_chat_opinion_concurrency.sh`

### Calder Examples
- `scripts/hpc/calder/run_concurrency.sh` (preferred generic entrypoint)
- `scripts/hpc/calder/run.sh`
- `scripts/hpc/calder/run_server.sh`
- `scripts/hpc/calder/run_client.sh`
- `scripts/hpc/calder/chat/run_chat_concurrency.sh`
- `scripts/hpc/calder/chat_opinion/run_chat_opinion_concurrency.sh`

### Script selection guide

| System | Script | Use when | Type |
|---|---|---|---|
| Aire | `scripts/hpc/aire/run_concurrency.sh` | You want the standard Aire entrypoint for concurrent simulation runs | Primary entrypoint (delegates to `chat/run_chat_concurrency.sh`) |
| Aire | `scripts/hpc/aire/run_concurrency_flash.sh` | You want to stage model + SIF to node-local flash for heavier runs | Primary entrypoint (flash-staging wrapper) |
| Aire | `scripts/hpc/aire/chat/run_chat_concurrency.sh` | You want direct control of chat concurrency launcher options | Base launcher used by wrappers |
| Aire | `scripts/hpc/aire/chat_opinion/run_chat_opinion_concurrency.sh` | You want chat_opinion mode using the same concurrency framework | Mode wrapper around chat concurrency launcher |
| Calder | `scripts/hpc/calder/run_concurrency.sh` | You want the standard Calder entrypoint for concurrent simulation runs | Primary entrypoint (delegates to `chat/run_chat_concurrency.sh`) |
| Calder | `scripts/hpc/calder/chat/run_chat_concurrency.sh` | You want direct control of chat concurrency launcher options | Base launcher used by wrappers |
| Calder | `scripts/hpc/calder/chat_opinion/run_chat_opinion_concurrency.sh` | You want chat_opinion mode using the same concurrency framework | Mode wrapper around chat concurrency launcher |
| Calder | `scripts/hpc/calder/run.sh` | You want one script that starts serving and runs a selected simulation mode | Combined server + simulation launcher |
| Calder | `scripts/hpc/calder/run_server.sh` | You want to start only the vLLM server job | Server-only launcher |
| Calder | `scripts/hpc/calder/run_client.sh` | You already have a running server and want to send reproducibility/client requests | Client-only launcher |

## Per-HPC vLLM variables file

Each HPC directory keeps its own variables file so scripts can use the same
variable names regardless of system:

- `scripts/hpc/aire/variables.sh`
- `scripts/hpc/calder/variables.sh`

Each file defines:

- `VLLM_VERSION` (for example `0.11.0` or `0.33.0`)
- `VLLM_SIF` (derived as `vllm-openai_v${VLLM_VERSION}.sif`)
- `DEFAULT_WORKING_DIR` (HPC-local default working directory)
- `DEFAULT_CONDA_ENV` (default conda environment name for launchers)

If you add support for another HPC system, create
`scripts/hpc/<new-hpc>/variables.sh` with the same two variables and source it
from that HPC's launcher scripts.

## One-time setup on a login node

### Aire

```bash
source scripts/hpc/aire/variables.sh
HPC="aire"
DIR_S="/mnt/scratch/$USER"
HF_HUB="$DIR_S/gabm/huggingface/hub"

cd "$DIR_S"
module load apptainer
module load miniforge
```

### Calder

```bash
source scripts/hpc/calder/variables.sh
HPC="calder"
DIR_S="/scratch-calder/users/$USER"
DIR_F="/flash-calder/users/$USER"
HF_HUB="$DIR_F/gabm/huggingface/hub"

cd "$DIR_F"
module load calder/hopper
module load miniforge3

# Optional prebuilt Apertus image
apptainer pull apertus15.sif docker://ghcr.io/swiss-ai/vllm_apertus_1.5_release:latest-amd64
```

### Shared setup steps (both systems)

```bash
# Pull vLLM OpenAI image
apptainer pull "vllm-openai_v${VLLM_VERSION}.sif" "docker://vllm/vllm-openai:v${VLLM_VERSION}"

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
# Replace with your fork URL if needed.
git clone https://github.com/compolis/GABM.git
cd GABM
conda create -n "gabm-$HPC" -y python=3.12
conda activate "gabm-$HPC"
pip install --upgrade pip setuptools wheel
pip install -r requirements-dev.txt
pip install -e .
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


## Calder + Apertus 1.5 70B Known-Working Notes

- Requirements: 4 H200 GPUs, 64 CPU cores

Serving settings from successful runs:
- `tensor_parallel_size=4`
- `gpu_memory_utilization=0.8`
- `max_model_len=262144`
- `fuse_allreduce_rms=false`

Observed operational characteristics:
- Startup time around 148 seconds (environment-dependent)
- Reported KV cache around 983,456 tokens
- Reported max concurrency at full context around 3.75 requests


## Portability Checklist

When moving between HPC systems, review these items:
- The NVIDIA driver version and available GPU types and counts on nodes
- Module names and versions (CUDA, NCCL)
- Container runtime options (`apptainer` flags)
- Filesystem paths for models and logs
- Scheduler directives (`#SBATCH` lines)
- Network and firewall constraints for service ports
- Stage-in/stage-out conventions for node-local storage
- Whether high-performance local storage is available


## Operational Guidance

- Start with conservative resource settings, then scale.
- Monitor memory and GPU utilisation.
- Record exact model, runtime, and scheduler settings with experiment outputs.


## Security and Cost Notes

- Treat API keys and credentials as secrets; do not hardcode them in scripts.
- For large ensemble runs, local/HPC inference is expected to be more cost-effective than using LLM Service APIs.
- For runtime estimation and benchmark logging that compare local, hosted, HPC, and cloud options, see [../experiments/Runtime_Planning_and_Benchmarking.md](../experiments/Runtime_Planning_and_Benchmarking.md).
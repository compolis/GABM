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
- `scripts/hpc/calder/run.sh`
- `scripts/hpc/calder/run_server.sh`
- `scripts/hpc/calder/run_client.sh`
- `scripts/hpc/calder/run_chat_concurrency.sh`

Compatibility note:
- Prefer using scripts directly from `scripts/hpc/` for new workflows.

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

## Operational Guidance

- Start with conservative resource settings, then scale.
- Prefer explicit environment variables for tunables.
- Keep memory and GPU monitoring enabled for long runs.
- Record exact model, runtime, and scheduler settings with experiment outputs.

## Security and Cost Notes

- Treat API keys and credentials as secrets; do not hardcode them in scripts.
- For large ensemble runs, local/HPC inference can be more cost-effective than repeated hosted API calls.
- Pilot with small `N_RUNS` before scaling to larger sweeps.

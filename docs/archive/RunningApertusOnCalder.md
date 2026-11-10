# Running LLMs on HPC systems (Apertus on Calder)

This archived note preserves an earlier Calder/Apertus setup snapshot.

For active guidance, use:
- [Running_On_HPC_Systems.md](../documentation/hpc/Running_On_HPC_Systems.md)

Some LLMs require more computational resources than are generally available in normal laptop or desktop machines. This guide explains how to run [Apertus](https://www.apertus-ai.org/) models on the [University of Leeds Calder](https://arc.leeds.ac.uk/knowledge-centre/resources/calder/) High Perfomance Computing (HPC) system using [Apptainer](https://apptainer.org/).

Tested configuration:
- Calder H200 (Grace Hopper) nodes
- vLLM 0.23.1
- Apptainer
- Apertus-v1.5-70B
- Tensor parallelism across 8 GPUs

## Known Working Configuration
- Model: Apertus-v1.5-70B
- Resources:
  - 1 node
  - 4 H200 GPUs
  - 64 CPU cores
  - 200 GB RAM per core
- Context length:
  - 65336 tokens
- Tensor parallel size:
  - 4

- Model:
  - Apertus-v1.5-70B
- Node:
  - Calder H200
- Resources:
  - 4 H200 GPUs
  - 112 CPUs
  - 200 GB RAM
- vLLM:
  - 0.23.1rc1
- Settings:
  - tensor_parallel_size=4
  - gpu_memory_utilization=0.8
  - max_model_len=262144
  - fuse_allreduce_rms=false
- Startup time:
  - ~148 seconds
- KV cache:
  - 983,456 tokens
- Max concurrency at full context:
  - 3.75 requests

[Example Calder Slurm Script](../../scripts/hpc/calder/run.sh)

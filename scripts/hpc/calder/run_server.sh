#!/bin/bash
# =============================================================================
# GABM — server Calder (Leeds HPC) launcher
# =============================================================================
#
# WHAT THIS DOES:
#   1. Loads the necessary modules for activating a conda enviornment.
#   2. Starts a vLLM server on a H200 GPU node within an apptainer container. The vLLM server is loaded with the model specified.
#
# HOW TO RUN IT:
#   1. Download the LLM model you want to use.
#   2. Download a vLLM apptainer sif file to use.
#
# Here is an example command:
# sbatch scripts/calder/run_server.sh --model Qwen3-14B --working-dir /scratch-calder/calder-uat/geoagdt/gabm --sif vllm-openai_latest.sif
#
# --model is the name of the LLM model to run
# --working-dir is a directory location where the sif file is located and where results will be written in a cag_runs folder
# --sif is the name of the sif file to use
# --seed is the seed to use to initilise the LLM
#
# The following are Slurm parameters to request resources and direct output
# "LLM-" job-name prefix is wanted for LLM jobs (Research Computing policy).
#SBATCH --job-name=LLM-gabm-server
#SBATCH --nodes=1
#SBATCH --partition=calder-gpu-hopper
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=4
#SBATCH --cpus-per-task=32
#SBATCH --mem=256G
#SBATCH --time=01:00:00            
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

set -euo pipefail

# set -x causes every command to be echoed into the Slurm output file as it's executed.
set -x

# Default MODEL_NAME, SIF_FILE, WORKING_DIR, SEED
MODEL_NAME="Apertus-v1.5-70B"
#MODEL_NAME="Apertus-v1.5-8B"
#MODEL_NAME="Qwen3-14B"
# Install hf if necessary the download a model
# curl -LsSf https://hf.co/cli/install.sh | bash
# hf download swiss-ai/Apertus-v1.5-8B --local-dir ~/.cache/huggingface/hub/Apertus-v1.5-8B
# hf download swiss-ai/Apertus-v1.5-70B --local-dir ~/.cache/huggingface/hub/Apertus-v1.5-70B
# hf download Qwen/Qwen3-14B --local-dir /scratch-calder/calder-uat/geoagdt/gabm/huggingface/hub/Qwen3-14B

# Obtain sif file:
# apptainer pull apertus15.sif docker://ghcr.io/swiss-ai/vllm_apertus_1.5_release:latest-amd64
# apptainer pull docker://vllm/vllm-openai
SIF_FILE="apertus15.sif"
#SIF_FILE="vllm-openai_latest.sif"
#WORKING_DIR="/scratch-calder/calder-uat/${USER}/gabm"
#WORKING_DIR="/users/${USER}/gabm"
WORKING_DIR="/flash-calder/users/${USER}/gabm"
SEED="42"


# Check Arguments
CLI_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model)
      [[ -z "$2" ]] && { echo "Missing value for --model"; exit 1; }
      MODEL_NAME="$2"
      shift 2
      ;;
    --sif)
      [[ -z "$2" ]] && { echo "Missing value for --sif"; exit 1; }
      SIF_FILE="$2"
      shift 2
      ;;
    --working-dir)
      [[ -z "$2" ]] && { echo "Missing value for --working-dir"; exit 1; }
      WORKING_DIR="$2"
      shift 2
      ;;
    --seed)
      [[ -z "$2" ]] && { echo "Missing value for --seed"; exit 1; }
      SEED="$2"
      shift 2
      ;;
    *)
      CLI_ARGS+=("$1")
      shift
      ;;
  esac
done


echo "=== MODEL_NAME ==="
echo ${MODEL_NAME}

# Load modules
module load calder/hopper
module load cuda/13.3.0
module load nccl/2.29.7-1

echo "=== WORKING_DIR ==="
echo ${WORKING_DIR}

MODEL_DIR="${WORKING_DIR}/huggingface/hub/${MODEL_NAME}"
echo "=== MODEL_DIR ==="
echo ${MODEL_DIR}

# Obtain sif file:
# apptainer pull apertus15.sif docker://ghcr.io/swiss-ai/vllm_apertus_1.5_release:latest-amd64
SIF_IMAGE="${WORKING_DIR}/${SIF_FILE}"

# Avoid PORT collisions rather than setting PORT=8000
PORT=$((10000 + SLURM_JOB_ID % 50000))
echo "=== PORT ==="
echo ${PORT}

BASE_URL="http://localhost:${PORT}/v1"
REPO_DIR="${SLURM_SUBMIT_DIR}"
cd "${REPO_DIR}"
echo "=== REPO_DIR ==="
echo ${REPO_DIR}

OUTDIR="${WORKING_DIR}/cag_runs/run_${SLURM_JOB_ID}"
mkdir -p "${OUTDIR}"
echo "Using OUTDIR=$OUTDIR"
echo "Using SEED=$SEED"

export PYTHONUNBUFFERED=1
export APPTAINERENV_PYTHONUNBUFFERED=1
export APPTAINERENV_CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES

echo "=== Node information ==="
echo "=== GPU Information ==="
nvidia-smi -L
echo "=== CPU Information ==="
lscpu | grep "^CPU(s):"
echo "=== Memory Information ==="
free -h

echo "=== Job details ==="
echo "Job ID: $SLURM_JOBID"
echo "Number of GPUs: $SLURM_GPUS_ON_NODE"
echo "Number of CPUs: $SLURM_CPUS_ON_NODE"

echo "=== Start memory logging ==="
MEMORY_LOG="run_${MODEL_NAME}_${SLURM_GPUS_ON_NODE}_${SLURM_JOBID}.log"
echo "MEMORY_LOG: $MEMORY_LOG"
(
while true
do
  date
  nvidia-smi --query-gpu=index,memory.used,utilization.gpu \
             --format=csv,noheader
  sleep 50
done
) > $MEMORY_LOG &
MONITOR_PID=$!

echo "=== Starting Grace Hopper Production Inference Execution ==="
echo "Assigned Compute Node: $(hostname)"
echo "Visible Slurm GPU Indices: $CUDA_VISIBLE_DEVICES"

echo "=== Start Apptainer ==="

START=$(date +%s)

SERVER_LOG="${OUTDIR}/vllm_server.log"

apptainer exec \
  --cleanenv \
  --nv \
  -B ${WORKING_DIR}:${WORKING_DIR} \
  --env CUDA_HOME=/usr/local/cuda \
  --env CUDACXX=/usr/local/cuda/bin/nvcc \
  --env VLLM_ENABLE_V1_MULTIPROCESSING=0 \
  --env VLLM_BATCH_INVARIANT=1 \
  ${SIF_IMAGE} \
  vllm serve $MODEL_DIR \
  --seed ${SEED} \
  --served-model-name ${MODEL_NAME} \
  --tensor-parallel-size $SLURM_GPUS_ON_NODE \
  --compilation-config.pass_config.fuse_allreduce_rms=false \
  --chat-template-content-format string \
  --gpu-memory-utilization 0.9 \
  --port "${PORT}" \
  > "${SERVER_LOG}" 2>&1 

SERVER_PID=$?

# Shutdown
cleanup() {
  kill "${SERVER_PID}" 2>/dev/null || true
  wait "${SERVER_PID}" 2>/dev/null || true
}
trap cleanup EXIT

# Capture exit code of apptainer vllm serve process
EXIT_CODE=$?


echo "=== End Apptainer ==="
echo "Apptainer exited with code: ${EXIT_CODE}"

echo "=== End memory logging ==="
kill $MONITOR_PID


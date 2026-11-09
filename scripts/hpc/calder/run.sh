#!/bin/bash -l
#
# =============================================================================
# GABM — generic Calder (Leeds HPC) launcher
# =============================================================================
#
# WHAT THIS DOES:
#   1. Loads the necessary modules for activating a conda enviornment.
#   2. Starts a vLLM server on a H200 GPU node within an apptainer container. The vLLM server is loaded with the model specified.
#   3. Activates the GABM conda environment.
#   4. Runs the gabm Python process passing in command line arguments.
#   5. Saves results.
#   6. Shuts the server down.
#
# If there is insufficient time to complete the simulation but some days have completed, then to process further a new run has to be started to resume the simulation.
#
# HOW TO RUN IT:
#   1. Download the LLM model you want to use.
#   2. Download a vLLM apptainer sif file to use.
#   3. Download GABM and set up a virtual environment as per the User Guide
# 
# Here is an example command:
# sbatch scripts/hpc/calder/run.sh --model Qwen3-14B --working-dir /scratch-calder/calder-uat/geoagdt/gabm --sif vllm-openai_latest.sif --conda-env gabm --example chat --year 2026 --seed 42
#
# --model if not specified is the Qwen3-14B model
# --working-dir is a directory location where the sif file is located and where results will be written in a gabm_runs folder
# --sif is the name of the sif file to use
# --conda-env is the name of the conda enviornment to activate
# --example is one of: chat, chat_opinion, chat_ensemble, chat_opinion_ensemble
# Other parameters are passed in the selected example command.
#
# To restart a run, pass a previous --outdir value, for example:
# sbatch scripts/hpc/calder/run.sh --model Qwen3-14B --working-dir /scratch-calder/calder-uat/geoagdt/gabm --sif vllm-openai_latest.sif --conda-env gabm --example chat --year 2026 --seed 42 --outdir /scratch-calder/calder-uat/geoagdt/gabm/gabm_runs/run_4751
#
# The following are Slurm parameters to request resources and direct output
# "LLM-" job-name prefix is wanted for LLM jobs (Research Computing policy).
#SBATCH --job-name=LLM-gabm-run
#SBATCH --partition=calder-gpu-hopper
#SBATCH --nodes=1
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
WORKING_DIR="/flash-calder/users/geoagdt/gabm"
#WORKING_DIR="/users/geoagdt/gabm"
SEED="42"
#CONDA_ENV="test-cag"
CONDA_ENV="gabm"
EXAMPLE_MODE="chat"
YEAR="2026"
ROUNDS="8"
START_SEED="42"
N_RUNS="5"

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
    --conda-env)
      [[ -z "$2" ]] && { echo "Missing value for --conda-env"; exit 1; }
      CONDA_ENV="$2"
      shift 2
      ;;
    --example)
      [[ -z "$2" ]] && { echo "Missing value for --example"; exit 1; }
      EXAMPLE_MODE="$2"
      shift 2
      ;;
    --year)
      [[ -z "$2" ]] && { echo "Missing value for --year"; exit 1; }
      YEAR="$2"
      shift 2
      ;;
    --rounds)
      [[ -z "$2" ]] && { echo "Missing value for --rounds"; exit 1; }
      ROUNDS="$2"
      shift 2
      ;;
    --start-seed)
      [[ -z "$2" ]] && { echo "Missing value for --start-seed"; exit 1; }
      START_SEED="$2"
      shift 2
      ;;
    --n-runs)
      [[ -z "$2" ]] && { echo "Missing value for --n-runs"; exit 1; }
      N_RUNS="$2"
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
module load miniforge3

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

# Default
OUTDIR="${WORKING_DIR}/gabm_runs/run_${SLURM_JOB_ID}"
OUTDIR_PASSED=false
# Look for --outdir argument without mutating positional parameters.
for ((i=0; i<${#CLI_ARGS[@]}; i++)); do
  if [[ "${CLI_ARGS[$i]}" == "--outdir" ]] && [[ $((i + 1)) -lt ${#CLI_ARGS[@]} ]]; then
    OUTDIR="${CLI_ARGS[$((i + 1))]}"
    OUTDIR_PASSED=true
  fi
done
echo "Using OUTDIR=$OUTDIR"
if ! $OUTDIR_PASSED; then
  mkdir -p "${OUTDIR}"
  echo "Created OUTDIR"
elif [[ -d "$OUTDIR" ]]; then
  echo "Restarting from existing directory: $OUTDIR"
else
  echo "Error: directory does not exist: $OUTDIR"
  exit 1
fi

# Look for --seed argument without mutating positional parameters.
for ((i=0; i<${#CLI_ARGS[@]}; i++)); do
  if [[ "${CLI_ARGS[$i]}" == "--seed" ]] && [[ $((i + 1)) -lt ${#CLI_ARGS[@]} ]]; then
    SEED="${CLI_ARGS[$((i + 1))]}"
  fi
done
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
  > "${SERVER_LOG}" 2>&1 &

SERVER_PID=$!

# Shutdown
cleanup() {
  kill "${SERVER_PID}" 2>/dev/null || true
  wait "${SERVER_PID}" 2>/dev/null || true
}
trap cleanup EXIT

# Capture exit code of apptainer vllm serve process
EXIT_CODE=$?

END=$(date +%s)

echo "Elapsed: $((END-START)) seconds"

echo "=== End Apptainer ==="
echo "Apptainer exited with code: ${EXIT_CODE}"

echo "=== End memory logging ==="
kill $MONITOR_PID


# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate ${CONDA_ENV}

# Readiness loop
until curl -sf "${BASE_URL}/chat/completions" \
  -H 'Content-Type: application/json' \
  -d "$(python3 -c "
import json
print(json.dumps({
    'model': '${MODEL_NAME}',
    'messages': [{'role': 'user', 'content': 'ping'}],
    'max_tokens': 1
}))
")" >/dev/null 2>&1
do
  sleep 10
done

# Run GABM against local vLLM OpenAI-compatible endpoint.
export OPENAI_BASE_URL="${BASE_URL}"
export OPENAI_API_KEY="${OPENAI_API_KEY:-local}"

ONS_MALE_FILE="${REPO_DIR}/data/input/abm/names_england_wales_ons_male.csv"
ONS_FEMALE_FILE="${REPO_DIR}/data/input/abm/names_england_wales_ons_female.csv"

case "${EXAMPLE_MODE}" in
  chat)
    PYTHONPATH=src python3 src/gabm/examples/chat/sim.py \
      --llm-service openai \
      --model "${MODEL_NAME}" \
      --api-key "${OPENAI_API_KEY}" \
      --seed "${SEED}" \
      --year "${YEAR}" \
      --ons-male-file "${ONS_MALE_FILE}" \
      --ons-female-file "${ONS_FEMALE_FILE}" \
      --output-root "${OUTDIR}" \
      --run-id "chat_seed${SEED}"
    ;;
  chat_opinion)
    PYTHONPATH=src python3 src/gabm/examples/chat_opinion/sim.py \
      --llm-service openai \
      --model "${MODEL_NAME}" \
      --api-key "${OPENAI_API_KEY}" \
      --seed "${SEED}" \
      --year "${YEAR}" \
      --rounds "${ROUNDS}" \
      --ons-male-file "${ONS_MALE_FILE}" \
      --ons-female-file "${ONS_FEMALE_FILE}" \
      --output-root "${OUTDIR}" \
      --run-id "chat_opinion_seed${SEED}"
    ;;
  chat_ensemble)
    PYTHONPATH=src python3 src/gabm/examples/chat/ensembles/similarity_sweep.py \
      --llm-service openai \
      --model "${MODEL_NAME}" \
      --api-key "${OPENAI_API_KEY}" \
      --start-seed "${START_SEED}" \
      --n-runs "${N_RUNS}" \
      --year "${YEAR}" \
      --ons-male-file "${ONS_MALE_FILE}" \
      --ons-female-file "${ONS_FEMALE_FILE}" \
      --output-root "${OUTDIR}" \
      --run-id "chat_ensemble_seed${START_SEED}_n${N_RUNS}"
    ;;
  chat_opinion_ensemble)
    PYTHONPATH=src python3 src/gabm/examples/chat_opinion/ensembles/similarity_sweep.py \
      --llm-service openai \
      --model "${MODEL_NAME}" \
      --api-key "${OPENAI_API_KEY}" \
      --start-seed "${START_SEED}" \
      --n-runs "${N_RUNS}" \
      --year "${YEAR}" \
      --rounds "${ROUNDS}" \
      --ons-male-file "${ONS_MALE_FILE}" \
      --ons-female-file "${ONS_FEMALE_FILE}" \
      --output-root "${OUTDIR}" \
      --run-id "chat_opinion_ensemble_seed${START_SEED}_n${N_RUNS}"
    ;;
  *)
    echo "Unsupported --example value '${EXAMPLE_MODE}'. Use one of: chat, chat_opinion, chat_ensemble, chat_opinion_ensemble"
    exit 1
    ;;
esac


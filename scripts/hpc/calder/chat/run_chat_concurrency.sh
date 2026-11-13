#!/bin/bash -l
#
# =============================================================================
# GABM — Calder concurrent chat launcher
# =============================================================================
#
# WHAT THIS DOES:
#   1. Starts one vLLM server process on the allocated GPU node.
#   2. Launches many chat simulation clients against that one server.
#   3. Runs clients concurrently up to --concurrency.
#   4. Writes per-run output and per-worker logs for analysis.
#
# Typical use (small sanity run):
#   sbatch scripts/hpc/calder/chat/run_chat_concurrency.sh --model Qwen3-14B --n-runs 8 --concurrency 4 --seed-mode increment --seed 42
#
# Chat+opinion determinism test (fixed rounds):
#   sbatch scripts/hpc/calder/chat_opinion/run_chat_opinion_concurrency.sh --rounds 8 --model Qwen3-14B --n-runs 8 --concurrency 4 --seed-mode fixed --seed 42 --llm-seed 42
#
# Determinism test against one server instance:
#   sbatch scripts/hpc/calder/chat/run_chat_concurrency.sh --model Qwen3-14B --n-runs 8 --concurrency 4 --seed-mode fixed --seed 42 --llm-seed 42
#
# Stress test:
#   sbatch scripts/hpc/calder/chat/run_chat_concurrency.sh --model Qwen3-14B --n-runs 40 --concurrency 12 --seed-mode increment --seed 42

#SBATCH --job-name=LLM-gabm-chat-conc
#SBATCH --partition=calder-gpu-hopper
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=4
#SBATCH --cpus-per-task=32
#SBATCH --mem=256G
#SBATCH --time=12:00:00
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

set -euo pipefail
set -x

MODEL_NAME="Qwen3-14B"
SIF_FILE="vllm-openai_v0.33.0.sif"
WORKING_DIR="/flash-calder/users/${USER}/gabm"
CONDA_ENV="gabm"

EXAMPLE_MODE="chat"
YEAR="2026"
ROUNDS="8"
SEED="42"
LLM_SEED=""
N_RUNS="8"
CONCURRENCY="4"
SEED_MODE="increment"
USE_CACHE="false"

EXTRA_SIM_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model)
      [[ -z "${2:-}" ]] && { echo "Missing value for --model"; exit 1; }
      MODEL_NAME="$2"
      shift 2
      ;;
    --sif)
      [[ -z "${2:-}" ]] && { echo "Missing value for --sif"; exit 1; }
      SIF_FILE="$2"
      shift 2
      ;;
    --working-dir)
      [[ -z "${2:-}" ]] && { echo "Missing value for --working-dir"; exit 1; }
      WORKING_DIR="$2"
      shift 2
      ;;
    --conda-env)
      [[ -z "${2:-}" ]] && { echo "Missing value for --conda-env"; exit 1; }
      CONDA_ENV="$2"
      shift 2
      ;;
    --year)
      [[ -z "${2:-}" ]] && { echo "Missing value for --year"; exit 1; }
      YEAR="$2"
      shift 2
      ;;
    --example)
      [[ -z "${2:-}" ]] && { echo "Missing value for --example"; exit 1; }
      EXAMPLE_MODE="$2"
      shift 2
      ;;
    --rounds)
      [[ -z "${2:-}" ]] && { echo "Missing value for --rounds"; exit 1; }
      ROUNDS="$2"
      shift 2
      ;;
    --seed)
      [[ -z "${2:-}" ]] && { echo "Missing value for --seed"; exit 1; }
      SEED="$2"
      shift 2
      ;;
    --llm-seed)
      [[ -z "${2:-}" ]] && { echo "Missing value for --llm-seed"; exit 1; }
      LLM_SEED="$2"
      shift 2
      ;;
    --n-runs)
      [[ -z "${2:-}" ]] && { echo "Missing value for --n-runs"; exit 1; }
      N_RUNS="$2"
      shift 2
      ;;
    --concurrency)
      [[ -z "${2:-}" ]] && { echo "Missing value for --concurrency"; exit 1; }
      CONCURRENCY="$2"
      shift 2
      ;;
    --seed-mode)
      [[ -z "${2:-}" ]] && { echo "Missing value for --seed-mode"; exit 1; }
      SEED_MODE="$2"
      shift 2
      ;;
    --use-cache)
      USE_CACHE="true"
      shift
      ;;
    --)
      shift
      while [[ $# -gt 0 ]]; do
        EXTRA_SIM_ARGS+=("$1")
        shift
      done
      ;;
    *)
      EXTRA_SIM_ARGS+=("$1")
      shift
      ;;
  esac
done

if [[ "$SEED_MODE" != "fixed" && "$SEED_MODE" != "increment" ]]; then
  echo "Unsupported --seed-mode '$SEED_MODE'. Use one of: fixed, increment"
  exit 1
fi

if [[ "$EXAMPLE_MODE" != "chat" && "$EXAMPLE_MODE" != "chat_opinion" ]]; then
  echo "Unsupported --example '$EXAMPLE_MODE'. Use one of: chat, chat_opinion"
  exit 1
fi

if ! [[ "$N_RUNS" =~ ^[0-9]+$ ]] || [[ "$N_RUNS" -lt 1 ]]; then
  echo "--n-runs must be a positive integer"
  exit 1
fi

if ! [[ "$CONCURRENCY" =~ ^[0-9]+$ ]] || [[ "$CONCURRENCY" -lt 1 ]]; then
  echo "--concurrency must be a positive integer"
  exit 1
fi

module load calder/hopper
module load cuda/13.3.0
module load nccl/2.29.7-1
module load miniforge3

export PYTHONUNBUFFERED=1
export APPTAINERENV_PYTHONUNBUFFERED=1
export APPTAINERENV_CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES

REPO_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$REPO_DIR"

MODEL_DIR="${WORKING_DIR}/huggingface/hub/${MODEL_NAME}"
SIF_IMAGE="${WORKING_DIR}/${SIF_FILE}"
PORT=$((10000 + SLURM_JOB_ID % 50000))
BASE_URL="http://localhost:${PORT}/v1"

OUTDIR="${WORKING_DIR}/gabm_runs/run_${SLURM_JOB_ID}"
CLIENT_OUT_ROOT="${OUTDIR}/clients"
mkdir -p "$CLIENT_OUT_ROOT"

SERVER_LOG="${OUTDIR}/vllm_server.log"
LAUNCHER_LOG="${OUTDIR}/launcher_summary.log"

echo "=== Configuration ===" | tee -a "$LAUNCHER_LOG"
echo "MODEL_NAME=${MODEL_NAME}" | tee -a "$LAUNCHER_LOG"
echo "EXAMPLE_MODE=${EXAMPLE_MODE}" | tee -a "$LAUNCHER_LOG"
echo "WORKING_DIR=${WORKING_DIR}" | tee -a "$LAUNCHER_LOG"
echo "OUTDIR=${OUTDIR}" | tee -a "$LAUNCHER_LOG"
echo "N_RUNS=${N_RUNS}" | tee -a "$LAUNCHER_LOG"
echo "CONCURRENCY=${CONCURRENCY}" | tee -a "$LAUNCHER_LOG"
echo "ROUNDS=${ROUNDS}" | tee -a "$LAUNCHER_LOG"
echo "SEED_MODE=${SEED_MODE}" | tee -a "$LAUNCHER_LOG"
echo "USE_CACHE=${USE_CACHE}" | tee -a "$LAUNCHER_LOG"
echo "BASE_URL=${BASE_URL}" | tee -a "$LAUNCHER_LOG"

echo "=== Node information ===" | tee -a "$LAUNCHER_LOG"
nvidia-smi -L | tee -a "$LAUNCHER_LOG"
lscpu | grep "^CPU(s):" | tee -a "$LAUNCHER_LOG"
free -h | tee -a "$LAUNCHER_LOG"

echo "=== Start memory logging ===" | tee -a "$LAUNCHER_LOG"
MEMORY_LOG="${OUTDIR}/gpu_memory.log"
(
while true
do
  date
  nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader
  sleep 30
done
) > "$MEMORY_LOG" &
MONITOR_PID=$!

echo "=== Start vLLM server ===" | tee -a "$LAUNCHER_LOG"
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

cleanup() {
  kill "${MONITOR_PID}" 2>/dev/null || true
  kill "${SERVER_PID}" 2>/dev/null || true
  wait "${SERVER_PID}" 2>/dev/null || true
}
trap cleanup EXIT

echo "=== Activate conda ===" | tee -a "$LAUNCHER_LOG"
eval "$(conda shell.bash hook)"
conda activate "${CONDA_ENV}"

echo "=== Wait for server readiness ===" | tee -a "$LAUNCHER_LOG"
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

export OPENAI_BASE_URL="${BASE_URL}"
export OPENAI_API_KEY="${OPENAI_API_KEY:-local}"

ONS_MALE_FILE="${REPO_DIR}/data/input/abm/names_england_wales_ons_male.csv"
ONS_FEMALE_FILE="${REPO_DIR}/data/input/abm/names_england_wales_ons_female.csv"

run_one() {
  local run_index="$1"
  local sim_seed="$2"
  local run_id
  run_id=$(printf "%s_i%03d_seed%s" "$EXAMPLE_MODE" "$run_index" "$sim_seed")
  local run_log="${CLIENT_OUT_ROOT}/${run_id}.log"

  local sim_script="src/gabm/examples/chat/sim.py"
  if [[ "$EXAMPLE_MODE" == "chat_opinion" ]]; then
    sim_script="src/gabm/examples/chat_opinion/sim.py"
  fi

  local cmd=(
    python3 "$sim_script"
    --llm-service openai
    --model "${MODEL_NAME}"
    --api-key "${OPENAI_API_KEY}"
    --seed "${sim_seed}"
    --year "${YEAR}"
    --ons-male-file "${ONS_MALE_FILE}"
    --ons-female-file "${ONS_FEMALE_FILE}"
    --output-root "${CLIENT_OUT_ROOT}"
    --run-id "${run_id}"
  )

  if [[ "$EXAMPLE_MODE" == "chat_opinion" ]]; then
    cmd+=(--rounds "${ROUNDS}")
  fi

  if [[ "$USE_CACHE" == "false" ]]; then
    cmd+=(--no-cache)
  fi

  if [[ -n "$LLM_SEED" ]]; then
    cmd+=(--llm-seed "$LLM_SEED")
  fi

  if [[ ${#EXTRA_SIM_ARGS[@]} -gt 0 ]]; then
    cmd+=("${EXTRA_SIM_ARGS[@]}")
  fi

  PYTHONPATH=src "${cmd[@]}" >"${run_log}" 2>&1
}

echo "=== Launch concurrent clients ===" | tee -a "$LAUNCHER_LOG"
declare -a worker_pids=()
declare -a worker_desc=()

active_worker_count() {
  local count=0
  local pid
  for pid in "${worker_pids[@]}"; do
    if kill -0 "$pid" 2>/dev/null; then
      count=$((count + 1))
    fi
  done
  echo "$count"
}

for ((i=0; i<N_RUNS; i++)); do
  if [[ "$SEED_MODE" == "fixed" ]]; then
    sim_seed="$SEED"
  else
    sim_seed=$((SEED + i))
  fi

  run_one "$i" "$sim_seed" &
  pid=$!
  worker_pids+=("$pid")
  worker_desc+=("i=$i,seed=$sim_seed,pid=$pid")

  while [[ "$(active_worker_count)" -ge "$CONCURRENCY" ]]; do
    if ! wait -n; then
      :
    fi
  done
done

failures=0
for pid in "${worker_pids[@]}"; do
  if ! wait "$pid"; then
    failures=$((failures + 1))
  fi
done

successes=$((N_RUNS - failures))

echo "=== Worker summary ===" | tee -a "$LAUNCHER_LOG"
echo "SUCCESSFUL_RUNS=${successes}" | tee -a "$LAUNCHER_LOG"
echo "FAILED_RUNS=${failures}" | tee -a "$LAUNCHER_LOG"
printf '%s\n' "${worker_desc[@]}" | tee -a "$LAUNCHER_LOG"

if [[ "$failures" -gt 0 ]]; then
  echo "One or more workers failed. Check logs under ${CLIENT_OUT_ROOT}" | tee -a "$LAUNCHER_LOG"
  exit 1
fi

echo "All workers completed successfully." | tee -a "$LAUNCHER_LOG"

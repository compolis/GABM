#!/bin/bash -l
#
# =============================================================================
# GABM — AIRE concurrent chat launcher (with local scratch stage-in/out)
# =============================================================================
#
# WHAT THIS DOES:
#   1. Stages a minimal repo working set to node-local scratch (${TMPDIR}).
#   2. Starts one vLLM server process on the allocated GPU node.
#   3. Launches many simulation clients against that one server.
#   4. Runs clients concurrently up to --concurrency.
#   5. Copies run artifacts from local scratch back to shared storage.
#
# Typical use:
#   sbatch scripts/hpc/aire/chat/run_chat_concurrency.sh \
#     --model Qwen3-14B --n-runs 8 --concurrency 2 --seed-mode increment --seed 42
#
# chat_opinion fixed-seed determinism:
#   sbatch scripts/hpc/aire/chat/run_chat_concurrency.sh \
#     --example chat_opinion --rounds 8 --model Qwen3-14B \
#     --n-runs 8 --concurrency 2 --seed-mode fixed --seed 42 --llm-seed 42

#SBATCH --job-name=LLM-gabm-chat-conc
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-task=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=80G
#SBATCH --time=04:00:00
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

set -euo pipefail
set -x

MODEL_NAME="Qwen3-14B"
SIF_FILE="vllm-openai_latest.sif"
SHARED_WORKING_DIR="${SHARED_WORKING_DIR:-${SCRATCH:-$HOME}/gabm}"
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
    --shared-working-dir)
      [[ -z "${2:-}" ]] && { echo "Missing value for --shared-working-dir"; exit 1; }
      SHARED_WORKING_DIR="$2"
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

module add apptainer
module load miniforge

export PYTHONUNBUFFERED=1
export APPTAINERENV_PYTHONUNBUFFERED=1
export APPTAINERENV_CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}"

REPO_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
MODEL_DIR="${MODEL_DIR:-${SHARED_WORKING_DIR}/huggingface/hub/${MODEL_NAME}}"
SIF_IMAGE="${SIF_IMAGE:-${SHARED_WORKING_DIR}/${SIF_FILE}}"
PORT=$((10000 + SLURM_JOB_ID % 50000))
BASE_URL="http://localhost:${PORT}/v1"

OUTDIR="${SHARED_WORKING_DIR}/gabm_runs/run_${SLURM_JOB_ID}"
LOCAL_ROOT="${TMPDIR:-/tmp}/${USER}/gabm_${SLURM_JOB_ID}"
LOCAL_REPO="${LOCAL_ROOT}/repo"
LOCAL_OUT="${LOCAL_ROOT}/run"
CLIENT_OUT_ROOT="${LOCAL_OUT}/clients"

mkdir -p "$OUTDIR" "$LOCAL_REPO" "$CLIENT_OUT_ROOT"

SERVER_LOG="${OUTDIR}/vllm_server.log"
LAUNCHER_LOG="${OUTDIR}/launcher_summary.log"

echo "=== Stage in to local scratch ===" | tee -a "$LAUNCHER_LOG"
rsync -a --delete "${REPO_DIR}/src/" "${LOCAL_REPO}/src/"
mkdir -p "${LOCAL_REPO}/data"
rsync -a --delete "${REPO_DIR}/data/input/" "${LOCAL_REPO}/data/input/"

echo "=== Configuration ===" | tee -a "$LAUNCHER_LOG"
echo "MODEL_NAME=${MODEL_NAME}" | tee -a "$LAUNCHER_LOG"
echo "EXAMPLE_MODE=${EXAMPLE_MODE}" | tee -a "$LAUNCHER_LOG"
echo "REPO_DIR=${REPO_DIR}" | tee -a "$LAUNCHER_LOG"
echo "LOCAL_REPO=${LOCAL_REPO}" | tee -a "$LAUNCHER_LOG"
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

if [[ ! -d "$MODEL_DIR" ]]; then
  echo "Model directory not found: $MODEL_DIR" | tee -a "$LAUNCHER_LOG"
  exit 1
fi

if [[ ! -f "$SIF_IMAGE" ]]; then
  echo "Container image not found: $SIF_IMAGE" | tee -a "$LAUNCHER_LOG"
  exit 1
fi

echo "=== Start vLLM server ===" | tee -a "$LAUNCHER_LOG"
apptainer exec \
  --cleanenv \
  --nv \
  -B "${SHARED_WORKING_DIR}:${SHARED_WORKING_DIR}" \
  --env VLLM_ENABLE_V1_MULTIPROCESSING=0 \
  --env VLLM_BATCH_INVARIANT=1 \
  "${SIF_IMAGE}" \
  vllm serve "$MODEL_DIR" \
  --seed "${SEED}" \
  --served-model-name "${MODEL_NAME}" \
  --tensor-parallel-size "${SLURM_GPUS_PER_TASK:-1}" \
  --compilation-config.pass_config.fuse_allreduce_rms=false \
  --chat-template-content-format string \
  --gpu-memory-utilization 0.9 \
  --port "${PORT}" \
  > "${SERVER_LOG}" 2>&1 &
SERVER_PID=$!

stage_out() {
  if [[ -d "$LOCAL_OUT" ]]; then
    rsync -a "$LOCAL_OUT/" "$OUTDIR/"
  fi
}

cleanup() {
  kill "${MONITOR_PID}" 2>/dev/null || true
  kill "${SERVER_PID}" 2>/dev/null || true
  wait "${SERVER_PID}" 2>/dev/null || true
  stage_out
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
  if ! kill -0 "${SERVER_PID}" 2>/dev/null; then
    echo "vLLM server exited before readiness. Last log lines:" | tee -a "$LAUNCHER_LOG"
    tail -n 30 "$SERVER_LOG" | tee -a "$LAUNCHER_LOG"
    exit 1
  fi
  sleep 10
done

export OPENAI_BASE_URL="${BASE_URL}"
export OPENAI_API_KEY="${OPENAI_API_KEY:-local}"

ONS_MALE_FILE="${LOCAL_REPO}/data/input/abm/names_england_wales_ons_male.csv"
ONS_FEMALE_FILE="${LOCAL_REPO}/data/input/abm/names_england_wales_ons_female.csv"

run_one() {
  local run_index="$1"
  local sim_seed="$2"
  local run_id
  run_id=$(printf "%s_i%03d_seed%s" "$EXAMPLE_MODE" "$run_index" "$sim_seed")
  local run_log="${CLIENT_OUT_ROOT}/${run_id}.log"

  local sim_script="${LOCAL_REPO}/src/gabm/examples/chat/sim.py"
  if [[ "$EXAMPLE_MODE" == "chat_opinion" ]]; then
    sim_script="${LOCAL_REPO}/src/gabm/examples/chat_opinion/sim.py"
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

  PYTHONPATH="${LOCAL_REPO}/src" "${cmd[@]}" >"${run_log}" 2>&1
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
  echo "One or more workers failed. Check logs under ${OUTDIR}/clients" | tee -a "$LAUNCHER_LOG"
  exit 1
fi

echo "All workers completed successfully." | tee -a "$LAUNCHER_LOG"

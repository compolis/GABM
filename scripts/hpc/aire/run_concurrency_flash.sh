#!/bin/bash -l
#
# Aire high-performance concurrency entrypoint.
# Stages selected heavy assets (SIF + model) from persistent scratch to
# node-local flash scratch (preferably $TMP_SHARED on Aire), runs the standard
# Aire concurrency launcher from flash, then stages run outputs back to
# persistent scratch.

#SBATCH --job-name=LLM-gabm-air-flash
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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_SCRIPT="${SCRIPT_DIR}/run_concurrency.sh"
if [[ -n "${SLURM_SUBMIT_DIR:-}" ]]; then
  SUBMIT_BASE_SCRIPT="${SLURM_SUBMIT_DIR}/scripts/hpc/aire/run_concurrency.sh"
  if [[ -f "$SUBMIT_BASE_SCRIPT" ]]; then
    BASE_SCRIPT="$SUBMIT_BASE_SCRIPT"
  fi
fi

if [[ ! -f "$BASE_SCRIPT" ]]; then
  echo "Missing base script: $BASE_SCRIPT" >&2
  exit 1
fi

MODEL_NAME="Qwen3-14B"
SIF_FILE="vllm-openai_v0.11.0.sif"
PERSIST_WORKING_DIR="${PERSIST_WORKING_DIR:-/mnt/scratch/$USER/gabm}"
KEEP_FLASH_WORKDIR="${KEEP_FLASH_WORKDIR:-false}"

FORWARD_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model)
      [[ -z "${2:-}" ]] && { echo "Missing value for --model"; exit 1; }
      MODEL_NAME="$2"
      FORWARD_ARGS+=("$1" "$2")
      shift 2
      ;;
    --sif)
      [[ -z "${2:-}" ]] && { echo "Missing value for --sif"; exit 1; }
      SIF_FILE="$2"
      FORWARD_ARGS+=("$1" "$2")
      shift 2
      ;;
    --shared-working-dir)
      [[ -z "${2:-}" ]] && { echo "Missing value for --shared-working-dir"; exit 1; }
      PERSIST_WORKING_DIR="$2"
      shift 2
      ;;
    *)
      FORWARD_ARGS+=("$1")
      shift
      ;;
  esac
done

JOB_ID="${SLURM_JOB_ID:-manual}"
if [[ -n "${FLASH_BASE:-}" ]]; then
  RESOLVED_FLASH_BASE="$FLASH_BASE"
else
  CANDIDATE_FLASH_BASES=()
  if [[ -n "${TMP_SHARED:-}" ]]; then
    CANDIDATE_FLASH_BASES+=("$TMP_SHARED")
  fi
  CANDIDATE_FLASH_BASES+=("/mnt/flash/tmp/job.${JOB_ID}" "/flash")

  RESOLVED_FLASH_BASE=""
  for candidate in "${CANDIDATE_FLASH_BASES[@]}"; do
    if mkdir -p "$candidate" 2>/dev/null; then
      RESOLVED_FLASH_BASE="$candidate"
      break
    fi
  done

  if [[ -z "$RESOLVED_FLASH_BASE" ]]; then
    echo "Could not find writable FLASH_BASE. Tried: ${CANDIDATE_FLASH_BASES[*]}" >&2
    echo "Set FLASH_BASE explicitly, e.g. --export=ALL,FLASH_BASE=/mnt/flash/tmp/job.\$SLURM_JOB_ID" >&2
    exit 1
  fi
fi

FLASH_BASE="$RESOLVED_FLASH_BASE"
FLASH_WORKING_DIR="${FLASH_BASE}/gabm_flash_${JOB_ID}"
FLASH_HUB="${FLASH_WORKING_DIR}/huggingface/hub"
FLASH_MODEL_DIR="${FLASH_HUB}/${MODEL_NAME}"
FLASH_SIF_IMAGE="${FLASH_WORKING_DIR}/${SIF_FILE}"

PERSIST_MODEL_DIR="${MODEL_DIR_SRC:-${PERSIST_WORKING_DIR}/huggingface/hub/${MODEL_NAME}}"
PERSIST_SIF_IMAGE="${SIF_IMAGE_SRC:-${PERSIST_WORKING_DIR}/${SIF_FILE}}"
PERSIST_OUT_ROOT="${PERSIST_WORKING_DIR}/gabm_runs"
FLASH_RUN_DIR="${FLASH_WORKING_DIR}/gabm_runs/run_${JOB_ID}"
FLASH_TIMING_LOG="${FLASH_RUN_DIR}/flash_stage_timing.log"
OVERALL_START_TS="$(date +%s)"
STAGE_IN_MODEL_SEC=0
STAGE_IN_SIF_SEC=0
CORE_RUN_SEC=0
STAGE_OUT_SEC=0

if [[ ! -d "$PERSIST_MODEL_DIR" ]]; then
  echo "Model directory not found on persistent scratch: $PERSIST_MODEL_DIR" >&2
  exit 1
fi

if [[ ! -f "$PERSIST_SIF_IMAGE" ]]; then
  echo "Container image not found on persistent scratch: $PERSIST_SIF_IMAGE" >&2
  exit 1
fi

mkdir -p "$FLASH_HUB" "$PERSIST_OUT_ROOT"

echo "[flash-stage] Using FLASH_BASE: $FLASH_BASE"
echo "[flash-stage] Staging model from persistent scratch to flash..."
stage_start_ts="$(date +%s)"
rsync -a --delete "$PERSIST_MODEL_DIR/" "${FLASH_MODEL_DIR}/"
STAGE_IN_MODEL_SEC="$(( $(date +%s) - stage_start_ts ))"

echo "[flash-stage] Staging SIF from persistent scratch to flash..."
stage_start_ts="$(date +%s)"
rsync -a "$PERSIST_SIF_IMAGE" "$FLASH_SIF_IMAGE"
STAGE_IN_SIF_SEC="$(( $(date +%s) - stage_start_ts ))"

stage_out() {
  local stage_start_ts
  stage_start_ts="$(date +%s)"
  mkdir -p "$PERSIST_OUT_ROOT/run_${JOB_ID}"
  mkdir -p "$FLASH_RUN_DIR"
  {
    echo "JOB_ID=${JOB_ID}"
    echo "FLASH_BASE=${FLASH_BASE}"
    echo "PERSIST_WORKING_DIR=${PERSIST_WORKING_DIR}"
    echo "STAGE_IN_MODEL_SEC=${STAGE_IN_MODEL_SEC}"
    echo "STAGE_IN_SIF_SEC=${STAGE_IN_SIF_SEC}"
    echo "CORE_RUN_SEC=${CORE_RUN_SEC}"
    echo "STAGE_OUT_SEC=PENDING"
    echo "TOTAL_SEC_SO_FAR=$(( $(date +%s) - OVERALL_START_TS ))"
  } > "$FLASH_TIMING_LOG"
  rsync -a "${FLASH_RUN_DIR}/" "${PERSIST_OUT_ROOT}/run_${JOB_ID}/"
  STAGE_OUT_SEC="$(( $(date +%s) - stage_start_ts ))"
  {
    echo "JOB_ID=${JOB_ID}"
    echo "FLASH_BASE=${FLASH_BASE}"
    echo "PERSIST_WORKING_DIR=${PERSIST_WORKING_DIR}"
    echo "STAGE_IN_MODEL_SEC=${STAGE_IN_MODEL_SEC}"
    echo "STAGE_IN_SIF_SEC=${STAGE_IN_SIF_SEC}"
    echo "CORE_RUN_SEC=${CORE_RUN_SEC}"
    echo "STAGE_OUT_SEC=${STAGE_OUT_SEC}"
    echo "TOTAL_SEC=$(( $(date +%s) - OVERALL_START_TS ))"
  } > "${PERSIST_OUT_ROOT}/run_${JOB_ID}/flash_stage_timing.log"
}

cleanup() {
  stage_out
  if [[ "$KEEP_FLASH_WORKDIR" != "true" ]]; then
    rm -rf "$FLASH_WORKING_DIR"
  else
    echo "[flash-stage] KEEP_FLASH_WORKDIR=true, preserving ${FLASH_WORKING_DIR}"
  fi
}
trap cleanup EXIT

echo "[flash-stage] Running from flash working dir: $FLASH_WORKING_DIR"
echo "[flash-stage] Persistent output root: $PERSIST_OUT_ROOT"

stage_start_ts="$(date +%s)"
SHARED_WORKING_DIR="$FLASH_WORKING_DIR" \
MODEL_DIR="$FLASH_MODEL_DIR" \
SIF_IMAGE="$FLASH_SIF_IMAGE" \
"$BASE_SCRIPT" "${FORWARD_ARGS[@]}"
CORE_RUN_SEC="$(( $(date +%s) - stage_start_ts ))"

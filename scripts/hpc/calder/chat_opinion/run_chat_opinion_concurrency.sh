#!/bin/bash -l
#
# Convenience wrapper for chat_opinion concurrent runs on Calder.
#
# Usage example:
#   sbatch scripts/hpc/calder/chat_opinion/run_chat_opinion_concurrency.sh \
#     --model Qwen3-14B --rounds 8 --n-runs 8 --concurrency 4 --seed-mode fixed --seed 42 --llm-seed 42

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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../../../../" && pwd)"
CHAT_CONC_SCRIPT="${ROOT_DIR}/scripts/hpc/calder/chat/run_chat_concurrency.sh"

if [[ ! -f "${CHAT_CONC_SCRIPT}" ]]; then
  echo "Missing base script: ${CHAT_CONC_SCRIPT}"
  exit 1
fi

exec "${CHAT_CONC_SCRIPT}" --example chat_opinion "$@"

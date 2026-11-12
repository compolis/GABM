#!/bin/bash -l
#
# Convenience wrapper for running chat_opinion concurrency jobs on AIRE.

#SBATCH --job-name=LLM-gabm-chat-opinion-conc
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
BASE_SCRIPT="${SCRIPT_DIR}/../chat/run_chat_concurrency.sh"

if [[ ! -f "$BASE_SCRIPT" ]]; then
  echo "Missing base script: $BASE_SCRIPT" >&2
  exit 1
fi

exec "$BASE_SCRIPT" --example chat_opinion "$@"

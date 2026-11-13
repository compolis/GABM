#!/bin/bash -l
#
# Canonical Calder concurrency entrypoint.
# Backward-compatible wrapper to the chat concurrency launcher.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_SCRIPT="${SCRIPT_DIR}/chat/run_chat_concurrency.sh"
if [[ -n "${SLURM_SUBMIT_DIR:-}" ]]; then
  SUBMIT_BASE_SCRIPT="${SLURM_SUBMIT_DIR}/scripts/hpc/calder/chat/run_chat_concurrency.sh"
  if [[ -f "$SUBMIT_BASE_SCRIPT" ]]; then
    BASE_SCRIPT="$SUBMIT_BASE_SCRIPT"
  fi
fi

if [[ ! -f "$BASE_SCRIPT" ]]; then
  echo "Missing base script: $BASE_SCRIPT" >&2
  exit 1
fi

exec "$BASE_SCRIPT" "$@"

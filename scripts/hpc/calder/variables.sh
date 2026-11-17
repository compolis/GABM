#!/bin/bash
#
# Calder-specific vLLM runtime defaults.

readonly VLLM_VERSION="0.33.0"
readonly VLLM_SIF="vllm-openai_v${VLLM_VERSION}.sif"
readonly DEFAULT_WORKING_DIR="/flash-calder/users/${USER}/gabm"
readonly DEFAULT_CONDA_ENV="gabm-calder"

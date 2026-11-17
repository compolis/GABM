#!/bin/bash
#
# Aire-specific vLLM runtime defaults.

readonly VLLM_VERSION="0.11.0"
readonly VLLM_SIF="vllm-openai_v${VLLM_VERSION}.sif"
readonly DEFAULT_WORKING_DIR="/mnt/scratch/${USER}/gabm"
readonly DEFAULT_CONDA_ENV="gabm-aire"

#!/bin/bash
#
# =============================================================================
# GABM — reproducibility test Calder (Leeds HPC) launcher
# =============================================================================
#
# WHAT THIS DOES:
#   1. Activates the GABM conda environment.
#   2. Runs the GABM Python process passing in command line arguments.
#   3. Saves results.
#
# HOW TO RUN IT:
#   1. You need to already have started the server and know which node it is running on and which port the server is using.
#   2. Example run:
#
# To check reproducibility/variety:
#   1. Run the same thing twice with n > 1
#   2. For any run compare the output from any two files to check that there is a difference. If there is a difference then changing the seed creates variety.
#      diff results/seed_42000.out results/seed_43000.out
#   3. Compare all the results for the two runs. These should be identical. Increase n for a larger test.
#      diff -r run1 run2
#      sha256sum run1/*.out
#      sha256sum run1/*.out
# 
# On login node
# bash scripts/calder/run_client.sh --node calder-h200-05 --port 15882 --working-dir /scratch-calder/calder-uat/geoagdt/gabm --conda-env test-cag --prompt "What is gravity?" --model Qwen3-14B --n 2 --seed 42 > 1.out
# bash scripts/calder/run_client.sh --node calder-h200-05 --port 15882 --working-dir /scratch-calder/calder-uat/geoagdt/gabm --conda-env test-cag --prompt "What is gravity?" --model Qwen3-14B --n 2 --seed 42 > 2.out
# diff 1.out 2.out
# Via slurm
# sbatch scripts/calder/run_client.sh --node calder-h200-05 --port 15882 --working-dir /scratch-calder/calder-uat/geoagdt/gabm --conda-env test-cag --prompt "What is gravity?" --model Qwen3-14B --n 2 --seed 42
# sbatch scripts/calder/run_client.sh --node calder-h200-05 --port 15882 --working-dir /scratch-calder/calder-uat/geoagdt/gabm --conda-env test-cag --prompt "What is gravity?" --model Qwen3-14B --n 2 --seed 42
#     
# --node 	The node on which the server is running 
# --port	The port over which the server communicates
# --working-dir The working directory.
# --conda-env   The conda enviornment with python and jq
# --prompt      The prompt to test.
# --model	The LLM model to test
# --n           The number of times the prompt is used to get a response and weights.
# --seed	Used to start the seed.
#
# The following is if this is submitted as a CPU job rather than run on a login node.
# "LLM-" job-name prefix is wanted for LLM jobs (Research Computing policy).
#SBATCH --job-name=LLM-gabm-client
# Best to run this either on a login node or on the amd_turin_9555 partition.
#SBATCH --partition=calder-cpu-turin
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=10G
#SBATCH --time=00:10:00
# When testing this script it seems /scratch-calder is not available from the amd_genoa_9634 partition, so output is explicitly written to /users.
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

set -x

#ls ~/scratch-calder
#ls /scratch-calder

echo "HOSTNAME=$(hostname)"
echo "PWD=$(pwd)"

python --version
jq --version


# Load modules
module load calder/cpu
module load miniforge3

# Defaults
NODE="calder-h200-05"
#PORT="8000"
PORT="15882"
#MODEL="Apertus-v1.5-70B"
MODEL="Qwen3-14B"

# Check Arguments
CLI_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --node)
      [[ -z "$2" ]] && { echo "Missing value for --node"; exit 1; }
      NODE="$2"
      shift 2
      ;;
    --port)
      [[ -z "$2" ]] && { echo "Missing value for --port"; exit 1; }
      PORT="$2"
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
    --prompt)
      [[ -z "$2" ]] && { echo "Missing value for --prompt"; exit 1; }
      PROMPT="$2"
      shift 2
      ;;
    --model)
      [[ -z "$2" ]] && { echo "Missing value for --model"; exit 1; }
      MODEL="$2"
      shift 2
      ;;
    --n)
      [[ -z "$2" ]] && { echo "Missing value for --n"; exit 1; }
      N="$2"
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

# Set OUTDIR
if [[ -n "${SLURM_JOB_ID:-}" ]]; then
  RUN_ID="$SLURM_JOB_ID"
else
  RUN_ID=$(date +%Y%m%d_%H%M%S)
fi
OUTDIR="${WORKING_DIR}/cag_runs/run_${RUN_ID}"
mkdir -p "${OUTDIR}"
echo "Using OUTDIR ${OUTDIR}"

echo "CONDA_ENV=$CONDA_ENV"
conda info --envs
#conda activate $CONDA_ENV 
conda activate $HOME/.conda/envs/$CONDA_ENV
which python
which jq
which curl

python --version
jq --version

echo "Prompt: \"$PROMPT\""

URL="http://${NODE}:${PORT}/v1/completions"

for ((i=1; i<=$N; i++))
do
  SEED2=$((($SEED+i)*1000))
  outfile="${OUTDIR}/seed_${SEED2}.out"
  echo "Run $i (seed=$SEED2) -> $outfile"
  #set -x
  payload=$(jq -n \
    --arg prompt "$PROMPT" \
    --arg model $MODEL \
    --argjson seed $SEED2 \
    '{
      model: $model,
      prompt: $prompt,
      max_tokens: 100,
      temperature: 0.5,
      seed: $seed,
      "logprobs": 20
    }')
  # Check outfile
  echo "outfile=<$outfile>"
  ls -ld "$(dirname "$outfile")"
  touch "$outfile"
  ls -l "$outfile"
  # Get response
  curl -s "$URL" \
    -H "Content-Type: application/json" \
    -d "$payload" \
  | python -c '
import json,sys,pprint
resp=json.load(sys.stdin)
print("TEXT:")
print(resp["choices"][0]["text"])
print("\nLOGPROBS:")
pprint.pp(resp["choices"][0].get("logprobs"))
' > "$outfile"

done


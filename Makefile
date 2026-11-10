# Makefile for common development tasks
# Usage:
#   make help            - Show this help message
#   make test            - Run tests (pytest)
#   make docs            - Build documentation (Sphinx)
#   make docs-clean      - Clean auto-copied documentation files from docs/
#   make gh-pages-deploy - Build and deploy documentation to GitHub Pages
#   make clean           - Remove build/test artifacts
#   make clear-caches    - Delete all LLM caches and model lists (for a clean slate)
#   make llm-drift-check - Clear caches and run live LLM integration tests
#   make git-clean       - Clean up merged local branches and prune deleted remotes
#   make sync            - Sync main branch with upstream
#   make sync-feature    - Sync and rebase a feature/release branch onto main (usage: make sync-feature BRANCH=release/0.2.0)
#   make setup-llms      - Run onboarding/setup for all LLMs (API key check, model lists, cache init)
#   make release         - Tag and push a release (usage: make release VERSION=x.y.z BRANCH=release/x.y.z)
#   make delete-release  - Delete a release tag locally and on remotes (usage: make delete-release VERSION=x.y.z)
#
# Note: This Makefile assumes you have the necessary Python dependencies installed (e.g., pytest, Sphinx) and that you have set up git remotes correctly for syncing and releasing.
#
# Targets are ordered by typical workflow: testing, documentation, cleaning, git maintenance, syncing, and releasing.
#
# The Makefile targets are explained in more detail in the DEV_GUIDE.md
#
# If you add a new target, please also add it to the help target and the DEV_GUIDE.md for consistency and ease of use for other developers.
#
# Caution: Some commands (like git-clean, release, and delete-release) can modify your git history or delete tags. Always review the scripts they call (in the scripts/ directory) to ensure they do what you expect before running these commands.

# Phony targets (not actual files)
.PHONY: help test docs docs-clean gh-pages-deploy gh-pages-deploy2 clean git-clean setup-llms clear-caches llm-drift-check sync sync-feature release delete-release build build-test pypi-release testpypi-release bump-version run-local run-installed run-example-chat run-example-chat-ensemble run-example-chat-opinion run-example-chat-opinion-ensemble compare-example-chat compare-ensemble-sweeps compare-hpc-chat-runs summarize-hpc-concurrency report-hpc-chat-runs summarize-chat-opinion-runs

# Show available Makefile commands
help:
	@echo "Available targets:"
	@echo "  test             - Run tests (pytest)"
	@echo "  docs             - Build documentation (Sphinx)"
	@echo "  docs-clean       - Clean auto-copied documentation files from docs/"
	@echo "  gh-pages-deploy  - Build and deploy documentation to GitHub Pages"
	@echo "  gh-pages-deploy2 - Build and deploy documentation to GitHub Pages on upstream remote (force push)"
	@echo "  clean            - Remove build/test artifacts"
	@echo "  clear-caches     - Delete all LLM caches and model lists (for a clean slate)"
	@echo "  llm-drift-check  - Clear caches and run live LLM integration tests"
	@echo "  git-clean        - Clean up merged local branches and prune deleted remotes"
	@echo "  sync             - Sync main branch with upstream"
	@echo "  sync-feature     - Sync and rebase a feature/release branch onto main (usage: make sync-feature BRANCH=release/0.2.0)"
	@echo "  setup-llms       - Run onboarding/setup for all LLMs (API key check, model lists, cache init)"
	@echo "  release          - Tag and push a release (usage: make release VERSION=x.y.z BRANCH=release/x.y.z)"
	@echo "  delete-release   - Delete a release tag locally and on remotes (usage: make delete-release VERSION=x.y.z)"
	@echo "  build            - Build a distribution package for PyPI (python -m build)"
	@echo "  build-test       - Build and test install the package in a fresh venv"
	@echo "  pypi-release     - Upload the built package to PyPI (twine upload dist/*)"
	@echo "  testpypi-release - Upload the built package to TestPyPI (twine upload --repository testpypi dist/*)"
	@echo "  bump-version     - Bump the project version (usage: make bump-version part=patch|minor|major)"
	@echo "  run-local        - Run gabm using local source (development mode)"
	@echo "  run-installed    - Run gabm using installed package (production mode)"
	@echo "  run-example-chat - Run chat example (usage: make run-example-chat SEED=42 YEAR=2026 ONS_MALE=... ONS_FEMALE=... OUTPUT_ROOT=... RUN_ID=... NO_CACHE=1)"
	@echo "  run-example-chat-ensemble - Run chat ensemble sweep (usage: make run-example-chat-ensemble START_SEED=100 N_RUNS=25 OUTPUT_ROOT=... RUN_ID=... NO_CACHE=1 LLM_SEED=42)"
	@echo "  run-example-chat-opinion - Run chat+opinion example (usage: make run-example-chat-opinion SEED=42 YEAR=2026 ROUNDS=8 CONVERSATION_MODE=normal PAIRING_STRATEGY=random CANDIDATE_POOL_SIZE=8 OUTPUT_ROOT=... RUN_ID=... NO_CACHE=1 LLM_SEED=42)"
	@echo "  run-example-chat-opinion-ensemble - Run ensemble similarity sweep (usage: make run-example-chat-opinion-ensemble START_SEED=100 N_RUNS=25 ROUNDS=8 CONVERSATION_MODE=normal PAIRING_STRATEGY=random CANDIDATE_POOL_SIZE=8 OUTPUT_ROOT=... RUN_ID=... NO_CACHE=1 LLM_SEED=42)"
	@echo "  summarize-chat-opinion-runs - Summarize chat_opinion run metadata (usage: make summarize-chat-opinion-runs INPUTS='--run-id review_a --run-id review_b' [OUTPUT_ROOT=data/output/examples/chat_opinion])"
	@echo "  compare-ensemble-sweeps - Compare two ensemble sweep directories (usage: make compare-ensemble-sweeps SWEEP_A=<dir> SWEEP_B=<dir> LABEL_A=hosted LABEL_B=hpc OUTPUT_ROOT=... RUN_ID=...)"
	@echo "  compare-example-chat - Compare two chat run output directories (usage: make compare-example-chat RUN_A=<dir> RUN_B=<dir> [OUTPUT_ROOT=...])"
	@echo "  compare-hpc-chat-runs - Compare two HPC chat run directories (usage: make compare-hpc-chat-runs RUN_A=<run|id|path> RUN_B=<run|id|path> [WORKING_DIR=/flash-calder/users/<user>/gabm])"
	@echo "  summarize-hpc-concurrency - Generate markdown rows from launcher summaries (usage: make summarize-hpc-concurrency INPUTS='--header --job-id 511621 --job-id 511679' [WORKING_DIR=...])"
	@echo "  report-hpc-chat-runs - Generate a full markdown comparison/concurrency report (usage: make report-hpc-chat-runs INPUTS='--run /path/to/run_1 --run /path/to/run_2 [--title ...]' [OUTPUT=path] [WORKING_DIR=...])"
	@echo "Use 'make <target>' to run a specific target. For targets that require additional variables (like release and sync-feature), include them as shown in the usage instructions."

# Run all tests (requires pytest)
test:
	@echo "Running tests with pytest..."
	PYTHONPATH=src:scripts pytest
	@echo "...done running tests with pytest."




# Build documentation (requires Sphinx, in docs/)
# This runs scripts/docs.py (which generates and post-processes .rst files), then builds with Sphinx, then cleans up auto-copied files.
docs: docs-make docs-clean

# Build documentation with Sphinx (in docs/)
docs-make:
	@echo "Building documentation with Sphinx..."
	python3 scripts/dev/docs.py
	PYTHONPATH=.. sphinx-build -b html docs docs/_build/html
	@echo "..done building documentation with Sphinx. Output in docs/_build/html/"

# Remove all auto-copied documentation files from docs/
docs-clean:
	@echo "Cleaning auto-copied documentation files from docs/..."
	python3 scripts/dev/docs-clean.py
	@echo "..done cleaning auto-copied documentation files from docs/"

# Build and deploy documentation to GitHub Pages
#
# NOTE: This target uses Make's dependency chaining to ensure docs are always built before deployment.
# This is preferred over calling $(MAKE) or make within a target.
gh-pages-deploy: docs
	@echo "Deploying documentation to GitHub Pages..."
	# Deploys documentation to GitHub Pages.
	# If you see a worktree error (gh-pages already used), the deployment script will attempt to clean up lingering worktrees automatically.
	# Manual cleanup: git worktree remove /tmp/gh-pages-xxxx...
	python3 scripts/dev/gh-pages-deploy.py
	@echo "...done deploying documentation to GitHub Pages."

# Deploy documentation to GitHub Pages on upstream remote (force push)
# This is a more aggressive deployment that force pushes to the gh-pages branch on the upstream remote. Use with caution, as it will overwrite the gh-pages branch on upstream.
gh-pages-deploy2: gh-pages-deploy
	@echo "Deploying documentation to GitHub Pages on upstream remote..."
	git push --force upstream gh-pages
	@echo "...done deploying documentation to GitHub Pages on upstream remote."

# Remove build/test artifacts
clean:
	@echo "Cleaning build and test artifacts..."
	python3 scripts/dev/clean.py
	@echo "...done cleaning build and test artifacts."

# Delete all LLM caches and model lists (for a clean slate)
clear-caches:
	@echo "Clearing all LLM caches and model lists..."
	python3 scripts/dev/clear-caches.py
	@echo "...done clearing all LLM caches and model lists."

# Clear caches and run live external LLM tests to check for API/model drift
llm-drift-check: clear-caches
	@echo "Running live LLM drift check tests..."
	PYTHONPATH=src:scripts pytest -m live_llm tests/src/gabm/io/llm -rs
	@echo "...done running live LLM drift check tests."
	
# Clean up merged local branches and prune deleted remotes (safe)
git-clean:
	@echo "Starting git cleanup of merged branches and pruned remotes..."
	@echo "Switching to main branch for safe cleanup..."
	@git checkout main
	@echo "Deleting local branches already merged to main..."
	@git branch --merged main | grep -vE '(^\*|main|gh-pages)' | xargs -r git branch -d
	@echo "Pruning deleted remote branches..."
	@git fetch --prune
	@echo "Git cleanup complete. Merged branches deleted and remotes pruned."


# Sync your main branch with upstream
sync:
	@echo "Syncing main branch with upstream and origin..."
	git fetch upstream
	git fetch origin
	git checkout main
	git merge upstream/main
	git pull origin main
	git push origin main
	@echo "...done syncing main branch with upstream and origin."

# Sync and rebase a feature/release branch with main
# Usage: make sync-feature BRANCH=release/0.2.0
sync-feature:
	@echo "Syncing and rebasing branch $(BRANCH) with main..."
	python3 scripts/dev/sync-feature.py --branch $(BRANCH)
	@echo "...done syncing and rebasing branch $(BRANCH) with main."


# Run onboarding/setup for all LLMs (API key check, model lists, cache init)
setup-llms:
	@echo "Running setup for LLMs (API key check, model lists, cache init)..."
	PYTHONPATH=src python3 scripts/dev/setup-llms.py
	@echo "...done running setup for LLMs."	


# Make a tag release on GitHub (usage: make release VERSION=x.y.z BRANCH=release/x.y.z)
release: sync-feature
	@echo "Making a tag release on GitHub for version $(VERSION) from branch $(BRANCH)..."
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION variable not set. Usage: make release VERSION=x.y.z BRANCH=release/x.y.z"; \
		exit 1; \
	fi
	python3 scripts/dev/release.py --version $(VERSION) --branch $(BRANCH)
	@echo "...done making a tag release on GitHub for version $(VERSION) from branch $(BRANCH)."

# Delete a release tag locally and on remotes (usage: make delete-release VERSION=x.y.z)
delete-release:
	@echo "Deleting release tag version $(VERSION) locally and on remotes..."
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION variable not set. Usage: make delete-release VERSION=x.y.z"; \
		exit 1; \
	fi
	git tag -d v$(VERSION) || true
	git push origin :refs/tags/v$(VERSION)
	git push upstream :refs/tags/v$(VERSION)
	@echo "...done deleting release tag version $(VERSION) locally and on remotes."


# Build a distribution package for PyPI (auto-sync README and requirements)
build: clean pypi-prep
	@echo "Building a distribution package for PyPI..."
	python3 -m build
	@echo "...done building a distribution package for PyPI. Output in dist/"

# Prepare PyPI packaging: sync requirements and generate README
pypi-prep:
	@echo "Syncing requirements and generating PyPI README..."
	python3 scripts/dev/sync_requirements_for_pypi.py
	python3 scripts/dev/generate_pypi_readme.py
	@echo "...done prepping for PyPI packaging."

# Build and test install the package in a fresh venv
build-test: build
	@echo "Building and test installing the package in a fresh venv..."
	python3 scripts/dev/build-test.py
	@echo "...done building and test installing the package in a fresh venv."

# Upload the built package to PyPI
pypi-release: build
	@echo "Uploading the built package to PyPI..."
	twine upload dist/*
	@echo "...done uploading the built package to PyPI."

# Upload the built package to TestPyPI
testpypi-release: build
	@echo "Uploading the built package to TestPyPI..."
	twine upload --repository testpypi dist/*
	@echo "...done uploading the built package to TestPyPI."

# Bump version everywhere (patch by default; use 'make bump-version part=minor' or 'part=major' for other bumps)
bump-version:
	bump2version --allow-dirty --list $${part:-patch}

# Run gabm using local source (development mode)
run-local:
	PYTHONPATH=src python3 -m gabm $(ARGS)

# Run gabm using installed package (production mode)
run-installed:
	python3 -m gabm $(ARGS)

# Run chat example with optional ONS file, output root, mode, and run-id overrides
# Usage: make run-example-chat SEED=42 YEAR=2026 CONVERSATION_MODE=normal PAIRING_STRATEGY=random CANDIDATE_POOL_SIZE=8 ONS_MALE=data/input/abm/names_england_wales_ons_male.csv ONS_FEMALE=data/input/abm/names_england_wales_ons_female.csv OUTPUT_ROOT=data/output/examples/chat RUN_ID=my_run_id NO_CACHE=1 LLM_SEED=42
run-example-chat:
	@RUN_ID_ARG=""; \
	if [ -n "$$RUN_ID" ]; then RUN_ID_ARG=" --run-id $$RUN_ID"; fi; \
	OUTPUT_ROOT_ARG=""; \
	if [ -n "$$OUTPUT_ROOT" ]; then OUTPUT_ROOT_ARG=" --output-root $$OUTPUT_ROOT"; fi; \
	LLM_SEED_ARG=""; \
	if [ -n "$$LLM_SEED" ]; then LLM_SEED_ARG=" --llm-seed $$LLM_SEED"; fi; \
	NO_CACHE_ARG=""; \
	if [ -n "$$NO_CACHE" ]; then NO_CACHE_ARG=" --no-cache"; fi; \
	PYTHONPATH=src python3 src/gabm/examples/chat/sim.py --llm-service openai --model gpt-4o-mini --seed $${SEED:-42} --year $${YEAR:-2026} --conversation-mode $${CONVERSATION_MODE:-normal} --pairing-strategy $${PAIRING_STRATEGY:-random} --candidate-pool-size $${CANDIDATE_POOL_SIZE:-8} --ons-male-file $${ONS_MALE:-data/input/abm/names_england_wales_ons_male.csv} --ons-female-file $${ONS_FEMALE:-data/input/abm/names_england_wales_ons_female.csv}$$OUTPUT_ROOT_ARG$$RUN_ID_ARG$$NO_CACHE_ARG$$LLM_SEED_ARG

# Run simple chat ensemble similarity sweep with optional overrides
# Usage: make run-example-chat-ensemble START_SEED=100 N_RUNS=25 YEAR=2026 CONVERSATION_MODE=normal PAIRING_STRATEGY=random CANDIDATE_POOL_SIZE=8 ONS_MALE=data/input/abm/names_england_wales_ons_male.csv ONS_FEMALE=data/input/abm/names_england_wales_ons_female.csv OUTPUT_ROOT=data/output/examples/chat/ensembles RUN_ID=my_sweep NO_CACHE=1 LLM_SEED=42
run-example-chat-ensemble:
	@RUN_ID_ARG=""; \
	if [ -n "$$RUN_ID" ]; then RUN_ID_ARG=" --run-id $$RUN_ID"; fi; \
	OUTPUT_ROOT_ARG=""; \
	if [ -n "$$OUTPUT_ROOT" ]; then OUTPUT_ROOT_ARG=" --output-root $$OUTPUT_ROOT"; fi; \
	LLM_SEED_ARG=""; \
	if [ -n "$$LLM_SEED" ]; then LLM_SEED_ARG=" --llm-seed $$LLM_SEED"; fi; \
	NO_CACHE_ARG=""; \
	if [ -n "$$NO_CACHE" ]; then NO_CACHE_ARG=" --no-cache"; fi; \
	PYTHONPATH=src python3 src/gabm/examples/chat/ensembles/similarity_sweep.py --llm-service openai --model gpt-4o-mini --start-seed $${START_SEED:-100} --n-runs $${N_RUNS:-25} --year $${YEAR:-2026} --conversation-mode $${CONVERSATION_MODE:-normal} --pairing-strategy $${PAIRING_STRATEGY:-random} --candidate-pool-size $${CANDIDATE_POOL_SIZE:-8} --ons-male-file $${ONS_MALE:-data/input/abm/names_england_wales_ons_male.csv} --ons-female-file $${ONS_FEMALE:-data/input/abm/names_england_wales_ons_female.csv}$$OUTPUT_ROOT_ARG$$RUN_ID_ARG$$NO_CACHE_ARG$$LLM_SEED_ARG

# Run chat+opinion example with optional overrides
# Usage: make run-example-chat-opinion SEED=42 YEAR=2026 ROUNDS=8 CONVERSATION_MODE=normal PAIRING_STRATEGY=random CANDIDATE_POOL_SIZE=8 QUESTION_BONUS=0.2 POSITIVE_TOKEN_BONUS=0.2 NEGATIVE_TOKEN_PENALTY=0.3 SHARED_INTEREST_CAP=0.3 ONS_MALE=data/input/abm/names_england_wales_ons_male.csv ONS_FEMALE=data/input/abm/names_england_wales_ons_female.csv OUTPUT_ROOT=data/output/examples/chat_opinion RUN_ID=my_run_id NO_CACHE=1 LLM_SEED=42
run-example-chat-opinion:
	@RUN_ID_ARG=""; \
	if [ -n "$$RUN_ID" ]; then RUN_ID_ARG=" --run-id $$RUN_ID"; fi; \
	OUTPUT_ROOT_ARG=""; \
	if [ -n "$$OUTPUT_ROOT" ]; then OUTPUT_ROOT_ARG=" --output-root $$OUTPUT_ROOT"; fi; \
	LLM_SEED_ARG=""; \
	if [ -n "$$LLM_SEED" ]; then LLM_SEED_ARG=" --llm-seed $$LLM_SEED"; fi; \
	NO_CACHE_ARG=""; \
	if [ -n "$$NO_CACHE" ]; then NO_CACHE_ARG=" --no-cache"; fi; \
	PYTHONPATH=src python3 src/gabm/examples/chat_opinion/sim.py --llm-service openai --model gpt-4o-mini --seed $${SEED:-42} --year $${YEAR:-2026} --rounds $${ROUNDS:-8} --conversation-mode $${CONVERSATION_MODE:-normal} --pairing-strategy $${PAIRING_STRATEGY:-random} --candidate-pool-size $${CANDIDATE_POOL_SIZE:-8} --question-bonus $${QUESTION_BONUS:-0.2} --positive-token-bonus $${POSITIVE_TOKEN_BONUS:-0.2} --negative-token-penalty $${NEGATIVE_TOKEN_PENALTY:-0.3} --shared-interest-cap $${SHARED_INTEREST_CAP:-0.3} --ons-male-file $${ONS_MALE:-data/input/abm/names_england_wales_ons_male.csv} --ons-female-file $${ONS_FEMALE:-data/input/abm/names_england_wales_ons_female.csv}$$OUTPUT_ROOT_ARG$$RUN_ID_ARG$$NO_CACHE_ARG$$LLM_SEED_ARG

# Run chat+opinion ensemble similarity sweep with optional overrides
# Usage: make run-example-chat-opinion-ensemble START_SEED=100 N_RUNS=25 YEAR=2026 ROUNDS=8 CONVERSATION_MODE=normal PAIRING_STRATEGY=random CANDIDATE_POOL_SIZE=8 QUESTION_BONUS=0.2 POSITIVE_TOKEN_BONUS=0.2 NEGATIVE_TOKEN_PENALTY=0.3 SHARED_INTEREST_CAP=0.3 ONS_MALE=data/input/abm/names_england_wales_ons_male.csv ONS_FEMALE=data/input/abm/names_england_wales_ons_female.csv OUTPUT_ROOT=data/output/examples/chat_opinion/ensembles RUN_ID=my_sweep NO_CACHE=1 LLM_SEED=42
run-example-chat-opinion-ensemble:
	@RUN_ID_ARG=""; \
	if [ -n "$$RUN_ID" ]; then RUN_ID_ARG=" --run-id $$RUN_ID"; fi; \
	OUTPUT_ROOT_ARG=""; \
	if [ -n "$$OUTPUT_ROOT" ]; then OUTPUT_ROOT_ARG=" --output-root $$OUTPUT_ROOT"; fi; \
	LLM_SEED_ARG=""; \
	if [ -n "$$LLM_SEED" ]; then LLM_SEED_ARG=" --llm-seed $$LLM_SEED"; fi; \
	NO_CACHE_ARG=""; \
	if [ -n "$$NO_CACHE" ]; then NO_CACHE_ARG=" --no-cache"; fi; \
	PYTHONPATH=src python3 src/gabm/examples/chat_opinion/ensembles/similarity_sweep.py --llm-service openai --model gpt-4o-mini --start-seed $${START_SEED:-100} --n-runs $${N_RUNS:-25} --year $${YEAR:-2026} --rounds $${ROUNDS:-8} --conversation-mode $${CONVERSATION_MODE:-normal} --pairing-strategy $${PAIRING_STRATEGY:-random} --candidate-pool-size $${CANDIDATE_POOL_SIZE:-8} --question-bonus $${QUESTION_BONUS:-0.2} --positive-token-bonus $${POSITIVE_TOKEN_BONUS:-0.2} --negative-token-penalty $${NEGATIVE_TOKEN_PENALTY:-0.3} --shared-interest-cap $${SHARED_INTEREST_CAP:-0.3} --ons-male-file $${ONS_MALE:-data/input/abm/names_england_wales_ons_male.csv} --ons-female-file $${ONS_FEMALE:-data/input/abm/names_england_wales_ons_female.csv}$$OUTPUT_ROOT_ARG$$RUN_ID_ARG$$NO_CACHE_ARG$$LLM_SEED_ARG

# Summarize chat_opinion run metadata ranges for calibration checks.
# Usage: make summarize-chat-opinion-runs INPUTS='--run-id review_a --run-id review_b' [OUTPUT_ROOT=data/output/examples/chat_opinion]
summarize-chat-opinion-runs:
	@python3 scripts/analysis/chat_opinion/summarize_runs.py --root $${OUTPUT_ROOT:-data/output/examples/chat_opinion} $${INPUTS}

# Compare two ensemble sweep directories and write aggregate difference report
# Usage: make compare-ensemble-sweeps SWEEP_A=data/output/examples/chat/ensembles/chat_small_01 SWEEP_B=data/output/examples/chat/ensembles/chat_hpc_01 LABEL_A=hosted LABEL_B=hpc OUTPUT_ROOT=data/output/examples/ensembles/compare RUN_ID=chat_compare_01
compare-ensemble-sweeps:
	@if [ -z "$(SWEEP_A)" ] || [ -z "$(SWEEP_B)" ]; then \
		echo "Error: SWEEP_A and SWEEP_B must be set."; \
		echo "Usage: make compare-ensemble-sweeps SWEEP_A=<dir> SWEEP_B=<dir> [LABEL_A=hosted] [LABEL_B=hpc] [OUTPUT_ROOT=...] [RUN_ID=...]"; \
		exit 1; \
	fi; \
	RUN_ID_ARG=""; \
	if [ -n "$$RUN_ID" ]; then RUN_ID_ARG=" --run-id $$RUN_ID"; fi; \
	OUTPUT_ROOT_ARG=""; \
	if [ -n "$$OUTPUT_ROOT" ]; then OUTPUT_ROOT_ARG=" --output-root $$OUTPUT_ROOT"; fi; \
	python3 scripts/analysis/chat/compare_sweeps.py --sweep-a "$(SWEEP_A)" --sweep-b "$(SWEEP_B)" --label-a "$${LABEL_A:-sweep_a}" --label-b "$${LABEL_B:-sweep_b}"$$OUTPUT_ROOT_ARG$$RUN_ID_ARG

# Compare two chat example runs by diffing their captured artifacts.
# Usage: make compare-example-chat RUN_A=seed42_run1 RUN_B=seed42_run2 [OUTPUT_ROOT=data/output/examples/chat]
compare-example-chat:
	@ROOT=$${OUTPUT_ROOT:-data/output/examples/chat}; \
	if [ -z "$(RUN_A)" ] || [ -z "$(RUN_B)" ]; then \
		echo "Error: RUN_A and RUN_B must be set."; \
		echo "Usage: make compare-example-chat RUN_A=<dir> RUN_B=<dir> [OUTPUT_ROOT=...]"; \
		exit 1; \
	fi; \
	A_DIR="$$ROOT/$(RUN_A)"; \
	B_DIR="$$ROOT/$(RUN_B)"; \
	if [ ! -d "$$A_DIR" ]; then echo "Error: missing directory $$A_DIR"; exit 1; fi; \
	if [ ! -d "$$B_DIR" ]; then echo "Error: missing directory $$B_DIR"; exit 1; fi; \
	STATUS=0; \
	for FILE in conversation_transcript.txt console_output.txt prompt_response_cache_delta.jsonl run_metadata.json; do \
		A_FILE="$$A_DIR/$$FILE"; \
		B_FILE="$$B_DIR/$$FILE"; \
		if [ ! -f "$$A_FILE" ] || [ ! -f "$$B_FILE" ]; then \
			echo "[MISSING] $$FILE (present? A=$$( [ -f "$$A_FILE" ] && echo yes || echo no ), B=$$( [ -f "$$B_FILE" ] && echo yes || echo no ))"; \
			STATUS=1; \
			continue; \
		fi; \
		if [ "$$FILE" = "run_metadata.json" ]; then \
			if python3 -c 'import json,sys; a=json.load(open(sys.argv[1], "r", encoding="utf-8")); b=json.load(open(sys.argv[2], "r", encoding="utf-8")); [d.pop("run_dir", None) for d in (a, b)]; [d.pop("created_at", None) for d in (a, b)]; raise SystemExit(0 if a == b else 1)' "$$A_FILE" "$$B_FILE"; then \
				echo "[IDENTICAL] $$FILE (ignoring volatile fields: run_dir, created_at)"; \
			else \
				echo "[DIFFERENT] $$FILE (after ignoring volatile fields: run_dir, created_at)"; \
				STATUS=1; \
			fi; \
			continue; \
		fi; \
		if diff -u "$$A_FILE" "$$B_FILE" > /dev/null; then \
			echo "[IDENTICAL] $$FILE"; \
		else \
			echo "[DIFFERENT] $$FILE"; \
			STATUS=1; \
		fi; \
	done; \
	if [ $$STATUS -eq 0 ]; then \
		echo "All compared artifacts are identical."; \
	else \
		echo "Differences detected. Re-run individual diff commands for details."; \
	fi; \
	exit $$STATUS

# Compare two HPC chat run directories using scripts/analysis/chat/compare_chat_runs.py
# Usage: make compare-hpc-chat-runs RUN_A=run_511621 RUN_B=/path/to/run_511679 [WORKING_DIR=/flash-calder/users/<user>/gabm]
compare-hpc-chat-runs:
	@if [ -z "$(RUN_A)" ] || [ -z "$(RUN_B)" ]; then \
		echo "Error: RUN_A and RUN_B must be set."; \
		echo "Usage: make compare-hpc-chat-runs RUN_A=<run|id|path> RUN_B=<run|id|path> [WORKING_DIR=...]"; \
		exit 1; \
	fi; \
	WORKING_DIR_ARG=""; \
	if [ -n "$(WORKING_DIR)" ]; then WORKING_DIR_ARG=" --working-dir $(WORKING_DIR)"; fi; \
	python3 scripts/analysis/chat/compare_chat_runs.py --run-a "$(RUN_A)" --run-b "$(RUN_B)"$$WORKING_DIR_ARG

# Generate markdown rows for concurrency/stress tables from launcher summaries.
# Usage: make summarize-hpc-concurrency INPUTS='--header --job-id 511621 --job-id 511679' [WORKING_DIR=/flash-calder/users/<user>/gabm]
summarize-hpc-concurrency:
	@if [ -z "$(INPUTS)" ]; then \
		echo "Error: INPUTS must be set."; \
		echo "Usage: make summarize-hpc-concurrency INPUTS='--header --job-id 511621 --job-id 511679' [WORKING_DIR=...]"; \
		exit 1; \
	fi; \
	WORKING_DIR_ARG=""; \
	if [ -n "$(WORKING_DIR)" ]; then WORKING_DIR_ARG=" --working-dir $(WORKING_DIR)"; fi; \
	python3 scripts/analysis/chat/generate_concurrency_rows.py $$WORKING_DIR_ARG $(INPUTS)

# Generate a markdown reproducibility report for multiple HPC chat runs.
# Usage: make report-hpc-chat-runs INPUTS='--run /path/to/run_1 --run /path/to/run_2 [--pair /path/to/run_1,/path/to/run_2] [--title ...]' [OUTPUT=report.md] [WORKING_DIR=/flash-calder/users/<user>/gabm]
report-hpc-chat-runs:
	@if [ -z "$(INPUTS)" ]; then \
		echo "Error: INPUTS must be set."; \
		echo "Usage: make report-hpc-chat-runs INPUTS='--run /path/to/run_1 --run /path/to/run_2 [--pair /path/to/run_1,/path/to/run_2] [--title ...]' [OUTPUT=report.md] [WORKING_DIR=...]"; \
		exit 1; \
	fi; \
	WORKING_DIR_ARG=""; \
	if [ -n "$(WORKING_DIR)" ]; then WORKING_DIR_ARG=" --working-dir $(WORKING_DIR)"; fi; \
	OUTPUT_ARG=""; \
	if [ -n "$(OUTPUT)" ]; then OUTPUT_ARG=" --output $(OUTPUT)"; fi; \
	python3 scripts/analysis/chat/generate_hpc_chat_report.py $$WORKING_DIR_ARG $(INPUTS)$$OUTPUT_ARG
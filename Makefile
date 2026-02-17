# Makefile for common development tasks
# Usage:
#   make help            - Show this help message
#   make test            - Run tests (pytest)
#   make docs            - Build documentation (Sphinx)
#   make docs-clean      - Clean auto-copied documentation files from docs/
#   make gh-pages-deploy - Build and deploy documentation to GitHub Pages
#   make clean           - Remove build/test artifacts
#   make clear-caches    - Delete all LLM caches and model lists (for a clean slate)
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
.PHONY: help test docs docs-clean gh-pages-deploy gh-pages-deploy2 clean git-clean setup-llms clear-caches sync sync-feature release delete-release build build-test pypi-release testpypi-release bump-version run-local run-installed

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
	@echo "Use 'make <target>' to run a specific target. For targets that require additional variables (like release and sync-feature), include them as shown in the usage instructions."

# Run all tests (requires pytest)
test:
	@echo "Running tests with pytest..."
	PYTHONPATH=src:scripts pytest
	@echo "...done running tests with pytest."


# Build documentation (requires Sphinx, in docs/)
#
# NOTE: This target uses Make's dependency chaining. Running `make docs` will first run `make docs-make` to build the documentation, and then `make docs-clean` to clean up any auto-copied files. This ensures that the documentation is always built before cleaning, without needing to call `$(MAKE)` or make within the target.
docs: docs-make docs-clean

# Build documentation with Sphinx (in docs/)
docs-make:
	@echo "Building documentation with Sphinx..."
	python3 scripts/docs.py
	PYTHONPATH=.. sphinx-build -b html docs docs/_build/html
	@echo "..done building documentation with Sphinx. Output in docs/_build/html/"

# Remove all auto-copied documentation files from docs/
docs-clean:
	@echo "Cleaning auto-copied documentation files from docs/..."
	python3 scripts/docs-clean.py
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
	python3 scripts/gh-pages-deploy.py
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
	python3 scripts/clean.py
	@echo "...done cleaning build and test artifacts."

# Delete all LLM caches and model lists (for a clean slate)
clear-caches:
	@echo "Clearing all LLM caches and model lists..."
	python3 scripts/clear-caches.py
	@echo "...done clearing all LLM caches and model lists."
	
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
	python3 scripts/sync-feature.py --branch $(BRANCH)
	@echo "...done syncing and rebasing branch $(BRANCH) with main."


# Run onboarding/setup for all LLMs (API key check, model lists, cache init)
setup-llms:
	@echo "Running setup for LLMs (API key check, model lists, cache init)..."
	PYTHONPATH=src python3 scripts/setup-llms.py
	@echo "...done running setup for LLMs."	


# Make a tag release on GitHub (usage: make release VERSION=x.y.z BRANCH=release/x.y.z)
release: sync-feature
	@echo "Making a tag release on GitHub for version $(VERSION) from branch $(BRANCH)..."
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION variable not set. Usage: make release VERSION=x.y.z BRANCH=release/x.y.z"; \
		exit 1; \
	fi
	python3 scripts/release.py --version $(VERSION) --branch $(BRANCH)
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
	python3 scripts/sync_requirements_for_pypi.py
	python3 scripts/generate_pypi_readme.py
	@echo "...done prepping for PyPI packaging."

# Build and test install the package in a fresh venv
build-test: build
	@echo "Building and test installing the package in a fresh venv..."
	python3 scripts/build-test.py
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
	PYTHONPATH=src python3 -m gabm

# Run gabm using installed package (production mode)
run-installed:
	python3 -m gabm
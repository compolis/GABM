# Makefile for common development tasks
# Usage:
#   make help           - Show this help message
#   make test           - Run tests (pytest)
#   make docs           - Build documentation (Sphinx)
#   make docs-clean     - Clean auto-copied documentation files from docs/
#   make gh-pages       - Build and deploy documentation to GitHub Pages
#   make clean          - Remove build/test artifacts
#   make clear-caches   - Delete all LLM caches and model lists (for a clean slate)
#   make git-clean      - Clean up merged local branches and prune deleted remotes
#   make sync           - Sync main branch with upstream
#   make sync-feature   - Sync and rebase a feature/release branch onto main (usage: make sync-feature BRANCH=release/0.2.0)
#   make setup-llms     - Run onboarding/setup for all LLMs (API key check, model lists, cache init)
#   make release        - Tag and push a release (usage: make release VERSION=x.y.z BRANCH=release/x.y.z)
#   make delete-release - Delete a release tag locally and on remotes (usage: make delete-release VERSION=x.y.z)
#
# Note: This Makefile assumes you have the necessary Python dependencies installed (e.g., pytest, Sphinx) and that you have set up git remotes correctly for syncing and releasing.
# Make sure to customize the scripts and commands as needed for your specific project structure and requirements.
#
# Targets are ordered by typical workflow: testing, documentation, cleaning, git maintenance, syncing, and releasing.
#
# The Makefile targets are explained in more detail in the DEV_GUIDE.md
#
# If you add a new target, please also add it to the help target and the DEV_GUIDE.md for consistency and ease of use for other developers.
#
# Caution: Some commands (like git-clean, release, and delete-release) can modify your git history or delete tags. Always review the scripts they call (in the scripts/ directory) to ensure they do what you expect before running these commands.

# Phony targets (not actual files)
.PHONY: help test docs docs-clean gh-pages clean git-clean setup-llms clear-caches sync sync-feature release delete-release

# Show available Makefile commands
help:
	@echo "Available targets:"
	@echo "  test         - Run tests (pytest)"
	@echo "  docs         - Build documentation (Sphinx)"
	@echo "  docs-clean   - Clean auto-copied documentation files from docs/"
	@echo "  gh-pages     - Build and deploy documentation to GitHub Pages"
	@echo "  clean        - Remove build/test artifacts"
	@echo "  clear-caches - Delete all LLM caches and model lists (for a clean slate)"
	@echo "  git-clean    - Clean up merged local branches and prune deleted remotes"
	@echo "  sync         - Sync main branch with upstream"
	@echo "  sync-feature - Sync and rebase a feature/release branch onto main (usage: make sync-feature BRANCH=release/0.2.0)"
	@echo "  setup-llms   - Run onboarding/setup for all LLMs (API key check, model lists, cache init)"
	@echo "  release      - Tag and push a release (usage: make release VERSION=x.y.z)"
	@echo "  delete-release - Delete a release tag locally and on remotes (usage: make delete-release VERSION=x.y.z)"
	

# Run all tests (requires pytest)
test:
	PYTHONPATH=. pytest

# Build documentation (requires Sphinx, in docs/)
docs:
	python3 scripts/docs.py
	PYTHONPATH=.. sphinx-build -b html docs docs/_build/html
	$(MAKE) docs-clean

# Remove all auto-copied documentation files from docs/
docs-clean:
	python3 scripts/docs-clean.py
	@echo "Cleaned auto-copied documentation files from docs/"

# Build and deploy documentation to GitHub Pages
gh-pages:
	python3 scripts/gh-pages.py


# Remove build/test artifacts
clean:
	python3 scripts/clean.py

# Delete all LLM caches and model lists (for a clean slate)
clear-caches:
	python3 scripts/clear-caches.py
	@echo "All LLM caches and model lists cleared."
	
# Clean up merged local branches and prune deleted remotes (safe)
git-clean:
	@echo "Switching to main branch for safe cleanup..."
	@git checkout main
	@echo "Deleting local branches already merged to main..."
	@git branch --merged main | grep -vE '(^\*|main|gh-pages)' | xargs -r git branch -d
	@echo "Pruning deleted remote branches..."
	@git fetch --prune
	@echo "Done. Review remote branches on GitHub for further cleanup if needed."


# Sync your main branch with upstream
sync:
	git fetch upstream
	git checkout main
	git merge upstream/main
	git push origin main

# Sync and rebase a feature/release branch onto main
# Usage: make sync-feature BRANCH=release/0.2.0
sync-feature:
	python3 scripts/sync-feature.py --branch $(BRANCH)


# Run onboarding/setup for all LLMs (API key check, model lists, cache init)
setup-llms:
	python3 scripts/setup-llms.py


# Tag and push a release (usage: make release VERSION=x.y.z BRANCH=release/x.y.z)
release:
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION variable not set. Usage: make release VERSION=x.y.z BRANCH=release/x.y.z"; \
		exit 1; \
	fi
	@if [ -z "$(BRANCH)" ]; then \
		echo "Error: BRANCH variable not set. Usage: make release VERSION=x.y.z BRANCH=release/x.y.z"; \
		exit 1; \
	fi
	python3 scripts/release.py --version $(VERSION) --branch $(BRANCH)

# Delete a release tag locally and on remotes (usage: make delete-release VERSION=x.y.z)
delete-release:
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION variable not set. Usage: make delete-release VERSION=x.y.z"; \
		exit 1; \
	fi
	git tag -d v$(VERSION) || true
	git push origin :refs/tags/v$(VERSION)
	git push upstream :refs/tags/v$(VERSION)
	@echo "Deleted tag v$(VERSION) locally, on origin, and on upstream."

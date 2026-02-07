# Makefile for common development tasks

# Phony targets (not actual files)
.PHONY: help sync test docs clean git-clean setup-llms clear-caches release sync-feature

# Show available Makefile commands
help:
	@echo "Available targets:"
	@echo "  sync         - Sync main branch with upstream"
	@echo "  test         - Run tests (pytest)"
	@echo "  docs         - Build documentation (Sphinx)"
	@echo "  clean        - Remove build/test artifacts"
	@echo "  git-clean    - Clean up merged local branches and prune deleted remotes"
	@echo "  setup-llms   - Run onboarding/setup for all LLMs (API key check, model lists, cache init)"
	@echo "  clear-caches - Delete all LLM caches and model lists (for a clean slate)"
	@echo "  release      - Tag and push a release (usage: make release VERSION=x.y.z)"

# Tag and push a release (usage: make release VERSION=x.y.z)
release:
	@if [ -z "$(VERSION)" ]; then \
	  echo "Error: VERSION variable not set. Usage: make release VERSION=x.y.z"; \
	  exit 1; \
	fi
	git tag -a v$(VERSION) -m "Release v$(VERSION)"
	git push origin v$(VERSION)
	@echo "Release v$(VERSION) tagged and pushed."

# Sync your main branch with upstream
sync:
	git fetch upstream
	git checkout main
	git merge upstream/main
	git push origin main

# Run all tests (requires pytest)
test:
	PYTHONPATH=. pytest

# Build documentation (requires Sphinx, in docs/)
docs:
	python3 scripts/update_docs_assets.py
	PYTHONPATH=.. sphinx-build -b html docs docs/_build/html
	$(MAKE) docs-clean

# Build and deploy documentation to GitHub Pages
gh-pages:
	python3 scripts/gh_pages_deploy.py

# Remove all auto-copied documentation files from docs/
docs-clean:
	python3 scripts/clean_docs_assets.py
	@echo "Cleaned auto-copied documentation files from docs/"

# Remove build/test artifacts
clean:
	python3 scripts/clean_project.py

# Clean up merged local branches and prune deleted remotes (safe)
git-clean:
	@echo "Switching to main branch for safe cleanup..."
	@git checkout main
	@echo "Deleting local branches already merged to main..."
	@git branch --merged main | grep -vE '(^\*|main|gh-pages)' | xargs -r git branch -d
	@echo "Pruning deleted remote branches..."
	@git fetch --prune
	@echo "Done. Review remote branches on GitHub for further cleanup if needed."

# Run onboarding/setup for all LLMs (API key check, model lists, cache init)
setup-llms:
	PYTHONPATH=. python3 src/setup_llms.py

# Delete all LLM caches and model lists (for a clean slate)
clear-caches:
	python3 scripts/clear_caches.py
	@echo "All LLM caches and model lists cleared."

# End of Makefile

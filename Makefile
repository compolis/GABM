# Makefile for common development tasks

.PHONY: help sync test docs

help:
	@echo "Available targets:"
	@echo "  sync   - Sync main branch with upstream"
	@echo "  test   - Run tests (pytest)"
	@echo "  docs   - Build documentation (Sphinx)"

sync:
	git fetch upstream
	git checkout main
	git merge upstream/main
	git push origin main

test:
	PYTHONPATH=. pytest

docs:
	PYTHONPATH=.. sphinx-build -b html docs docs/_build/html

gh-pages:
	cd docs && sphinx-build -b html . _build/html
	git worktree add /tmp/gh-pages gh-pages || git checkout --orphan gh-pages
	rm -rf /tmp/gh-pages/*
	cp -r docs/_build/html/* /tmp/gh-pages/
	cd /tmp/gh-pages && git add . && git commit -m "Update docs" && git push origin gh-pages
	git worktree remove /tmp/gh-pages
	

.PHONY: clean git-clean

# Remove build/test artifacts
clean:
	rm -rf docs/_build
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +

# Clean up merged local branches and prune deleted remotes (safe)
git-clean:
	@echo "Deleting local branches already merged to main..."
	@git branch --merged main | grep -vE '(^\*|main|gh-pages)' | xargs -r git branch -d
	@echo "Pruning deleted remote branches..."
	@git fetch --prune
	@echo "Done. Review remote branches on GitHub for further cleanup if needed."

# End of Makefile

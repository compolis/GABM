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
	cd docs && sphinx-build -b html . _build/html

gh-pages:
	cd docs && sphinx-build -b html . _build/html
	git worktree add /tmp/gh-pages gh-pages || git checkout --orphan gh-pages
	rm -rf /tmp/gh-pages/*
	cp -r docs/_build/html/* /tmp/gh-pages/
	cd /tmp/gh-pages && git add . && git commit -m "Update docs" && git push origin gh-pages
	git worktree remove /tmp/gh-pages
	
# End of Makefile

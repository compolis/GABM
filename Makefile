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
	cd docs && make html

# Developer Guide

---
title: Developer Guide
---

## Overview
This guide provides best practices for contributing to GABM, collaborating with other developers, and understanding the project structure, Makefile targets, and documentation workflow.

## Contributing Workflow
- Fork the repository and create feature branches for new work.
- Commit changes with clear messages.
- Push to your fork and open a pull request (PR) against the main repository.
- Review and respond to feedback promptly.
- Keep your branch up to date with upstream/main.

## Collaboration & Communication
- Use GitHub Issues and PRs for discussion and tracking.
- Communicate blockers or questions early.
- Reference related issues/PRs in your commits and comments.
- Respect code review feedback and project coding standards.

## Project Structure
- `src/`: Main source code
- `data/`: For data including log files
- `docs/`: Documentation and assets
- `scripts/`: Utility scripts
- `tests/`: Test suite
- `Makefile`: Automation targets

## Makefile Targets
- `make test`: Run all tests
- `make docs`: Build documentation
- `make setup-llms`: Setup LLM configuration
- `make clean`: Remove build artifacts
- `make gh-pages`: Deploy docs to GitHub Pages

## Developing Documentation
- Edit Markdown files in `docs/` and project root
- Use Sphinx and MyST for documentation builds
- Add new guides or API docs as needed
- Run `make docs` to preview changes

## Python Version
- Python 3.12+ required for development
- Ensure `python3` points to the correct version

## Additional Resources
- See `SETUP_GUIDE_DEV.md` for environment setup
- See `README.md` for project overview

---
For further questions, [open an issue](https://github.com/compolis/GABM/issues/new/choose) or contact maintainers via GitHub.

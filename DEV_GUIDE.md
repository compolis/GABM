# Developer Guide

## Overview
This guide provides best practices for contributing to GABM, collaborating with other developers, and understanding the project structure, Makefile targets, and documentation workflow. Documentation was updated in release 0.1.1 for clarity and completeness.

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

| Target         | Usage/Description                                                                 |
|--------------- |----------------------------------------------------------------------------------|
| `make help`    | Show available Makefile commands                                                  |
| `make sync`    | Sync main branch with upstream                                                    |
| `make test`    | Run all tests (pytest)                                                            |
| `make docs`    | Build documentation (Sphinx) and clean auto-copied docs assets                    |
| `make docs-clean` | Remove auto-copied documentation files from docs/                              |
| `make clean`   | Remove build/test artifacts and Python caches                                     |
| `make git-clean` | Clean up merged local branches and prune deleted remotes                        |
| `make setup-llms` | Run onboarding/setup for all LLMs (API key check, model lists, cache init)     |
| `make clear-caches` | Delete all LLM caches and model lists (for a clean slate)                    |
| `make release VERSION=x.y.z BRANCH=release/x.y.z` | Tag and push a release (platform-agnostic)     |
| `make sync-feature BRANCH=release/0.2.0` | Sync and rebase a feature/release branch onto main     |
| `make gh-pages` | Build and deploy documentation to GitHub Pages                                   |
| `make delete-release VERSION=x.y.z` | Delete a release tag locally and on remotes (origin, upstream) |


**Notes:**
- All Python scripts used by Makefile targets are in the `scripts/` directory and are named consistently with their Makefile targets (e.g., `make docs-clean` runs `scripts/docs-clean.py`).
- The `delete-release` target is platform-agnostic and automates deleting a release tag locally and on both remotes (origin, upstream).
- This convention improves clarity and discoverability for contributors.
- Targets are platform-agnostic and reproducible.

Refer to the Makefile for full details and usage examples.

## Developing Documentation
- Edit Markdown files in `docs/` and project root
- Use Sphinx and MyST via `make docs` for documentation builds and update the script it uses as approriate
- Add new guides or API docs as needed
- Run `make docs` to preview changes

## Python Version
- Python 3.12+ required for development
- Ensure `python3` points to the correct version

## Additional Resources
- See [SETUP_GUIDE_DEV.md](SETUP_GUIDE_DEV.md) for environment setup
- See [README.md](README.md) for project overview

---
For further questions, [open an issue](https://github.com/compolis/GABM/issues/new/choose) or contact maintainers via GitHub.

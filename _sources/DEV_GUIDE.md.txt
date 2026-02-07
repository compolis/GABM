
# Developer Guide

## Overview
This guide provides best practices for contributing to GABM, collaborating with other developers, and understanding the project structure, Makefile targets, and documentation workflow. Documentation was updated in release 0.1.1 for clarity and completeness.

## Table of Contents

- [Overview](#overview)
- [Contributing Workflow](#contributing-workflow)
- [Collaboration & Communication](#collaboration--communication)
- [Project Structure](#project-structure)
- [Python Package Entry Point: __main__.py](#python-package-entry-point-__main__py)
- [Makefile Targets](#makefile-targets)
- [Developing Documentation](#developing-documentation)
- [Python Version](#python-version)
- [Additional Resources](#additional-resources)

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
- `data/`: For data including log files
- `docs/`: Documentation and assets
- `scripts/`: Utility scripts
- `src/gabm`: Python source code package
- `tests/`: Test suite
- `Makefile`: Automation targets

## Python Package Entry Point: __main__.py
The main entry point for the GABM package is `src/gabm/__main__.py`. This follows Python packaging best practices and allows the application to be run using:

	python3 -m gabm

This approach is preferred over directly running a script (like `run.py`) because:
- It enables Python to treat `gabm` as a package, ensuring imports work correctly.
- It is the standard way to provide a command-line entry point for Python packages.
- It makes the project ready for distribution and installation via pip or PyPI.

The `__main__.py` file is executed when you run `python3 -m gabm` from the project root (with `src` on the Python path). If you need to add or change the main application logic, edit `src/gabm/__main__.py`.

For more details, see the [Python Packaging documentation](https://docs.python.org/3/library/__main__.html).


## Makefile Targets

| Target         | Usage/Description                                                                 |
|--------------- |----------------------------------------------------------------------------------|
| `make help`    | Show available Makefile commands                                                  |
| `make test`    | Run all tests (pytest)                                                            |
| `make docs`    | Build documentation (Sphinx) and clean auto-copied docs assets                    |
| `make docs-clean` | Remove auto-copied documentation files from docs/                              |
| `make gh-pages` | Build and deploy documentation to GitHub Pages                                   |
| `make clean`   | Remove build/test artifacts and Python caches                                     |
| `make clear-caches` | Delete all LLM caches and model lists (for a clean slate)                    |
| `make git-clean` | Clean up merged local branches and prune deleted remotes                        |
| `make sync`    | Sync main branch with upstream                                                    |
| `make sync-feature BRANCH=release/0.2.0` | Sync and rebase a feature/release branch onto main     |
| `make setup-llms` | Run onboarding/setup for all LLMs (API key check, model lists, cache init)     |
| `make release VERSION=x.y.z BRANCH=release/x.y.z` | Tag and push a release (platform-agnostic)     |
| `make delete-release VERSION=x.y.z` | Delete a release tag locally and on remotes (origin, upstream) |
| `make build`    | Build a distribution package for PyPI (python -m build)                            |
| `make build-test` | Build and test install the package in a fresh venv                               |
| `make pypi-release` | Upload the built package to PyPI (twine upload dist/*)                         |
| `make testpypi-release` | Upload the built package to TestPyPI (twine upload --repository testpypi dist/*) |


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




## Packaging Files

The following files and directories are essential for building, testing, and distributing the GABM package:

- **pyproject.toml**: Declares build system requirements and project metadata. Required for modern Python packaging (PEP 517/518).
- **setup.cfg**: Contains static package metadata and configuration for setuptools, such as:
	- Package name, version, author, and description
	- Python version requirements
	- Entry points (e.g., console_scripts)
	- Classifiers and other options
	This file is preferred over setup.py for static, declarative configuration.
- **MANIFEST.in**: Tells setuptools which additional files (beyond Python modules) to include in the source distribution (sdist). For example:
	- Documentation files (README.md, LICENSE, etc.)
	- Data files needed at runtime
	- Example: `include README.md LICENSE data/*.csv`
	This ensures users who install from source get all necessary files.
- **requirements.txt**: Lists pinned dependencies for end users (used by pip install -r requirements.txt).
- **requirements-dev.txt**: Lists development dependencies (testing, linting, docs) with version ranges for contributors.
- **dist/**: Output directory for built distributions (.tar.gz and .whl files) after running the build process.
- **src/gabm.egg-info/**: Metadata directory created by setuptools during build. Contains information about the package (version, dependencies, etc.). Safe to delete; will be recreated as needed.
- **venv-build-test/**: Temporary virtual environment created by `make build-test` for testing the built package in isolation. Can be safely deleted after testing.


## PyPI Release Process

To release a new version of GABM to PyPI, follow these steps:

1. **Update Version**: Bump the version in setup.cfg and/or pyproject.toml as appropriate.
2. **Build the Package**:
	```sh
	make build
	```
	This creates .tar.gz and .whl files in the dist/ directory.
3. **Test the Build**:
	```sh
	make build-test
	```
	This installs the built package in a clean environment and runs the test suite.
4. **Upload to TestPyPI (optional but recommended):**
	```sh
	make testpypi-release
	```
	This uploads the package to TestPyPI. Test installation from TestPyPI in a clean environment:
	```sh
	pip install --index-url https://test.pypi.org/simple/ gabm
	```
5. **Upload to PyPI:**
	```sh
	make pypi-release
	```
	This uploads the package to the official PyPI repository.
6. **Verify Release:**
	- Check the PyPI page and test installation with pip install gabm

For more details, see the [Python Packaging User Guide](https://packaging.python.org/).

## Additional Resources
- See [SETUP_GUIDE_DEV.md](SETUP_GUIDE_DEV.md) for environment setup
- See [README.md](README.md) for project overview

---
For further questions, [open an issue](https://github.com/compolis/GABM/issues/new/choose) or contact maintainers via GitHub.

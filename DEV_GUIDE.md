# Developer Guide


## Table of Contents
- [Overview](#overview)
- [Contributing and Communicating](#contributing-and-communicating)
- [Project Directories](#project-directories)
- [Python Package Entry Point](#python-package-entry-point)
- [Makefile Targets](#makefile-targets)
- [Developing Documentation](#developing-documentation)
- [Packaging and Deployment](#packaging-and-deployment)
- [Branch Protection](#branch-protection)
- [Maintainer Guide](#maintainer-guide)
- [Branch and Documentation Deployment](#branch-and-documentation-deployment)
- [GitHub Copilot](#github-copilot)
- [Managing Logs and Caches](#managing-logs-and-caches)
- [Files and Directories Excluded from Version Control](#files-and-directories-excluded-from-version-control)
- [LLM Service Architecture](#llm-service-architecture)
- [Additional Resources](#additional-resources)


## Overview

The GABM developer guide provides guidance for developers some of which are also maintainers.

Please follow the [Developer Quick Start Guide](DEV_QUICKSTART.md) to get set up to contribute as a developer.

In the rest of the document "you" means you as a GABM developer.


## Contributing and Communicating

Please follow the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

For the time being, please communicate by commenting on or raising new [GABM Repository Issues](https://github.com/compolis/GABM/issues).

You should have forked the [GABM Repository](https://github.com/compolis/GABM) to your own GitHub account.

The general workflow for contributing is to:
- Create a check out new local branch:

```bash
git branch my_feature
git checkout my_feature
```

- Make changes:
  - For each Python file edited, please adjust the Metadata at the top of the file by:
    - Adding your details to the `__author__` list
    - Incrementing the `__version__`
  - Update the [Change Log](CHANGE_LOG.md) with a summary of your changes.
- Commit changes with a clear message. For example:

```bash
git add .
git commit -m "Clear message that explains changes." 
```

- Ensure tests pass and documentation builds before submitting a PR:

```bash
make test
make docs
```

- Push to your Fork, For example:

```bash
git push origin my_feature
```

- Open a PR on GitHub to merge your `my_feature` branch into the the `main` branch of the upstream GABM Repository.
  - Please refer to any related issues in the PR comments.
- The PR will be reviewed and once the review is complete, changes will be merged.


## Project Directories

The root project directory contains documentation and files needed for building and deploying. The sub-diretories include: 
- `data/`: For data including log files
- `dist/`: Output directory for built distributions.
- `docs/`: Documentation
- `scripts/`: Utility scripts
- `src/`: Python source code
- `tests/`: Test suite for src
- `venv-build-test/`: For temporary virtual environments created for testing.


## Python Package Entry Point

The main entry point for the GABM package is `src/gabm/__main__.py`. This allows the application to be run using:

	python3 -m gabm

This approach is preferred over directly running a script (like `run.py`) as:
  - It enables Python to treat `gabm` as a package, ensuring imports work correctly.
  - It is the standard way to provide a command-line entry point for Python packages.
  - It makes the project ready for distribution and installation.

The `__main__.py` file is executed when you run `python3 -m gabm` from the project root (with `src` on the Python path). If you need to add or change the main application logic, edit `src/gabm/__main__.py`.

Please see the [Python Packaging documentation](https://docs.python.org/3/library/__main__.html) for information about Python packaging.


## Makefile Targets

The root directory contains a [Makefile](https://www.gnu.org/software/make/manual/make.html#Introduction). This is set up to automate tasks using [GNU Make](https://www.gnu.org/software/make). This section explains the rules or targets in the Makefile. Please ensure any changes to the Makefile are platform agnostic.


### Target Chaining, DRY, and Consistency

For maintainability, all Makefile targets that depend on other build steps should use Make's built-in dependency chaining (e.g., `gh-pages-deploy: docs`) rather than manually invoking `$(MAKE)` or shelling out to `make` within a target. This ensures:
- Each target is only responsible for its own logic.
- Consistency: all targets use the same build steps, and changes to one target (like `docs`) automatically propagate to dependents (like `gh-pages-deploy`). The following is a presentation of the Makefile rules/targets:

| Target         | Usage/Description                                                                 |
|--------------- |----------------------------------------------------------------------------------|
| `make help`    | Show available Makefile commands                                                  |
| `make test`    | Run all tests (pytest)                                                            |
| `make docs`    | Build documentation (Sphinx) and clean auto-copied docs assets                    |
| `make docs-build` | Build documentation (Sphinx)                                                      |
| `make docs-clean` | Remove auto-copied documentation files from docs/                              |
| `make gh-pages-deploy` | Build and deploy documentation to GitHub Pages (runs scripts/gh-pages-deploy.py) |
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
| `make bump-version` | Bump the project version everywhere (patch by default; use `make bump-version part=minor` or `part=major` for other bumps). Uses bump2version and updates all relevant files. |
| `make run-local` | Run gabm using local source (PYTHONPATH=src) |
| `make run-installed` | Run gabm using installed package |


All Python scripts used by Makefile targets are in the `scripts/` directory and are named consistently with their Makefile targets (e.g., `make docs-clean` runs `scripts/docs-clean.py`).

The `delete-release` target automates deleting a release tag locally and on both remotes (origin, upstream).

Please refer to the Makefile for full details.


## Developing Documentation

Markdown files in the root directory, each serving a specific purpose:
  - [README.md](README.md): A general [README](https://en.wikipedia.org/wiki/README) that links to much of the documentation outlined below including the developer and user guides. It is included in the Sphinx documentation and forms the basis for the main Sphinx documentation page.
  - [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): Provides details on expected behavior of developers and reporting procedures.
  - [USER_GUIDE.md](USER_GUIDE.md): Provides step-by-step instructions for users to get set, and should provide guidance for using GABM.
  - [DEV_QUICKSTART.md](DEV_QUICKSTART.md) Provides step-by-step instructions for developers to get set up for contributing to GABM development.
  - [DEV_GUIDE.md](DEV_GUIDE.md): Explains how to contribute to GABM as a developer. It provides details about project structure, and workflow guidance.
  - [API_KEYS.md](API_KEYS.md): Explains how to create a file containing API keys for communicating with LLMs.
  - [ROADMAP.md](ROADMAP.md): Document to outline planned features and future development goals.
  - [CHANGE_LOG.md](CHANGE_LOG.md): Document to describe changes and updates.
  - [DEVELOPMENT_HISTORY.md]: Document about development, milestones, and reflections.

- If you add a new Markdown file in the root directory, please update entries to `doc_assets.py` DOC_FILES and `docs/index.md` Project Documents to include them in Sphinx documentation.
- Add API docs via `docs/index.md`


### Sphinx Documentation

To build run:

```bash
make docs
```

- This effectively runs `scripts/docs.py` to copy key documentation files from the project root to the `docs/` directory, pre-processes them for building the Sphinx documentation, then delete those copied files once the build completes.

**Note on Sphinx/MyST Documentation Warnings:**

When building the documentation with [Sphinx](https://www.sphinx-doc.org/) and [MyST](https://mystmd.org/), you may see warnings like:

  Document headings start at H2, not H1 [myst.header]

These warnings occur even though all Markdown files start with H2 (`##`). This is a known quirk with MyST/Sphinx and does not affect the rendered documentation. You can safely ignore these warnings unless the formatting in the HTML output is incorrect.


Preview the Sphinx documentation by opening `docs/_build/html/index.html` in a [Web browser](https://en.wikipedia.org/wiki/Web_browser).

To deploying the Sphinx Documentation run:

```bash
make gh-pages-deploy
```

This should deploy/update the `gh-pages` branch on your origin Fork. If your Fork uses the `gh-pages` branch for [GitHub Pages](https://docs.github.com/en/pages), then the documentation should update there.

If it all looks good. Please submit a PR to incorporate documentation changes into main. A maintainer will subsequently update the upstream repository gh-pages branch.


## Packaging and Deployment

The following files and directories are essential for building, testing, and distributing the GABM package:
- **pyproject.toml**: Declares build system requirements and project metadata. Required for modern Python packaging (PEP 517/518).
- **setup.cfg**: Contains static package metadata and configuration for setuptools, such as:
	- Package name, version, author, and description
	- Python version requirements
	- Entry points (e.g., console_scripts)
	- Classifiers and other options
	This file is preferred over setup.py for static, declarative configuration.
- **MANIFEST.in**: Informs setuptools which additional files (beyond Python modules) to include in the source distribution (sdist). This should be updated so users who install from source get all necessary files.
- **requirements.txt**: Lists pinned dependencies for end users (used by pip install -r requirements.txt).
- **requirements-dev.txt**: Lists development dependencies (testing, linting, docs) with version ranges for contributors.
- **dist/**: Output directory for built distributions (.tar.gz and .whl files) after running the build process.
- **src/gabm.egg-info/**: Metadata directory created by setuptools during build. Contains information about the package (version, dependencies, etc.). Safe to delete; will be recreated as needed.
- **venv-build-test/**: Temporary virtual environment created by `make build-test` for testing the built package in isolation. This can be safely deleted after testing.


## Branch Protection

[GitHub Actions](https://github.com/features/actions) workflows are used to help manage Pull Requests (PRs):
- `.github/workflows/test.yml` automatically runs `make test` on PRs to the main branch.
- `.github/workflows/gh-pages-deploy.yml` builds documentation for the gh-pages branch and is for automated docs deployment.

PRs to the [GAB Repository main branch](https://github.com/compolis/GABM/tree/main) must pass the test workflow before merging.

The gh-pages branch is protected from deletion.


## Maintainer Guide

This section is aimed at developers that are maintainers. Developers that are not maintainers are requested to refrain from publishing releases to PyPI so maintainers can ensure project integrity and security.


### PyPI Release Process

To release a new version of GABM to [PyPI](https://pypi.org/), follow these steps:

1. **Update Version**: Run `make bump-version` to update the version everywhere (including setup.cfg, pyproject.toml, src/gabm/__init__.py, requirements-dev.txt, and all occurrences in [User Guide](USER_GUIDE.md)). Use `make bump-version part=minor` or `part=major` for non-patch bumps. Commit and push the changes before continuing.
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
	You will need to have an account on https://test.pypi.org and have created an API key for this to work.
5. **Upload to PyPI:**
	```sh
	make pypi-release
	```
	This uploads the package to the official PyPI repository.
	You will need to have an account on https://pypi.org and have created an API key for this to work.
6. **Verify Release:**
	- Check the PyPI page and test installation as a user ensuring the instructions in the [User Guide](USER_GUIDE.md) work.

To help recover from accidental corruption, template copies of the main packaging metadata files are provided:

- `setup.cfg.template`
- `pyproject.toml.template`

If you need to reset `setup.cfg` or `pyproject.toml`, copy these templates over the originals.

**Note:** These templates should be updated if you make structural changes to the originals. Bear in mind that the originals are processed to insert the dependency requirements from requirements.txt.


For more details, see the [Python Packaging User Guide](https://packaging.python.org/).


### Branch and Documentation Deployment

Sphinx documentation is built and deployed using `make gh-pages-deploy`. If the upstream `gh-pages` branch is out of sync or needs to be replaced, use `git push --force upstream gh-pages` to overwrite it with the correct local version. This should be done with care, as it replaces the branch history. 

When deploying documentation with `make gh-pages-deploy`, you may encounter an error like:

```
fatal: 'gh-pages' is already used by worktree at '/tmp/gh-pages-xxxx...'
```

This occurs if a previous deployment left a lingering worktree directory for the `gh-pages` branch. The deployment script should automatically check for and removes any existing worktree before adding a new one. If you encounter this error, manually remove the worktree:

```
git worktree remove /tmp/gh-pages-xxxx...
```

For more details, see the comments in the Makefile and the deployment script.


## GitHub Copilot

Using [GitHub Copilot](https://github.com/features/copilot)) for [vibe coding](https://en.wikipedia.org/wiki/Vibe_coding), can help with understanding workflows and developing documentation, code and tests.

GitHub Copilot uses limited context and the chat context does not currently persist between sessions. As a result, it is good to develop/update documentation along with changes. GitHub Copilot can be asked to read the [README](README.md) and [Developer Guide](DEV_GUIDE.md) at the start of a session so as to be more context aware and provide better support.


## Managing Logs and Caches

Logs and caches (including prompt/response caches for LLM services) are generated during development and use. These files can become large. Typically they are not committed to the repository. Tidy-up scripts and Makefile targets for managing logs and caches are planned for version 0.2.0.

Project Python scripts use Python logging and write logs to:

	data/logs/docs/         # Documentation logs
	data/logs/llm/          # LLM module logs (OpenAI, DeepSeek, GenAI, etc.)

Each Python script and LLM module has its own log file to help:
- Debug issues with documentation builds, asset copying, or LLM API calls
- Review script actions and errors

Logging levels can be adjusted as needed.

If you encounter problems, please check relevant log files for details.


## Files and Directories Excluded from Version Control

Certain files and directories are intentionally excluded from the repository via `.gitignore` to keep the project clean and secure:

- `data/logs/` — All log files generated by scripts and modules (can be large and environment-specific)
- `data/io/llm/*/prompt_response_cache.pkl` — LLM response cache files (can be large and are not needed for collaboration)
- `data/api_key.csv` — API keys (never commit secrets)


## LLM Service Architecture

GABM uses a class architecture for integrating LLM services. All LLM modules (OpenAI, GenAI, DeepSeek, PublicAI, etc.) subclass a shared LLMService base class, which provides:
- Generic caching and logging for prompt/response pairs
- Consistent file naming and path management
- Centralized error handling and environment variable setup
- Model list writing utilities

To add a new LLM service:
- Create a new class (e.g., MyLLMService) that subclasses LLMService.
- Implement the send and list_available_models methods.
- Use the base class helpers:
  - _pre_send_check_and_cache for API key, cache, and env setup
  - _call_and_cache_response for error handling and caching
  - _write_model_list for model list output

Example:
```Python
class MyLLMService(LLMService):
    SERVICE_NAME = "myllm"
    def send(self, api_key, message, model="default-model"):
        cached = self._pre_send_check_and_cache(api_key, message, model)
        if cached is not None:
            return cached
        cache_key = (message, model)
        def api_call():
            # Actual LLM API call here
            return myllm_client.send(model=model, prompt=message)
        return self._call_and_cache_response(api_call, cache_key, message, model, api_key)
```


## Additional Resources

- [Apertus LLM Setup and Usage](Apertus.md) — for details on obtaining and using local Apertus LLM models
# Developer Guide


## Table of Contents
- [Overview](#overview)
- [Resume This Workstream](#resume-this-workstream)
- [Contributing and Communicating](#contributing-and-communicating)
- [Project Directories](#project-directories)
- [Testing](#testing)
- [Network Utilities](#network-utilities)
- [Two-stage Survey Execution](#two-stage-survey-execution)
- [Example Simulations and Reproducibility](#example-simulations-and-reproducibility)
- [Python Package Entry Point](#python-package-entry-point)
- [Makefile Targets](#makefile-targets)
- [Developing Documentation](#developing-documentation)
- [Packaging and Deployment](#packaging-and-deployment)
- [Branch Protection](#branch-protection)
- [Maintainer Guide](#maintainer-guide)
- [Branch and Documentation Deployment](#branch-and-documentation-deployment)
- [GitHub Copilot](#gitHub-copilot)
- [Managing Logs and Caches](#managing-logs-and-caches)
- [Files and Directories Excluded from Version Control](#files-and-directories-excluded-from-version-control)
- [LLM Service Architecture](#llm-service-architecture)
- [Additional Resources](#additional-resources)


## Overview

The GABM developer guide provides guidance for developers and maintainers.

Please follow the [Developer Quick Start Guide](DEV_QUICKSTART.md) to get set up to contribute as a developer.


## Resume This Workstream

If you are resuming Calder/HPC reproducibility and release-prep work after a break, start here:

- Qwen3-14B reproducibility protocol + results template (primary source): [REPRODUCIBILITY_QWEN3_14B.md](REPRODUCIBILITY_QWEN3_14B.md)
- Release checklist and evidence gates (decision layer): [RELEASE_PREP_0.3.0.md](RELEASE_PREP_0.3.0.md)
- Current handover snapshot for chat_opinion calibration and next HPC steps: [HANDOVER_2026-11-10.md](HANDOVER_2026-11-10.md)
- Historical handover snapshot (context only): [HANDOVER_2026-10-30.md](HANDOVER_2026-10-30.md)
- Calder concurrent launcher (single server, many clients): [scripts/hpc/calder/run_chat_concurrency.sh](scripts/hpc/calder/run_chat_concurrency.sh)
- Run-to-run determinism comparator: [scripts/analysis/chat/compare_chat_runs.py](scripts/analysis/chat/compare_chat_runs.py)
- Markdown row generator for stress-summary tables: [scripts/analysis/chat/generate_concurrency_rows.py](scripts/analysis/chat/generate_concurrency_rows.py)

Suggested quick restart steps:

1. Confirm queued/completed Calder job IDs and run directories.
2. Update experiment outcomes in [REPRODUCIBILITY_QWEN3_14B.md](REPRODUCIBILITY_QWEN3_14B.md):
   - run determinism comparisons with `compare_chat_runs.py`
   - add stress-summary rows from `generate_concurrency_rows.py`
3. Use [RELEASE_PREP_0.3.0.md](RELEASE_PREP_0.3.0.md) to evaluate release readiness.


## Contributing and Communicating

Please follow the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

Please communicate by commenting on or raising new issue: [GABM Repository Issues](https://github.com/compolis/GABM/issues).

After forking the [GABM Repository](https://github.com/compolis/GABM) to your own GitHub account. The general workflow for contributing is to:
- Create a new local branch (or checkout a branch created upstream):

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

- Ensure tests pass and documentation builds before submitting a Pull Request (PR):

```bash
make test
make docs
```

- Push to your Fork, For example:

```bash
git push origin my_feature
```

- Open a PR on GitHub to merge your `my_feature` branch into the the `main` branch of the upstream GABM Repository.
  - Use the PR template in [.github/pull_request_template.md](.github/pull_request_template.md) to record:
    - release-note-ready bullets grouped as Added / Changed / Fixed / Docs / Infra
    - validation commands and outcomes
    - whether [CHANGE_LOG.md](CHANGE_LOG.md) was updated
  - Please refer to any related issues in the PR comments.
- The PR is to be reviewed by maintainers and accepted changes merged in due course.



## Project Directories

The root project directory contains documentation and files needed for building and deploying. The sub-directories include:
- `data/`: For data including log files
- `dist/`: Output directory for built distributions.
- `documentation/`: Authoritative long-form documentation and operational records (for example handovers)
- `docs/`: Sphinx configuration/navigation plus generated build artifacts
- `scripts/`: Utility scripts
- `scripts/analysis/`: Post-processing and analysis utilities, organized by example domain
- `scripts/analysis/chat/`: Analysis helpers for chat/chat_opinion runs and ensemble comparisons
- `scripts/analysis/chat_opinion/`: Calibration and run-summary helpers for chat_opinion
- `src/`: Python source code
- `src/gabm/examples/`: Runnable example simulation modules (source logic lives here)
- `tests/`: Test suite for src
- `tests/src/gabm/examples/`: Tests for example simulation modules
- `tests/scripts/analysis/`: Tests for analysis/post-processing script utilities
- `venv-build-test/`: For temporary virtual environments created for testing.


## Testing

GABM uses [pytest](https://docs.pytest.org/) for unit and integration tests. The unit test suite is located in the `tests/` directory, mirroring the module structure.

### Running Tests

Run most tests with:
  ```bash
  make test
  ```
or:
  ```bash
  pytest
  ```
By default, tests marked as `@pytest.mark.slow` are excluded (see `pytest.ini`). Run slow tests with:

  ```bash
  pytest -m slow
  ```

By default, tests marked as `@pytest.mark.live_llm` are also excluded. These tests require external LLM service access and are not suitable for offline/HPC compute-node default test runs.

Run live external LLM tests with:

  ```bash
  pytest -m live_llm
  ```

### Adding Tests

Please add or update tests when modifying or adding features. Aim for high test coverage to catch regressions and ensure code reliability.

For sustainability and maintainability, functional source code modules are expected to have corresponding tests. In practice, each non-trivial module under `src/gabm/` should have at least one test module under `tests/src/gabm/`.

Mark slow or resource-intensive tests with `@pytest.mark.slow` and set a timeout if needed (e.g., `@pytest.mark.timeout()`).

### Test Data and Fixtures

Store test-only fixture files under `tests/data/` (for example, `tests/data/input/`).

Do not place test fixtures in `data/`, as that directory is intended for runtime/demo inputs and generated logs.

When tests need file-based inputs, prefer paths under `tests/data/` so tests are self-contained and do not depend on mutable runtime data.

For simulation example tests, output artifacts should be written under the corresponding test example directory (for example, `tests/src/gabm/examples/chat/output/`) so output location is explicit and colocated with the tests.

### Local LLM Tests

Tests for local LLMs (e.g., Apertus) are marked as slow and excluded by default as these tests require significant hardware resources (GPU recommended). On CPU-only machines, inference may be extremely slow or impractical.

To run local LLM tests, ensure your environment is suitable and use:
  ```bash
  pytest -m slow
  ```

To run all optional LLM-related tests (local and live external) when your environment supports it, use:
  ```bash
  pytest -m "slow or live_llm"
  ```

## Example Simulations and Reproducibility

Example simulation logic should live in `src/gabm/examples/...` and be importable. Tests should live in `tests/src/gabm/examples/...` and validate reproducibility.

Recommended pattern:
- Put executable simulation logic in `src/gabm/examples/<example_name>/sim.py`.
- Keep tests in `tests/src/gabm/examples/<example_name>/test_sim.py`.
- Expose a callable (for example `run(...)`) from the source simulation module so tests can execute it directly.

### chat_opinion Calibration Workflow (2026-11)

To calibrate opinion-formation dynamics without changing code constants each time:

1. Run local no-cache pilots for baseline and candidate drift profiles.
2. Run small local no-cache sweeps (`N_RUNS=6` to `10`) for normal and awkward modes.
3. Compare `final_mean_opinion`, `delta_mean_opinion`, and `final_opinion_gap` ranges and stats.
4. Promote one profile to a small Calder pilot with matching seed windows and rounds.

New drift parameters exposed by Makefile wrappers and CLI:

- `QUESTION_BONUS`
- `POSITIVE_TOKEN_BONUS`
- `NEGATIVE_TOKEN_PENALTY`
- `SHARED_INTEREST_CAP`

Helpful summary command:

```bash
make summarize-chat-opinion-runs INPUTS='--run-id <run_a> --run-id <run_b>'
```

### Person Naming in Examples

`Person` has name state and assignment logic:
- You can pass `name` directly when constructing a `Person`.
- If `name` is omitted, `Person` auto-assigns a name from ONS male/female CSV tables using age (year of birth) and gender.
- Getter/setter methods are available via `get_name()` and `set_name()`.

For chat examples and similar simulations, prefer wiring naming through model creation rather than assigning names in the example script:
- Pass ONS file overrides into environment-level person creation (`create_random_people(..., ons_male_file=..., ons_female_file=...)`).
- Read names from person instances (`person.get_name()`) in prompts/transcripts.

Default ONS input paths are expected under `data/input/abm/`.

Reproducibility requirements for simulation tests:
- Prefer deterministic behavior by explicitly setting random seeds.
- Avoid hidden randomness from global state; use local RNG objects where practical.
- When generating multiple stochastic dimensions (for example traits and interests), derive separate deterministic seeds to avoid unintended cross-coupling while preserving reproducibility.
- Validate output reproducibility by running the same simulation twice with the same seed and asserting identical outputs.
- Where useful, also assert that changing the seed changes the output.

LLM-specific reproducibility guidance:
- External LLM responses may drift over time, so strict reproducibility should not depend on live external API calls.
- Use prompt/response caches when tests should replay known interactions.
- Local LLM reproducibility tests (for example on HPC) should be marked slow and optional.
- In HPC environments where compute nodes have no external access, avoid requiring external LLM calls in default test runs.
- Some code changes do not require clearing LLM caches; cache clearing should be periodic or intentional (for example, after LLM integration changes).
- Periodically run a cache-cleared LLM verification pass (for example using `make clear-caches` followed by targeted LLM tests) to detect service/API drift.

### Reproducibility Checklist

When adding or updating a simulation example, check the following:
- Simulation logic is in `src/gabm/examples/<example_name>/sim.py` and is importable.
- Test logic is in `tests/src/gabm/examples/<example_name>/test_sim.py`.
- A fixed seed is used for deterministic test runs.
- Independent random streams are used where separate stochastic processes are modeled (for example traits vs interests).
- Running the same simulation twice with the same seed gives identical outputs.
- Changing the seed is tested and expected to change outputs (where randomness is intended).
- Output paths for tests are explicit and under `tests/src/gabm/examples/.../output/` or `tmp_path`.
- Tests do not require external network calls in the default `make test` path.
- LLM-related tests are correctly marked as `slow` and/or `live_llm`.

### Test Workflow

- PRs should pass the test workflow before being merged.
- See `.github/workflows/test.yml` for Continuous Integration (CI) details.

### CI and LLM Drift Checks

The default CI workflow should continue to run `make test` only, excluding `slow` and `live_llm` tests for reliability and portability.

Maintainers should run `make llm-drift-check` periodically and especially in these cases:
- Before cutting a release.
- After changes to LLM service implementations, prompts, model names, or request/response handling.
- After dependency updates that can affect LLM client behavior.

In environments without outbound network access (for example HPC compute nodes), skip drift checks and run them in a suitable connected environment instead.

### Useful pytest markers
- `@pytest.mark.slow`: Marks tests as slow; skipped by default.
- `@pytest.mark.live_llm`: Marks tests that require live external LLM APIs; skipped by default.
- `@pytest.mark.timeout(seconds)`: Fails test if it exceeds the given duration.

### Note on DeprecationWarnings
You may see DeprecationWarnings related to protobuf (e.g., `Type google._upb._message.MessageMapContainer uses PyType_Spec with a metaclass that has custom tp_new`).
These warnings originate from upstream libraries (e.g., Google APIs) and do not affect GABM functionality. They are expected to be resolved in future library updates. Please ignore them unless they cause test failures or runtime errors.


## Network Utilities

`gabm.abm.networks` provides seeded graph builders for stochastic-block,
Erdős–Rényi, Watts–Strogatz, Barabási–Albert, and similarity-weighted
networks, along with structural diagnostics and deterministic component
repair. Builders accept caller-owned node IDs; the stochastic-block and
similarity-weighted variants also accept caller-supplied block labels or
feature rows. Domain-specific attribute selection and research defaults
belong in the application using these utilities.

## Two-stage Survey Execution

`gabm.abm.survey.execute_two_stage_question` is an optional reasoning-then-answer
executor. It accepts exact prompts and an injected
`send(system_prompt, user_prompt, stage)` callable (`stage` is `"reasoning"` or
`"answer"`). It records no agent state and adds no parsing, provider selection,
retries, or caching. Existing `SurveyConversation` behaviour is unchanged.

The required `on_reasoning` callback runs before the answer context is built or
sent, allowing applications to record intermediate state in event order.
`build_answer_system(system_prompt, reasoning)` controls the exact second-call
context; no domain-specific wording is added. Exceptions propagate immediately,
and completed application recording is not rolled back.

For example, this needs no credentials or real respondent data:

```python
from gabm.abm.survey import execute_two_stage_question

recorded = []
result = execute_two_stage_question(
    system_prompt="You are a library visitor.",
    reasoning_prompt="What matters when choosing a reading room?",
    answer_prompt="Choose A: lively or B: quiet.",
    send=lambda system, user, stage: (
        "I prefer quiet spaces." if stage == "reasoning" else "B"
    ),
    build_answer_system=lambda system, reasoning: f"{system}\nNotes: {reasoning}",
    on_reasoning=recorded.append,
)
assert recorded == [result.reasoning]
assert result.answer == "B"
```

Questions, prompt protocols, response validation/scoring, histories, and audit
metadata remain application-owned. This API does not require `Person`
inheritance and is not the mandatory protocol for all surveys.

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
| `make llm-drift-check` | Clear caches and run live LLM integration tests (for periodic drift checks) |
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
| `make run-example-chat` | Run the chat example simulation with ONS-backed names from `data/input/abm/` |
| `make compare-hpc-chat-runs RUN_A=... RUN_B=...` | Compare two HPC chat run directories via transcript/metadata/cache hashes |
| `make summarize-hpc-concurrency INPUTS='...'` | Generate markdown rows from `launcher_summary.log` files |
| `make report-hpc-chat-runs INPUTS='...' [OUTPUT=...]` | Generate a single markdown reproducibility report for multiple HPC runs |


All Python scripts used by Makefile targets are in the `scripts/` directory and are named consistently with their Makefile targets (e.g., `make docs-clean` runs `scripts/docs-clean.py`).

The `delete-release` target automates deleting a release tag locally and on both remotes (origin, upstream).

Please refer to the Makefile for full details.


## Developing Documentation

Documentation now follows a split model:

- `documentation/` contains maintained long-form project documentation.
- `docs/` is the Sphinx build/navigation surface.
- Root Markdown files remain as compatibility entry points during migration.

Where to place new documentation:

- Put authored/maintained narrative content in `documentation/` (for example handovers, process notes, research notes).
- Keep Sphinx structure/navigation and generated content in `docs/`.
- Only add new root-level Markdown docs when needed for compatibility or high-visibility entry points.

Markdown files in the root directory, each serving a specific purpose:
  - [README.md](README.md): A general [README](https://en.wikipedia.org/wiki/README) that links to much of the documentation outlined below including the developer and user guides. It is included in the Sphinx documentation and forms the basis for the main Sphinx documentation page.
  - [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): Provides details on expected behavior of developers and reporting procedures.
  - [USER_GUIDE.md](USER_GUIDE.md): Provides step-by-step instructions for users to get set up, and should provide guidance for using GABM.
  - [DEV_QUICKSTART.md](DEV_QUICKSTART.md) Provides step-by-step instructions for developers to get set up for contributing to GABM development.
  - [DEV_GUIDE.md](DEV_GUIDE.md): Explains how to contribute to GABM as a developer. It provides details about project structure, and workflow guidance.
  - [API_KEYS.md](API_KEYS.md): Explains how to create a file containing API keys for communicating with LLMs.
  - [ROADMAP.md](ROADMAP.md): Document to outline planned features and future development goals.
  - [CHANGE_LOG.md](CHANGE_LOG.md): Document to describe changes and updates.
  - [DEVELOPMENT_HISTORY.md]: Document about development, milestones, and reflections.

- If you add a new Markdown file in the root directory, please update entries in `scripts/dev/docs_assets.py` (`DOC_FILES`) and `docs/index.md` Project Documents so Sphinx includes them.

Documentation-organization approach (aligned with ClimateAction-GABM direction):
- Prefer [documentation/](documentation/) as the primary authored-docs home.
- Use [docs/](docs/) as the Sphinx build/navigation surface.
- Keep root-level canonical files during transition to avoid breaking existing links/workflows.
- Add new operational snapshots as dated files (for example handovers), and include them in `docs/index.md`.
- Migrate in stages by topic rather than doing a one-shot file move.


### Sphinx Documentation

To build run:

```bash
make docs
```

- This effectively runs `scripts/dev/docs.py` to copy key documentation files from the project root to the `docs/` directory and pre-process them for Sphinx builds.

**Note on Sphinx/MyST Documentation Warnings:**

When building the documentation with [Sphinx](https://www.sphinx-doc.org/) and [MyST](https://mystmd.org/), you may see warnings like:

  Document headings start at H2, not H1 [myst.header]
  document isn't included in any toctree [toc.not_included]
  duplicate object description ... use :no-index: for one of them
  WARNING: Field list ends without a blank line; unexpected unindent. [docutils]
  'myst' cross-reference target not found: ... [myst.xref_missing]

These warnings are common with Sphinx/Autosummary/MyST and do not affect the rendered documentation if the HTML output looks correct. In particular, myst.xref_missing means that a Markdown/MyST cross-reference (e.g., {ref}`target`) could not be resolved. If the documentation renders correctly and the missing reference is not critical, these can be safely ignored. You can safely ignore all these warnings unless the formatting in the HTML output is incorrect or a critical feature is missing.


Preview the Sphinx documentation by opening `docs/_build/html/index.html` in a [Web browser](https://en.wikipedia.org/wiki/Web_browser).

To deploy the Sphinx Documentation run:

```bash
make gh-pages-deploy
```

This should deploy/update the `gh-pages` branch on your origin Fork. If your Fork uses the `gh-pages` branch for [GitHub Pages](https://docs.github.com/en/pages), then the documentation should update there.

If it all looks good. Please submit a PR to incorporate documentation changes into main. A maintainer will subsequently update the upstream repository gh-pages branch.

#### Sphinx API Documentation and Autosummary


GABM uses Sphinx with the autosummary extension to generate API documentation for all major modules. To document new modules:

- Import the new module in the appropriate `__init__.py` file so Sphinx can discover it (e.g., add `from .my_module import *`).
- Add the module to the API Reference toctree in `docs/index.md` (as an `_autosummary/` entry) to ensure it appears in the documentation navigation.
- You do not need to manually maintain individual `.rst` files for each module; autosummary will generate them automatically during `make docs`.
- If you remove or rename modules, update both the `__init__.py` imports and the API Reference list in `docs/index.md`.
- You may delete stale `.rst` files in `_autosummary` if they are no longer referenced.

Preview the Sphinx documentation by opening `docs/_build/html/index.html` in a web browser.


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

PRs to the [GABM Repository main branch](https://github.com/compolis/GABM/tree/main) must pass the test workflow before merging.

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

## Archiving Historical Notes

To keep root-level documentation focused on active guidance:

- Keep current/active operational and developer guidance in root markdown files.
- Move time-bound snapshots (for example handover notes, dated experiment summaries, or superseded one-off runbooks) into [archive/](archive/).
- Mirror archived markdown files in [docs/archive/](docs/archive/) when they should appear in built Sphinx documentation navigation.
- If preserving old links is useful, keep a short root-level stub page that points to:
  - the active guide, and
  - the archived snapshot.

## GitHub Copilot

Using [GitHub Copilot](https://github.com/features/copilot) for [vibe coding](https://en.wikipedia.org/wiki/Vibe_coding), can help with understanding workflows and developing documentation, code and tests.

GitHub Copilot uses limited context and the chat context does not currently persist between sessions. As a result, it is good to develop/update documentation along with changes. GitHub Copilot can be asked to read the [README](README.md) and [Developer Guide](DEV_GUIDE.md) at the start of a session so as to be more context aware and provide better support.


## Managing Logs and Caches

Logs and caches (including prompt/response caches for LLM services) are generated during development and use. These files can become large. Typically they are not committed to the repository.

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
- `data/llm/*/prompt_response_cache.pkl` — LLM response cache files
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

- [HUGGING_FACE.md](HUGGING_FACE.md) — for details on obtaining and using local Apertus and other Hugging Face models

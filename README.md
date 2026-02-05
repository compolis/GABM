#
<!-- Badges -->
<p align="left">
  <a href="https://github.com/compolis/gabm/actions/workflows/ci.yml" title="Build Status">
    <img src="https://img.shields.io/github/actions/workflow/status/compolis/gabm/ci.yml?branch=main&label=build" alt="Build Status" />
  </a>
  <a href="https://github.com/compolis/gabm/blob/main/LICENSE" title="License">
    <img src="https://img.shields.io/github/license/compolis/gabm" alt="License" />
  </a>
  <a href="https://www.python.org/downloads/" title="Python Version">
    <img src="https://img.shields.io/badge/python-3.9%2B-blue.svg" alt="Python Version" />
  </a>
  <a href="https://compolis.github.io/gabm/" title="Documentation">
    <img src="https://img.shields.io/badge/docs-Sphinx-green" alt="Documentation" />
  </a>
</p>
> **Note for Fork Maintainers:**  
> The badges and clone URLs above reference the canonical compolis/gabm repository.  
> If you fork this project and want badges to reflect your fork’s status, update all `compolis/gabm` URLs to your own GitHub username/repo.

# GABM: Generative Agent-Based Model

[//]: # (Table of Contents)
## Table of Contents
- [Overview](#overview)
- [Roadmap](#roadmap)
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Set Up Your Environment](#2-set-up-your-environment)
  - [Recommended Tools & IDEs](#recommended-tools--ides)
  - [API Keys](#3-api-keys)
  - [LLM Setup and Onboarding](#4-llm-setup-and-onboarding)
  - [Running the Code](#5-running-the-code)
- [Usage](#usage)
- [Model Management & Caching](#model-management--caching)
- [Contribution Workflow](#contribution-workflow)
- [Makefile Reference](#makefile-reference)
- [Documentation](#documentation)
- [License](#license)
- [Centralized Logging](#centralized-logging)
- [Files and Directories Excluded from Version Control](#files-and-directories-excluded-from-version-control)
- [Documentation Build Workflow](#documentation-build-workflow)
- [Acknowledgements](#acknowledgements)

## Overview

GABM is a flexible, extensible Python framework for agent-based modeling (ABM) with a focus on integrating large language models (LLMs) as agent reasoning engines. It supports multiple LLM providers, persistent response caching, and robust onboarding for new users and contributors.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned next steps and future goals.

To create and push a release tag:

1. Ensure all changes are committed and pushed to the main branch.
2. Run:

   ```bash
   make release VERSION=x.y.z
   ```

   Replace `x.y.z` with the desired version number (e.g., `0.1.0`).
3. The release will be tagged and pushed to the remote repository.

See [CHANGE_LOG.md](CHANGE_LOG.md) for details of each release.

## Code of Conduct

Please see our [Code of Conduct](CODE_OF_CONDUCT.md) for guidelines on expected behavior and reporting issues.

## Getting Started

### 1. Clone the Repository
First, fork the upstream repository on GitHub to your own account. Then, clone your fork:

For a detailed, step-by-step walkthrough (including example output and troubleshooting), see [SETUP_GUIDE.md](SETUP_GUIDE.md).
git clone https://github.com/compolis/gabm.git
cd gabm

> **Note for Developers:**
> 
> The documentation files in the `docs/` directory (such as `README.md`, `ROADMAP.md`, `CHANGE_LOG.md`, `CODE_OF_CONDUCT.md`, `SETUP_GUIDE.md`, `CONTRIBUTORS`, and `LICENSE`) are automatically copied from the project root as part of the documentation build process. **Do not edit these files in `docs/` directly.** Always edit the originals in the project root.

### 2. Set Up Your Environment

Install Python 3.9+ and pip if you haven't already. Then install dependencies:

```bash
pip install -r requirements.txt
```

#### Recommended tools

- [Visual Studio Code](https://code.visualstudio.com/) is recommended for its excellent Python support and [GitHub Copilot](https://github.com/features/copilot) integration.
- Other good Python IDEs include [Spyder](https://www.spyder-ide.org/) (scientific workflow) and [PyCharm](https://www.jetbrains.com/pycharm/).
- [Make](https://www.gnu.org/software/make/) is used for build and clean workflow automation. All Makefile targets in this project are platform-agnostic and work on both Windows and Unix-like systems.
- You are free to use any editor, IDE, or workflow you prefer.


### 3. API Keys
You need a `data/api_key.csv` file with your API keys. This file is not included in the repository for security reasons.

> **Security Warning:** Never commit your API keys or other secrets to the repository. The `.gitignore` file is configured to exclude `data/api_key.csv` and other sensitive files from version control. Always keep your keys private and secure.

Ask the project maintainer for a template or example, or create it yourself with the following format (CSV with header):

```
api,key
openai,sk-...
deepseek,sk-...
genai,YOUR_GOOGLE_KEY
```

Place this file in the `data/` directory.

### 4. LLM Setup and Onboarding
To quickly initialize your environment, test your API keys, and generate model lists and caches for all supported LLMs, use the provided setup utility:

```bash
make setup-llms
```

This will:
- Check for all required API keys (OpenAI, GenAI, DeepSeek)
- Test each key with a default prompt and model
- Generate initial `models.json` and `models.txt` for each LLM
- Initialize response caches (`cache.pkl`)
- Report any issues or missing keys

If you need to clear all caches and model lists (for a fresh start or troubleshooting), use:
```bash
make clear-caches
```

**Note:** Model list files (`models.json`, `models.txt`) are lists of available models for each LLM service. This might change over time. To save generating the lists these are committed to the repository. Cache files (`cache.pkl`) are prompt/response data from each LLM service. These are currently not committed to the repository as they may become large. However, the intention is to store caches of prompts/responses and details of the Agent Based Models when run to generate results and explore reproducibility.

### 5. Running the Code
From the project root, run:

```bash
python3 run.py
```

## Usage

### Running the Main Program

```bash
python3 run.py
```

### Example: Persona Test Agent Fills Survey

```bash
python3 src/io/persona_test_agent_fills_survey_v1.py
```

## Model Management & Caching

- All LLM responses are cached in `data/llm_cache/` (pickled)
- Model lists are cached in `data/model_lists/` (JSON/TXT)
- Use `make clear-caches` to clear all caches

### Supported LLM Providers
- DeepSeek

### Model Listing, Caching, and Validation
When a model list is fetched, it is cached locally. LLM responses are also cached for efficiency and reproducibility.

When running the main script, the selected model for each LLM is checked against the cached JSON model list. If the model is not found, a warning is shown and the available models can be listed automatically.

This workflow is consistent across all LLMs, making it easy to add new providers or update model selection logic.

#### Model Selection (Explicit Required)

When running the main script, you must explicitly set the model name for each LLM provider in `run.py`. There are no defaults—this ensures clarity and prevents accidental use of deprecated or unsupported models.

To select a model, set the variable (e.g., `openai_model`, `genai_model`, `deepseek_model`) at the top of the main function in `run.py`.

If you do not set a model, the script will raise an error and prompt you to specify one.

To see available models, run the model listing function for each provider or check the generated `models.json` file in `data/llm/{provider}/`.

Example:
```python
openai_model = "gpt-3.5-turbo"
genai_model = "gemini-pro"
deepseek_model = "deepseek-model-1"
```

See the API documentation and module docstrings for more details on how model management is implemented and used in the codebase.

## Contribution Workflow

**Note:** The `main` branch is protected. All changes must be made through Pull Requests, which require at least one review and approval before merging. Direct pushes to `main` are not allowed. This ensures code quality and collaborative review.

### How to Contribute

1. Add your name to the `__author__` list in any Python file you edit.
2. Increment the `__version__` string in the file if you make a significant change.
3. Submit a pull request with a clear description of your changes.

### Example Metadata Block

```python
__author__ = ["Alice Smith", "Bob Jones"]
__version__ = "0.2.1"
__copyright__ = "2024-present Alice Smith, Bob Jones"
```

### Contributor Best Practices

- Keep `__author__` as a list (not a string)
- Update `__version__` for meaningful changes
- Add yourself to the list in every file you touch

### Contributor Checklist (for PRs)
- [ ] Increment the `__version__` string for significant changes
- [ ] Update the CHANGE_LOG.md with a summary of your changes
- [ ] Ensure all tests pass and documentation builds
- **Major**: Increment for incompatible API changes or major new features.
- **Minor**: Increment for backward-compatible feature additions or improvements.
- **Fix**: Increment for backward-compatible bug fixes or minor changes.

Example: `0.2.1` → `0.2.2` (fix), `0.3.0` (minor), `1.0.0` (major).

If you contribute code to this project, please:

- Add your name and email to the end of the `__author__` list in any Python file you edit.
- Increment the `__version__` string if you make a significant change.
- Optionally, add a short comment in the file or in your pull request describing your contribution.

Example:
```python
__author__ = [
  "Andy Turner <agdturner@gmail.com>",
  "Your Name <your.email@example.com>"
]
```

This helps ensure proper attribution and makes it easy to track contributors. For large or multi-author changes, consider also updating this README or adding a CONTRIBUTORS file.

## Makefile Reference


### Common Targets


- `make git-clean` — Clean up merged local branches and prune deleted remotes. This target automatically checks out the `main` branch before deleting merged branches to avoid errors if the active branch is merged and needs deletion.

### Python Scripts Used by Makefile Targets

| Script                        | Used by Target    | Purpose                                                      |
|-------------------------------|-------------------|--------------------------------------------------------------|
| scripts/update_docs_assets.py  | docs              | Copies and normalizes Markdown docs for Sphinx               |
| scripts/clean_docs_assets.py   | docs-clean        | Removes auto-copied docs assets from docs/                   |
| scripts/clean_project.py       | clean             | Removes build/test artifacts and Python caches               |
| scripts/clear_caches.py        | clear-caches      | Deletes all LLM/model caches and model lists                 |
| scripts/gh_pages_deploy.py     | gh-pages          | Builds and deploys Sphinx docs to the gh-pages branch        |

- All scripts are in the `scripts/` directory at the project root.
- These scripts ensure all Makefile targets are platform-agnostic and reproducible.

## Documentation

```bash
make docs
```

Docs are generated with Sphinx and output to `docs/_build/html/`.

> **To view the documentation:** Open `docs/_build/html/index.html` in your web browser after running `make docs`.

### Adding New Modules to the Documentation

To add a new module to the docs:
1. Create a new .rst file in the appropriate directory under `docs/`.
2. Add the `automodule` directive for your module.
3. Reference the new .rst file in the `toctree` in `index.rst`.
4. Run `make docs` to rebuild the documentation.

This structure keeps documentation organized and easy to extend as the codebase grows.

---
**Note on Sphinx/MyST Documentation Warnings:**

When building the documentation with Sphinx and MyST, you may see warnings like:

  Document headings start at H2, not H1 [myst.header]

These warnings occur even though all Markdown files start with H2 (`##`). This is a known quirk with MyST/Sphinx and does not affect the rendered documentation. You can safely ignore these warnings unless the formatting in the HTML output is incorrect.
---

## LLM Model Listing, Caching, and Validation

This project supports multiple LLM providers (OpenAI, GenAI, DeepSeek, Anthropic) with a unified workflow for model management:

- **Model Listing:** Each LLM module provides a function to fetch and list available models from the provider's API. The full model list is saved as both JSON (machine-readable) and TXT (human-readable) in the corresponding `data/llm/{provider}/` directory.
- **Caching:** When a model list is fetched, it is cached locally. LLM responses are also cached for efficiency and reproducibility.
- **Validation:** When running the main script, the selected model for each LLM is checked against the cached JSON model list. If the model is not found, a warning is shown and the available models can be listed automatically.
- **Extensibility:** This workflow is consistent across all LLMs, making it easy to add new providers or update model selection logic.

### LLM Model Selection (Explicit Required)

When running the main script, you must explicitly set the model name for each LLM provider in `run.py`. There are no defaults—this ensures clarity and prevents accidental use of deprecated or unsupported models.

- To select a model, set the variable (e.g., `openai_model`, `genai_model`, `deepseek_model`) at the top of the main function in `run.py`.
- If you do not set a model, the script will raise an error and prompt you to specify one.
- To see available models, run the model listing function for each provider or check the generated `models.json` file in `data/llm/{provider}/`.

Example:
```python
openai_model = "gpt-3.5-turbo"
genai_model = "gemini-pro"
deepseek_model = "deepseek-model-1"
```

See the API documentation and module docstrings for more details on how model management is implemented and used in the codebase.

## Centralized Logging

All major modules and utilities in GABM use a centralized logging system. In addition to any console output, each LLM module and utility writes detailed logs automatically to the `data/logs/` directory. These logs include setup steps, API calls, warnings, and errors, making troubleshooting and reproducibility easier. See the [SETUP_GUIDE.md](SETUP_GUIDE.md) for details on how to view and use these logs.

## Files and Directories Excluded from Version Control

Certain files and directories are intentionally excluded from the repository via `.gitignore` to keep the project clean and secure:

- `data/logs/` — All log files generated by scripts and modules (can be large and environment-specific)
- `data/llm/*/cache.pkl` — LLM response cache files (can be large and are not needed for collaboration)
- `data/api_key.csv` — API keys (never commit secrets)

If you do not see these files or folders in the repository, this is expected. Each collaborator should generate their own as needed by following the setup guide.

- If you want to link to Markdown files (like ROADMAP.md, CHANGE_LOG.md, CODE_OF_CONDUCT.md, SETUP_GUIDE.md, CONTRIBUTORS, LICENSE) in the Sphinx docs, ensure they are present in the docs/ directory or use plain Markdown links (e.g., `[ROADMAP.md](../ROADMAP.md)`) instead of MyST cross-references. Otherwise, Sphinx will warn about missing references.
- If you want to include a file in the Sphinx navigation, add it to a toctree in index.rst. If not, remove or comment out the reference.

## Documentation Build Workflow

- The Makefile `docs` target automatically runs `scripts/update_docs_assets.py` to copy key documentation files (README.md, ROADMAP.md, etc.) from the project root to the `docs/` directory and update their internal links for Sphinx.
- **Edit only the originals in the project root.** Do not edit the auto-copied files in `docs/`—they will be overwritten.
- `.rst` files in `docs/` are meant to be created, edited, and maintained by developers for Sphinx documentation.
- This workflow ensures that all documentation is up to date, cross-referenced, and easy to navigate in both the repository and the generated HTML docs.

> **Platform Agnostic:** All core developer workflows (build, clean, cache management, docs, deployment) are fully platform-agnostic and work on both Windows and Unix-like systems. You can develop and contribute using your preferred OS.


## License

See [LICENSE](LICENSE).


## Acknowledgements

This project was developed with significant assistance from [GitHub Copilot](https://github.com/features/copilot) for code generation, refactoring, and documentation improvements.

We gratefully acknowledge support from the [University of Leeds](https://www.leeds.ac.uk/). Funding for this project comes from a UKRI Future Leaders Fellowship awarded to [Professor Viktoria Spaiser](https://essl.leeds.ac.uk/politics/staff/102/professor-viktoria-spaiser) (grant reference: [UKRI2043](https://gtr.ukri.org/projects?ref=UKRI2043)).
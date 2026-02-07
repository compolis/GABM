---
title: Project README
---


# GABM: Generative Agent-Based Model


## Overview

GABM is a flexible, extensible Python framework for agent-based modeling (ABM) with a focus on integrating large language models (LLMs) as agent reasoning engines. It supports multiple LLM providers, persistent response caching, and robust onboarding for new users and contributors.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned next steps and future goals.

To create and push a release tag:

1. Ensure all changes are committed and pushed to the main branch.
2. Run:

```
   make release VERSION=x.y.z
```

   Replace `x.y.z` with the desired version number (e.g., `0.1.0`).
3. The release will be tagged and pushed to the remote repository.

See [CHANGE_LOG.md](CHANGE_LOG.md) for details of each release.


## Code of Conduct and Reporting

Please see our [Code of Conduct](CODE_OF_CONDUCT.md) for guidelines on expected behavior and reporting issues.

For security or conduct concerns, you can also use the “Contact maintainers” link on the GitHub repository, or see the [SECURITY.md](SECURITY.md) file in the documentation for details on confidential reporting.

## Getting Started

### 1. Clone the Repository
First, fork the [upstream repository](https://github.com/compolis/GABM) on GitHub to your own account. Then, clone your fork locally:

> Replace `<your-username>` with your GitHub username in the commands below.

```
git clone https://github.com/<your-username>/GABM.git

```
or
```
git clone git@github.com:<your-username>/gabm.git

```

#### Recommended: Onboard with the Latest Stable Release
For the most reliable onboarding experience, checkout the latest stable release branch (e.g., `stable/0.1.0`).
```
git checkout stable/0.1.0
```

This branch contains the most tested and stable code. For development or contributing, use the main or feature branches.


For a detailed, step-by-step walkthrough, see:

- [User Setup Guide](SETUP_GUIDE_USER.md) — for end users who want to run GABM
- [Developer Setup Guide](SETUP_GUIDE_DEV.md) — for contributors and advanced users


> **Note for Developers:**


> 

> The documentation files in the `docs/` directory (such as `README.md`, `ROADMAP.md`, `CHANGE_LOG.md`, `CODE_OF_CONDUCT.md`, `SETUP_GUIDE_USER.md`, `SETUP_GUIDE_DEV.md`, `CONTRIBUTORS`, and `LICENSE`) are automatically copied from the project root as part of the documentation build process. **Do not edit these files in `docs/` directly.** Always edit the originals in the project root.

### 2. Set Up Your Environment


Install Python 3.12 or higher and pip if you haven't already.

#### User Setup (Recommended for most users)

Install only the core runtime dependencies:

```
pip install -r requirements.txt
```

#### Developer Setup (For contributors, testing, and docs)

Install all runtime, development, and documentation dependencies:

```
pip install -r requirements-dev.txt
```

**[requirements.md](requirements.md)** contains only the packages needed to run GABM as a user.

**[requirements-dev.md](requirements-dev.md)** includes everything in requirements.txt plus extra packages for development, testing, and building documentation (e.g., pytest, Sphinx, linters).

Use the developer setup if you plan to contribute code, run tests, or build the documentation locally.

#### Recommended tools

- [Visual Studio Code](https://code.visualstudio.com/) is recommended for its excellent Python support and [GitHub Copilot](https://github.com/features/copilot) integration.

- Other good Python IDEs include [Spyder](https://www.spyder-ide.org/) (scientific workflow) and [PyCharm](https://www.jetbrains.com/pycharm/).

- [Make](https://www.gnu.org/software/make/) is used for build and clean workflow automation. All Makefile targets in this project are platform-agnostic and work on both Windows and Unix-like systems.

- You are free to use any editor, IDE, or workflow you prefer.


### 3. API Keys
See [API_KEYS.md](API_KEYS.md) for instructions on setting up your API keys and initializing your environment.

### 4. LLM Setup and Onboarding
To quickly initialize your environment, test your API keys, and generate model lists and caches for all supported LLMs, use the provided setup utility:

```
make setup-llms
```

This will:

- Check for all required API keys (OpenAI, GenAI, DeepSeek)
- Test each key with a default prompt and model
- Generate initial `models.json` and `models.txt` for each LLM
- Initialize response caches (`cache.pkl`)
- Report any issues or missing keys

If you need to clear all caches and model lists (for a fresh start or troubleshooting), use:

```
make clear-caches
```

**Note:** Model list files (`models.json`, `models.txt`) are lists of available models for each LLM service. This might change over time. To save generating the lists these are committed to the repository. Cache files (`cache.pkl`) are prompt/response data from each LLM service. These are currently not committed to the repository as they may become large. However, the intention is to store caches of prompts/responses and details of the Agent Based Models when run to generate results and explore reproducibility.

### 5. Running the Code
From the project root, run:

```
python3 run.py
```

## Usage

### Running the Main Program

```
python3 run.py
```

### Example: Persona Test Agent Fills Survey

```
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

```
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

```
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

```
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

| scripts/update_docs_assets.py  | docs              | Copies and normalizes Markdown docs for Sphinx               |
| scripts/clean_docs_assets.py   | docs-clean        | Removes auto-copied docs assets from docs/                   |
| scripts/clean_project.py       | clean             | Removes build/test artifacts and Python caches               |
| scripts/clear_caches.py        | clear-caches      | Deletes all LLM/model caches and model lists                 |
| scripts/gh_pages_deploy.py     | gh-pages          | Builds and deploys Sphinx docs to the gh-pages branch        |

- All scripts are in the `scripts/` directory at the project root.
- These scripts ensure all Makefile targets are platform-agnostic and reproducible.


## Documentation

Project documentation is available in the `docs/` directory and online via GitHub Pages.

- See [`DEV_GUIDE.md`](DEV_GUIDE.md) for developer workflow, collaboration, Makefile targets, and project structure.
- See [`USER_GUIDE.md`](USER_GUIDE.md) for user guidance, support, and future configuration instructions.
- See `SETUP_GUIDE_DEV.md` and `SETUP_GUIDE_USER.md` for environment setup instructions.

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

```
openai_model = "gpt-3.5-turbo"
genai_model = "gemini-pro"
deepseek_model = "deepseek-model-1"
```

See the API documentation and module docstrings for more details on how model management is implemented and used in the codebase.

## Centralized Logging

All major modules and utilities in GABM use a centralized logging system. In addition to any console output, each LLM module and utility writes detailed logs automatically to the `data/logs/` directory. These logs include setup steps, API calls, warnings, and errors, making troubleshooting and reproducibility easier. See the [Developer Setup Guide](SETUP_GUIDE_DEV.md) for details on how to view and use these logs.

## Files and Directories Excluded from Version Control

Certain files and directories are intentionally excluded from the repository via `.gitignore` to keep the project clean and secure:

- `data/logs/` — All log files generated by scripts and modules (can be large and environment-specific)
- `data/llm/*/cache.pkl` — LLM response cache files (can be large and are not needed for collaboration)
- `data/api_key.csv` — API keys (never commit secrets)

If you do not see these files or folders in the repository, this is expected. Each collaborator should generate their own as needed by following the setup guide.

- If you want to link to Markdown files (like ROADMAP.md, CHANGE_LOG.md, CODE_OF_CONDUCT.md, SETUP_GUIDE_USER.md, SETUP_GUIDE_DEV.md, CONTRIBUTORS, LICENSE) in the Sphinx docs, ensure they are present in the docs/ directory or use plain Markdown links (e.g., `[ROADMAP.md](../ROADMAP.md)`) instead of MyST cross-references. Otherwise, Sphinx will warn about missing references.
- If you want to include a file in the Sphinx navigation, add it to a toctree in index.rst. If not, remove or comment out the reference.

## Documentation Build Workflow

- The Makefile `docs` target automatically runs `scripts/update_docs_assets.py` to copy key documentation files (README.md, ROADMAP.md, etc.) from the project root to the `docs/` directory and update their internal links for Sphinx.
- **Edit only the originals in the project root.** Do not edit the auto-copied files in `docs/`—they will be overwritten.
- `.rst` files in `docs/` are meant to be created, edited, and maintained by developers for Sphinx documentation.
- This workflow ensures that all documentation is up to date, cross-referenced, and easy to navigate in both the repository and the generated HTML docs.

> **Platform Agnostic:** All core developer workflows (build, clean, cache management, docs, deployment) are fully platform-agnostic and work on both Windows and Unix-like systems. You can develop and contribute using your preferred OS.


## License

See [LICENSE](LICENSE.md).


## Acknowledgements

This project was developed with significant assistance from [GitHub Copilot](https://github.com/features/copilot) for code generation, refactoring, and documentation improvements.

We gratefully acknowledge support from the [University of Leeds](https://www.leeds.ac.uk/). Funding for this project comes from a UKRI Future Leaders Fellowship awarded to [Professor Viktoria Spaiser](https://essl.leeds.ac.uk/politics/staff/102/professor-viktoria-spaiser) (grant reference: [UKRI2043](https://gtr.ukri.org/projects?ref=UKRI2043)).
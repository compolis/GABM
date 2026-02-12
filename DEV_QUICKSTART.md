# Developer Quickstart


## Table of Contents
- [Overview](#overview)
- [Pre-requisites](#pre-requisits)
- [1. Fork and Clone](#1-fork-and-clone)
- [2. Install Dependencies](#2-install-dependencies)
- [3. Set Up LLM API Keys](#3-set-up-llm-api-keys)
- [4. Run Tests and Build Documentation](#4-run-tests-and-build-documentation)
- [Troubleshooting](#troubleshooting)
- [Additional Resources](#additional-resources)


## Overview
This guide helps developers get started with GABM quickly. Please refer to the [Developer Guide](DEV_GUIDE.md) for details of how to contribute.

In the rest of the document "you" means you as a GABM developer.

Your choice of development environment is your own, but we recommend [Visual Studio Code](https://code.visualstudio.com/).


## Pre-requisits
You need:
- A [GitHub](https://github.com/) account to contribute.
- [git](https://git-scm.com/) version 2 at or above 2.43.
- [Python](https://www.python.org/) version 3 at or above version 3.12.
- [PIP](https://pypi.org/project/pip/) at or above version 25.2.
- [GNU Make](https://www.gnu.org/software/make/) version 4 at or above version 4.3.

To check your Python version run:

```bash
python3 --version
```

To check your PIP version run:

```bash
pip --version
```

To check you GNU Make version run:

```bash
make --version
```

You may have multiple versions of Python and GNU Make on your system. Please use the right [Path](https://en.wikipedia.org/wiki/Path_(computing)) to the versions needed for GABM when developing GABM. You might want to do this by modifying your [PATH](https://en.wikipedia.org/wiki/PATH_(variable)).


With the pre-requisites in place, the following steps should have you set up in a matter of minutes.


## 1. Fork and Clone
- Fork from the [GABM Repository](https://github.com/compolis/GABM) to your own GitHub account using the "Fork" button to "Create a new fork".
- Clone your fork locally using the following command and by replacing "<your-GitHub-username>" with your actual GitHub username:

```bash
git clone https://github.com/<your-GitHub-username>/GABM.git
```

## 2. Install Dependencies
Change into the GABM directory. From the project root, install all runtime, development, and documentation dependencies:

```bash
pip install -r requirements-dev.txt
```


## 3. Set Up LLM API Keys
Create `data/api_key.csv` with your API keys for LLM providers. See [API_KEYS.md](API_KEYS.md) for format and details.

To initialize your environment, test your API keys, and generate model lists and caches for all supported LLMs, run:

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

**Note:** For each LLM service directories are created in `data/llm`, for example `data/llm/openai`. Model list files (`models.json`, `models.txt`) are lists of available models for the LLM service. Cache files (`cache.pkl`) are prompt/response data from each LLM service.


## 4. Run Tests and Build Documentation

- Run tests:

```bash
make test
```

- Build documentation:

```bash
make docs
```

- View docs in your browser: open `docs/_build/html/index.html`



## Troubleshooting
If you encounter errors, double-check your setup steps above. If you want help, [open an issue on GitHub](https://github.com/compolis/GABM/issues/new/choose).


## Additional Resources
- [README](README.md)
- [Developer Guide](DEV_GUIDE.md)
- [Reported Issues](https://github.com/compolis/GABM/issues)
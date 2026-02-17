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

To keep your fork up to date with the main repository, add the upstream remote:

```bash
git remote add upstream https://github.com/compolis/GABM.git
```

## 2. Install Dependencies
Change into the GABM directory. From the project root, install all runtime, development, and documentation dependencies:

```bash
pip install -r requirements-dev.txt
```

**Important:** The `torch` package (PyTorch) is required for Apertus LLM model inference and can take several minutes to install. The download size is typically hundreds of megabytes, and the installed package may require over 1 GB of disk space. Please ensure you have sufficient storage and bandwidth before installing. For GPU support, follow the instructions at [pytorch.org](https://pytorch.org/get-started/locally/) to match your environment. Using local installs of Apertus models is optional.

**Warning about LLM model downloads:**

If you want to use a local LLM (such as Apertus), see [HUGGING_FACE.md](HUGGING_FACE.md) for full instructions, including authentication and troubleshooting. Downloading the model weights from Hugging Face can require a very large amount of disk space (10–20 GB or more per model) and a fast, stable internet connection. The download and setup of these models is **optional** for most users. If you only want to use API-based LLMs (OpenAI, GenAI, DeepSeek, etc.), you do not need to download any local models.

If you do want to use a local LLM, ensure you have at least 20 GB of free disk space and be prepared for a long download time.


## 3. Set Up LLM API Keys
Create `data/api_key.csv` with your API keys for LLM providers. For all supported providers (including PublicAI/Apertus), see [API_KEYS.md](API_KEYS.md) for format and details.

To initialize your environment, test your API keys, and generate model lists and caches for all supported LLMs, run:

```bash
make setup-llms
```

This will:
- Check for all required API keys (OpenAI, GenAI, DeepSeek, PublicAI)
- Test each key with a default prompt and model
- Populate `data/llm/` directories with:
  - `models.json` and `models.txt` files for each LLM, detailing available models
  - Response caches: `prompt_response_cache.pkl` and `prompt_response_cache.jsonl` for test prompts sent to the default model of each service
- Create log files in `data/logs/llm` and `data/logs/setup_llms.log` for diagnostics
- Report any issues, such as missing or malformed `api_key.csv`, or problems with API keys/services

If you need to clear all caches and model lists (for a fresh start or troubleshooting), use:
```bash
make clear-caches
```

**Note:** For each LLM service directories are created in `data/llm`, for example `data/llm/openai`. Model list files (`models.json`, `models.txt`) are lists of available models for the LLM service. Cache files (`prompt_response_cache.pkl`, `prompt_response_cache.json`) are prompt/response data from each LLM service.


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
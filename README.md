# GABM
Generative Agent Based Model

## Getting Started

### 1. Clone the Repository
First, fork the upstream repository on GitHub to your own account. Then, clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/gabm.git
cd gabm
```

### 2. Set Up Your Environment
Install Python 3.9+ and pip if you haven't already. Then install dependencies:

```bash
pip install -r requirements.txt
```

### 3. API Keys
You need a `data/api_key.csv` file with your API keys. This file is not included in the repository for security reasons.

- Ask the project maintainer for a template or example.
- Or, create it yourself with the following format (CSV with header):

```
api,key
openai,sk-...
deepseek,sk-...
llama,YOUR_GROQ_KEY
claude,YOUR_ANTHROPIC_KEY
genai,YOUR_GOOGLE_KEY
```

Place this file in the `data/` directory.

### 4. Running the Code
From the project root, run:

```bash
python3 run.py
```


## Contributing Workflow

**Note:** The `main` branch is protected. All changes must be made through Pull Requests, which require at least one review and approval before merging. Direct pushes to `main` are not allowed. This ensures code quality and collaborative review.

1. **Fork** the upstream repository to your own GitHub account.
2. **Clone** your fork locally.
3. **Create a new branch** for your feature or fix:
	```bash
	git checkout -b my-feature
	```
4. **Make your changes** and commit them:
	```bash
	git add .
	git commit -m "Describe your change"
	```
5. **Push** your branch to your fork:
	```bash
	git push origin my-feature
	```
6. **Open a Pull Request** from your branch to the main branch of the upstream repository on GitHub.
7. Wait for review and feedback. Update your branch as needed.


### Tips
- Keep your fork up to date with the upstream repository:
  ```bash
  git remote add upstream https://github.com/UPSTREAM_USERNAME/gabm.git
  git fetch upstream
  git merge upstream/main
  ```
- For easier authentication, set up SSH keys with GitHub:
  1. Generate an SSH key (if you don’t have one):
	  ```bash
	  ssh-keygen -t ed25519 -C "your_email@example.com"
	  ```
  2. Add your public key to GitHub (Settings > SSH and GPG keys).
  3. Change your remotes to use SSH:
	  ```bash
	  git remote set-url origin git@github.com:YOUR_USERNAME/gabm.git
	  git remote set-url upstream git@github.com:compolis/gabm.git
	  ```
  4. Test with:
	  ```bash
	  ssh -T git@github.com
	  ```


## Development Tasks with Makefile


This project uses a Makefile to simplify common development tasks. Run `make help` to see available commands. Key targets include:

```bash
make help        # List available Makefile commands
make sync        # Sync your main branch with upstream
make test        # Run all tests (requires pytest)
make docs        # Build documentation (requires Sphinx, in docs/)
make clean       # Remove build/test artifacts (docs/_build, .pyc, __pycache__)
make git-clean   # Safely delete merged local branches (except main/gh-pages) and prune deleted remote branches
```

**Note:**
- `make clean` is safe and only removes generated files and folders.
- `make git-clean` is safe for most workflows, but always double-check you have pushed any important branches before running. It will not delete unmerged or protected branches.

Make sure you have `make` installed (standard on Linux/macOS; for Windows, use WSL or install GNU Make).


## Documentation Deployment

Project documentation is built with Sphinx and deployed to GitHub Pages using the `gh-pages` branch.

The documentation includes an auto-generated API Reference and a module index (see `py-modindex.html` in the built docs) for easy navigation of the codebase. The Makefile and Sphinx are configured so that `make docs` works out of the box (no manual PYTHONPATH changes needed).

To build and deploy the docs:

```bash
make docs
make gh-pages
```

After deployment, documentation will be available at:
https://YOUR_USERNAME.github.io/gabm/

To activate GitHub Pages:
1. Go to your repository on GitHub.
2. Click Settings > Pages.
3. Set the source to the `gh-pages` branch (root).
4. Save.

**Note:** The `gh-pages` branch is for static site deployment and is updated automatically. Protect your `main` branch for code review and collaboration.

## Sphinx Documentation Organization

API reference documentation is organized to mirror the Python code structure for clarity and maintainability. Each major module has its own reStructuredText (.rst) file located in a matching directory under `docs/`.

For example:

```
docs/
  io/
    llm/
      utils.rst
      openai.rst
      anthropic.rst
      genai.rst
```

Each module .rst file contains an `automodule` directive for its corresponding Python module, e.g.:

```
.. automodule:: src.io.llm.openai
   :members:
   :undoc-members:
   :show-inheritance:
```

The main documentation index (`docs/index.rst`) uses a `toctree` to reference these module .rst files:

```
.. toctree::
   :maxdepth: 2
   :caption: API Reference

   io/llm/utils
   io/llm/openai
   io/llm/anthropic
   io/llm/genai
```

**How to add a new module to the docs:**
1. Create a new .rst file in the appropriate directory under `docs/`.
2. Add the `automodule` directive for your module.
3. Reference the new .rst file in the `toctree` in `index.rst`.
4. Run `make docs` to rebuild the documentation.

This structure keeps documentation organized and easy to extend as the codebase grows.

## LLM Model Listing, Caching, and Validation

This project supports multiple LLM providers (OpenAI, GenAI, DeepSeek, Anthropic) with a unified workflow for model management:

- **Model Listing:** Each LLM module provides a function to fetch and list available models from the provider's API. The full model list is saved as both JSON (machine-readable) and TXT (human-readable) in the corresponding `data/llm/{provider}/` directory.
- **Caching:** When a model list is fetched, it is cached locally. LLM responses are also cached for efficiency and reproducibility.
- **Validation:** When running the main script, the selected model for each LLM is checked against the cached JSON model list. If the model is not found, a warning is shown and the available models can be listed automatically.
- **Extensibility:** This workflow is consistent across all LLMs, making it easy to add new providers or update model selection logic.

### Model Selection (Explicit Required)

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

## Acknowledgements

- This project was developed with significant assistance from GitHub Copilot for code generation, refactoring, and documentation improvements.
- Developers are encouraged to use Visual Studio Code for its rich Python and GitHub Copilot integration, but you are free to use any editor or IDE you prefer. Spyder is also a good choice for Python development, especially if you prefer a scientific workflow.
# Developer Setup Guide

This guide is for contributors and developers who want to work on the GABM codebase, run tests, or build documentation.

## 1. Install Python and pip

- Install Python 3.12 or higher from [python.org](https://www.python.org/downloads/).
- Ensure `pip` is available.
- Check your version:

```bash
python3 --version
pip --version
```

## 2. Install Development Dependencies

From the project root, install all runtime, development, and documentation dependencies:

```bash
pip install -r requirements-dev.txt
```

## 3. Fork and Clone the Repository

- Fork the [upstream repository](https://github.com/compolis/GABM) to your own GitHub account.
- Clone your fork locally:

```bash
git clone https://github.com/<your-username>/GABM.git
cd GABM
git checkout main  # Or your feature branch
```

## 4. Set Up API Keys

- Create `data/api_key.csv` with your API keys for LLM providers. See [API_KEYS.md](API_KEYS.md) for format and details.

## 5. Run Tests and Build Documentation

- Run tests:

```bash
pytest
```

- Build documentation:

```bash
make docs
```

- View docs in your browser: open `docs/_build/html/index.html`

## 6. Contribution Workflow

- Follow the guidelines in [CONTRIBUTORS.md](CONTRIBUTORS.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Use feature branches and submit pull requests for review.
- Ensure all tests pass and documentation builds before submitting a PR.


## 7. Script Logging and Debugging

Several project scripts (asset management, cleaning, deployment) now use Python logging to record their actions, warnings, and errors. Logs are written to:

	data/logs/docs/

Each script has its own log file (e.g., `update_docs_assets.log`, `clean_docs_assets.log`). These logs help you:

- Debug issues with documentation builds or asset copying
- Review script actions and errors
- Adjust logging levels if needed (see script source for details)

If you encounter problems, check the relevant log file for details before seeking support.




## 8. Troubleshooting & Support

- If you encounter errors, check your Python version and that all dependencies are installed.
- For more help, see the [README](README.md).
- If you need support, you can [open an issue on GitHub](https://github.com/compolis/GABM/issues/new/choose).

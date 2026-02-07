# CHANGE_LOG

All notable changes to this project will be documented in this file.

## [0.2.0] - Unreleased
- ...

## [0.1.1] - 2026-02-07
### Changed
- Updated documentation files for clarity and completeness (README.md, USER_GUIDE.md, DEV_GUIDE.md).
- Improved guide integration and Makefile target documentation.
- Standardized Markdown formatting and removed YAML front matter from guides.

### Packaging & Build Workflow
- Added scripts/build-test.py for platform-agnostic build and test install in a fresh virtual environment.
- Updated Makefile: build-test now uses scripts/build-test.py; added pypi-release and testpypi-release targets for uploading to PyPI and TestPyPI.
- Updated DEV_GUIDE.md: documented new Makefile targets and clarified packaging workflow.
- Added twine to requirements-dev.txt for PyPI uploads.

### Logging
- All asset management, cleaning, deployment, and cache scripts now use Python logging.
- Logs are written to `data/logs/docs/` with rotating file handlers for each script.
- Logging helps with debugging, error tracking, and collaboration.

## [0.1.0] - 2026-02-06
### Added
- Initial private release.
- Road map outlines next step:
  - 0.2.0 implementation of a simple agent-based model
- LLM integration (OpenAI, Google Generative AI, DeepSeek).
- Persistent response/model caching.
- Onboarding utility and Makefile targets.
- Contributor workflow and documentation.
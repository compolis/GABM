# Change Log


## Table of Contents
- [Overview](#overview)
- [0.2.0 - Unreleased](#020---unreleased)
- [0.1.1 - 2026-02-12](#011---2026-02-12)
- [0.1.0 - 2026-02-06](#010---2026-02-06)


## Overview
Notable changes are to be documented in this file.


## [0.2.0] - Unreleased
- ...


## [0.1.1] - 2026-02-12
- Updated documentation to improve clarity and completeness
- Standardized Markdown formatting and removed YAML front matter from guides.

### Packaging & Build Workflow
- Added `scripts/build-test.py` for platform agnostic builds.
- Makefile pypi-release and testpypi-release targets added for uploading to [PyPI](https://pypi.org/) and [TestPyPI](https://test.pypi.org/).
- Updated [Developer Guide](DEV_GUIDE.md) by documenting new Makefile targets and clarifying packaging workflow.
- Added [Twine](https://pypi.org/project/twine/) to `requirements-dev.txt` for PyPI uploads.

### Logging
- All asset management, cleaning, deployment, and cache scripts now use [Python logging](https://docs.python.org/3/library/logging.html).
- Logs are written to `data/logs/docs/` with rotating file handlers for each script.
- Logging helps with debugging, error tracking, and collaboration.


## [0.1.0] - 2026-02-06
- Initial private release.
- Project Documentation initialised
  - [README](README.md)
  - [Road Map](RoadMap.md)
  - [User Guide](USER_GUIDE.md)
  - [Developer Guide](DEV_GUIDE.md)
- LLM setup tested for (OpenAI, Google Generative AI and DeepSeek).
- Persistent response/model caching implemented.
- Makefile targets.
- Contributor workflow and documentation.
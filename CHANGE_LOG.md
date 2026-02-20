# Change Log


## Table of Contents
- [Overview](#overview)
- [0.2.6 - 2026-02-20](#026---2026-02-20)
- [0.2.5 - 2026-02-19](#025---2026-02-19)
- [0.2.2 - 2026-02-18](#022---2026-02-18)
- [0.2.0 - 2026-02-17](#020---2026-02-17)
- [0.1.1 - 2026-02-11](#011---2026-02-11)
- [0.1.0 - 2026-02-06](#010---2026-02-06)


## Overview
A summary of changes are documented in this file.


## [0.2.6] - 2026-02-20
- [Public release on PyPI](https://pypi.org/project/gabm/0.2.6/)
- Major ABM improvements.


## [0.2.5] - 2026-02-19
- [Public release on PyPI](https://pypi.org/project/gabm/0.2.5/)
- Major ABM improvements.


## [0.2.2] - 2026-02-18
- [Public release on PyPI](https://pypi.org/project/gabm/0.2.2/)
- ABM running and outputs graphs showing change of opinion over time.
- Random seed set for reproducibility.
- Updated USER_GUIDE.md.
- Migrated LLM integration from deprecated `google-generativeai` to the new `google-genai` AP.
- Extended and improved the test suite to cover all LLM service classes.


## [0.2.0] - 2026-02-17
- [Public release on PyPI](https://pypi.org/project/gabm/0.2.0/)
- Implemented class architecture for LLM services.
- Added `publicai` LLM service.
- LLM models from Hugging Face that can optionally be used locally.
- New scripts to compile [PyPI specific README](README-pypi.md).


## [0.1.1] - 2026-02-11
- [Public release on PyPI](https://pypi.org/project/gabm/0.1.1/)
- Builds are platform agnostic.
- Makefile `pypi-release` and `testpypi-release` targets added for uploading to [PyPI](https://pypi.org/) and [TestPyPI](https://test.pypi.org/).
- All scripts use [Python logging](https://docs.python.org/3/library/logging.html) to write logs in `data/logs` with rotating file handlers for each script.
- [Sphinx documentation released on GitHub Pages](https://compolis.github.io/GABM/).


## [0.1.0] - 2026-02-06
- Documentation added:
  - [README](README.md)
  - [Road Map](RoadMap.md)
  - [User Guide](USER_GUIDE.md)
  - [Developer Guide](DEV_GUIDE.md)
- LLM setup tested and working.
- Persistent caching implemented.
# Change Log

A summary of changes are documented in this file.


## [Unreleased]
- Added optional `execute_two_stage_question` and immutable
  `TwoStageSurveyResult` in `gabm.abm.survey`, with injected chat, exact prompt
  preservation, and an intermediate reasoning-recording callback. Existing
  survey APIs and transport behaviour are unchanged.
- Expanded generic network regression tests for feature similarity and missing
  values, diagnostics metrics, timeout handling and size caps, and exact seeded
  component bridges.
- Reorganized authored documentation under `documentation/` with topic-specific
  subdirectories (`handovers`, `reproducibility`, `release`, `hpc`,
  `planning`, `history`, `publication`) and updated cross-links/Sphinx
  navigation to match.
- Moved Calder chat concurrency launcher to
  `scripts/hpc/calder/chat/run_chat_concurrency.sh` and added
  `scripts/hpc/calder/chat_opinion/run_chat_opinion_concurrency.sh` wrapper for
  `chat_opinion` runs.
- Expanded roadmap 0.6 scope with release-target detail for calibrated
  `chat_opinion` workflows and associated evidence expectations.

## [0.4.0] 2026-11-09
- Added generic seeded network builders, structural diagnostics, and
  connectivity repair in `gabm.abm.networks`. Declared their runtime
  dependencies and documented the API; downstream CAG wiring remains pending
  publication of a new GABM release.


## [0.3.0] - 2026-10-23
- Added layered trait state in `Person`:
  - immutable canonical `initial_trait_values` (Big Five defaults);
  - mutable `base_traits` for simulation evolution;
  - typed `TraitBeliefState` for self, other, and higher-order trait beliefs.
- Added `export_trait_state()` and `import_trait_state()` for reproducible trait-state checkpointing.
- Added `reflect_on_traits()` to update mutable base traits toward self-trait opinions.
- Extended tests for reproducible trait generation, trait immutability/mutability layers, trait belief hierarchy, reflection behavior, and state roundtrips.
- Updated `README.md` and `USER_GUIDE.md` with trait-state modeling guidance.
- Added/expanded chat example operation:
  - standardized chat command (`run-example-chat`) and metadata-rich output artifacts;
  - OpenAI request seed (`llm_seed`) handling and `system_fingerprint` capture;
  - cache bypass mode (`--no-cache`) to force live prompting.
- Added richer `chat_opinion` example with opinion trajectories and plot artifacts.
- Added ensemble workflows for `chat` and `chat_opinion` examples:
  - per-example `ensembles` source/test/output structure;
  - seed-window sweep runners with CSV/JSON/plot outputs;
  - aggregate sweep comparison utility for hosted-vs-HPC analysis.
- Added awkward-conversation controls and dissimilar-pair selection options for stress-testing interaction dynamics in `chat` and `chat_opinion`.
- Improved temporal realism APIs:
  - `Person` support for exact DOB, year-of-birth, exact age, and age ranges;
  - sub-year environment date stepping and birthday-event helpers.
- Updated application entry behavior in `__main__.py` with `auto` mode defaulting to chat when LLM credentials are configured.
- Reorganized HPC operational scripts under `scripts/hpc/` with compatibility wrapper retained at repository root for existing workflows.


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
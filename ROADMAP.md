# Roadmap


## Table of Contents
1. [Overview](#overview)
2. [1.0](#10)
3. [0.4](#04)


## Overview
This file outlines planned next steps and future goals.


## 1.0
- Criteria and features to be determined...


## 0.4
- Fix any reported bugs.
- Add and maintain platform-agnostic reproducibility comparison tooling in Python.
- Keep feature parity and extend analysis tools:
	- `scripts/analysis/chat/compare_chat_runs.py`
	- `scripts/analysis/chat/generate_concurrency_rows.py`
- Package Python comparison tools so they can run on Linux/macOS/Windows (including non-HPC environments).
- Add tests for comparison outputs (determinism summaries, metadata normalization, markdown row generation).
- Document user-facing workflows for local and HPC run comparison in the user guide.
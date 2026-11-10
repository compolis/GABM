# Roadmap


## Table of Contents
1. [Overview](#overview)
2. [1.0](#10)
3. [0.6](#06)


## Overview
This file outlines planned next steps and future goals.


## 1.0
- Criteria and features to be determined...


## 0.6
Target: strengthen and package the calibrated `chat_opinion` workflow as the primary 0.6 release outcome.

Planned scope:
- include documented drift-calibration controls for `chat_opinion` (`QUESTION_BONUS`, `POSITIVE_TOKEN_BONUS`, `NEGATIVE_TOKEN_PENALTY`, `SHARED_INTEREST_CAP`)
- include reproducibility-oriented run outputs and metadata summaries for single runs and ensemble sweeps
- include analysis helpers for comparing run outcomes and summarizing calibration experiments
- include updated user/developer guidance for local and HPC execution paths

Evidence expected before final 0.6 release decision:
- local no-cache calibration evidence for normal and awkward pairings
- at least one Calder/HPC pilot using the selected mid-profile drift settings
- documentation build and relevant targeted tests passing

Out of scope for 0.6:
- broad API redesign of the ABM core
- major transport-layer or provider-interface refactors unrelated to chat_opinion calibration/reproducibility
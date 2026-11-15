# Roadmap


## Table of Contents
1. [Overview](#overview)
2. [1.0](#10)
3. [0.6](#06)
4. [0.7 (proposed)](#07-proposed)


## Overview
This file outlines planned next steps and future goals.


## 1.0
- Criteria and features to be determined...


## 0.6
Delivered and tagged as `v0.6.0` on 2026-11-15.

Release record:
- see `CHANGE_LOG.md` (`[0.6.0]`) for shipped scope and details.

Notes:
- keep this roadmap focused on forward-looking plans (`0.7`, `1.0`).


## 0.7 (proposed)
Target: consolidate reusable opinion-dynamics functionality in GABM so work is not tied to a single downstream domain project.

Context:
- We are actively lifting generic functionality from `../Climate-Action-GABM`.
- A second concrete application is desirable, but direct co-development with external survey teams may not be immediately available.

Proposed scope:
- extract and stabilize generic survey/opinion-dynamics building blocks from CAG-derived workflows into GABM core utilities;
- define a dataset-agnostic survey input contract (schema + validation) so new survey sources can be added without core code changes;
- provide at least one non-CAG demonstration path, for example:
  - a public/open survey-derived example, or
  - a synthetic-but-realistic survey fixture that exercises the same interfaces;
- add CLI and documentation patterns for plugging in alternative survey datasets;
- add reproducibility checks for the new survey-input path (seeded runs + summary comparisons).

Evidence expected before a final 0.7 release decision:
- one end-to-end run using the generalized survey-input pathway outside the original CAG-specific dataset;
- focused tests covering schema validation, loader behavior, and opinion-output summaries for the generalized path;
- updated documentation showing how to map a new survey into GABM without editing core model logic.

Out of scope for 0.7 (unless explicitly reprioritized):
- bespoke adapters for every external survey format;
- broad redesign of core agent cognition APIs not required for survey generalization;
- hard dependencies on external collaborators for baseline 0.7 completion.
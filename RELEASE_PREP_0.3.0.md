# Release Preparation for 0.3.0

This checklist supports a release decision after hosted-vs-HPC comparison runs are complete.

Companion reproducibility protocol:

- `REPRODUCIBILITY_QWEN3_14B.md`

## 1) Evidence Collection (Hosted vs HPC)

Run small and medium sweeps for both `chat` and `chat_opinion`:

- Hosted baseline:
  - `make run-example-chat-ensemble ...`
  - `make run-example-chat-opinion-ensemble ...`
- HPC/local baseline:
  - same seed windows and rounds as hosted

Compare sweep outputs:

- `make compare-ensemble-sweeps SWEEP_A=... SWEEP_B=... LABEL_A=hosted LABEL_B=hpc RUN_ID=...`

Collect Qwen3-14B reproducibility evidence:

- run E1 to E4 experiments from `REPRODUCIBILITY_QWEN3_14B.md`
- archive transcript exact-match summaries from `scripts/analysis/compare_chat_runs.py`
- archive concurrency summaries (`FAILED_RUNS`, completion rates)

Archive for release notes:

- comparison report JSON/TXT
- sweep metadata JSON files
- key CSV summaries from both sides

## 2) Release Readiness Gates

- Tests:
  - `make test`
  - targeted ensemble + compare tests
- Documentation:
  - `make docs`
  - confirm links for HPC scripts and new ensemble workflows
- LLM drift checks (network-connected environment):
  - `make llm-drift-check`

## 3) Packaging and Publish

- Confirm versions are aligned (`pyproject.toml`, `setup.cfg`).
- Build and install test:
  - `make build-test`
- Optional TestPyPI validation:
  - `make testpypi-release`
- Publish:
  - `make pypi-release`

## 4) Changelog and Announcement Inputs

Ensure `CHANGE_LOG.md` entry for `0.3.0` includes:

- ensemble workflow additions
- awkward/dissimilarity controls
- reproducibility metadata controls
- temporal precision enhancements
- HPC script location change

## 5) Next Development Phase: ClimateAction-GABM (CAG)

Goal: adapt CAG to the new GABM patterns with minimal regression risk.

Recommended sequence:

1. Baseline CAG against current GABM release branch.
2. Port CAG run scripts into `scripts/hpc/` conventions where reusable.
3. Replace legacy chat invocation paths with `run-example-chat` and ensemble workflow where appropriate.
4. Adopt new run metadata/compare outputs for CAG experiments.
5. Add/port tests in CAG for deterministic seed windows and comparison artifacts.
6. Validate hosted-vs-HPC behavior using matched sweep settings.

## 6) Suggested Immediate Actions

1. Run one awkward + one normal hosted pilot for `chat_opinion`.
2. Re-run the same pilots on HPC using the same seed windows.
3. Compare with `compare-ensemble-sweeps` and decide release-go/no-go.
4. Open a CAG adaptation issue list grouped by: scripts, run commands, metadata, tests.

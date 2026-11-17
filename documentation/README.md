# Documentation Directory

This directory stores long-form project documentation that should not be tied
to Sphinx build mechanics.

Use this directory for:

- maintained operational notes
- dated handover snapshots
- research/process records
- other narrative documentation that evolves over time

Sphinx build inputs remain under [docs/](../docs/). Root-level docs remain
available during migration for compatibility and discoverability.

## Structure

- [handovers/](./handovers/): dated handover notes
- [reproducibility/](./reproducibility/): reproducibility protocols and experiment logs
- [release/](./release/): release checklists and evidence gates
- [guides/hpc/](./guides/hpc/): HPC operational guides and notes
- [guides/experiments/](./guides/experiments/): advanced experiment/ensemble operation guides
- [planning/](./planning/): roadmap and forward planning documents
- [history/](./history/): project development history
- [publication/](./publication/): publication planning/support documents (for example JOSS planning notes)

## Handover retention guidance

Handover notes are optional operational snapshots, not long-term canonical
documentation.

To keep this repository streamlined for new collaborators:

- Keep at most the **current handover** plus **one previous handover** for short
  transition history.
- Move durable guidance into canonical docs instead:
  - planning decisions: [planning/ROADMAP.md](./planning/ROADMAP.md)
  - reproducibility protocol/evidence:
    [reproducibility/REPRODUCIBILITY_QWEN3_14B.md](./reproducibility/REPRODUCIBILITY_QWEN3_14B.md)
  - release criteria: [release/RELEASE_PREP.md](./release/RELEASE_PREP.md)
  - HPC operational guidance:
    [guides/hpc/Running_On_HPC_Systems.md](./guides/hpc/Running_On_HPC_Systems.md)
- Review `handovers/` at each release cut; archive or remove superseded notes
  once key actions have been migrated into the canonical docs above.

## Current key documents

- [reproducibility/REPRODUCIBILITY_QWEN3_14B.md](./reproducibility/REPRODUCIBILITY_QWEN3_14B.md)
- [release/RELEASE_PREP.md](./release/RELEASE_PREP.md)
- [guides/hpc/Running_On_HPC_Systems.md](./guides/hpc/Running_On_HPC_Systems.md)
- [guides/experiments/Running_Chat_Ensembles.md](./guides/experiments/Running_Chat_Ensembles.md)
- [planning/ROADMAP.md](./planning/ROADMAP.md)
- [history/DEVELOPMENT_HISTORY.md](./history/DEVELOPMENT_HISTORY.md)
- [publication/JOSS_SUBMISSION.md](./publication/JOSS_SUBMISSION.md)

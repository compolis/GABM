# Development History


## Table of Contents
- [Overview](#overview)
- [GitHub Copilot](#github-copilot)
- [Contributors](#contributors)
- [Development Timeline](#development-timeline)


## Overview
This document summarises the development of GABM, including key decisions, milestones, and collaborative experiences. A summary of changes is provided in the [Change Log](CHANGE_LOG.md).


## GitHub Copilot
[GitHub Copilot](https://github.com/features/copilot) has been used to help automate release and cleanup tasks, develop document, test and formulate code.


## Contributors
See [CONTRIBUTORS].


## Development Timeline
- [2026-02-18] [GABM version 0.2.2 Released on PyPI](https://pypi.org/project/gabm/0.2.2)
- [2026-02-17] [GABM version 0.2.1 Released on PyPI](https://pypi.org/project/gabm/0.2.1)
- [2026-02-17] [GABM version 0.2.0 Released on PyPI](https://pypi.org/project/gabm/0.2.0)
- [2026-02-16] GABM Project meeting
  - Viktoria, Ajay, Andy
  - Plan to release GABM 0.2 and Climate-Action-GABM 0.1
- [2026-02-13] GABM Meeting
  - Ajay and Andy
  - Focused on Climate-Action GABM documentation and set up
- [2026-02-14] [GABM version 0.1.4 Released on PyPI](https://pypi.org/project/gabm/0.1.4)
- [2026-02-11] [GABM version 0.1.3 Released on PyPI](https://pypi.org/project/gabm/0.1.3)
- [2026-02-11] [GABM version 0.1.2 Released on PyPI](https://pypi.org/project/gabm/0.1.2)
- [2026-02-11] [GABM version 0.1.1 Released on PyPI](https://pypi.org/project/gabm/0.1.1)
- [2026-02-09] GABM Meeting
  - Ajay and Andy
  - GABM Repository visibility changed from Private to Public
  - Branch protection explained
  - Climate-Action-GABM Repository code explanation and review
- [2026-02-06] GABM Onboarding Session
  - Ajay and Andy
  - [Submitted first issue](https://github.com/compolis/GABM/issues/33)
  - Andy presented the environment setup, workflow automation, and project structure.
  - Ajay added his details to [CONTRIBUTORS](CONTRIBUTORS), and quickly learned the command line commit-push process and about creating GitHub Pull Requests to merge changes from a feature branch to the upstream repository main branch.
  - Makefile targets for syncing and clearing up branches were introduced and Ajay practised using these.
- [2026-02-03] GABM Repository created in [compolis](https://github.com/compolis/)
  - The idea is to develop GABM in part by abstracting general things from the Climate-Action-GABM Repository. Specific parts to do with Climate Action will remain in the Climate-Action-GABM Repository.
- [2026-02-02] GABM Project meeting
  - Viktoria, Ajay, Andy
  - Climate-Action-GABM Repository transered to [compolis](https://github.com/compolis/)
- [2026-01-25] Name of GitHub organisation agreed, [compolis](https://github.com/compolis/) was set up in the [University of Leeds GitHub Enterprise](https://github.com/enterprises/the-university-of-leeds) and ownership transferred to Andy. Viktoria was also added as an owner and Ajay was added as a member.
- [2026-01-21] GABM Project Meeting
  - Viktoria, Ajay, Andy
  - Key decision reached to get an organisation set up in the [University of Leeds GitHub Enterprise](https://github.com/enterprises/the-university-of-leeds) for the project.
  - Ajay agreed to transfer ownership of an existing GitHub repository into the new organisation.
  - Retrieval Augmented Generation (RAG)
    - https://www.promptingguide.ai/techniques/rag
    - RAG takes an input and retrieves a set of relevant/supporting documents which are then also fed into the text generator which produces output. This makes RAG adaptive for situations where facts could evolve over time. RAG allows language models to bypass retraining, but allows new information to be input when deriving outputs via retrieval-based generation
- [2025-10-16] GABM Kick-off Meeting
  - Viktoria, Ajay, Andy
  - Team decided to develop GABM primarily in Python
# Development History

## Table of Contents
- [Overview](#overview)
- [GitHub Copilot](#github-copilot)
- [Contributors](#contributors)
- [Development Timeline](#development-timeline)


## Overview
This document summarises the development of GABM, including key decisions, milestones, and collaborative experiences. A summary of changes is provided in the [Change Log](CHANGE_LOG.md).


### GitHub Copilot
GABM development has paired human expertise with assistance from [GitHub Copilot](https://github.com/features/copilot). This helped rapidly develop the software.

GitHub Copilot helped automate release and cleanup tasks and document not just technical steps, but also the reasoning and learning process.

Capturing information about interactions between other developers and GitHub Copilot was attempted, but has proven difficult to sustain.

GitHub Copilot has only limited session memory and no memory between sessions. Project documentation can help provide context to GitHub Copilot to tailor responses to better reflect how GABM is organised.


## Contributors
- Ajaykumar Manivannan (Ajay)
- Viktoria Spaiser (Viktoria)
- Andy Turner (Andy)
- Charlie Pilgrim (Charlie)

## Development Timeline
- [2026-02-16] GABM Project meeting
  - Viktoria, Ajay, Andy
  - ...
- [2026-02-13] GABM Meeting
  - Ajay and Andy
  - ...
- [2026-02-09] GABM Meeting
  - Ajay and Andy
  - GABM Repository visibility changed from Private to Public
  - Branch protection explained
  - Climate-Action-GABM Repository code explanation and review 
- [2026-02-06] GABM Onboarding Session
  - Ajay and Andy
  - Ajay had prepared by following steps in the README and Developer Guide, but there was [an issue which submitted together](https://github.com/compolis/GABM/issues/33)
  - Andy presented the environment setup, workflow automation, and project structure.
  - Ajay added his details to [CONTRIBUTORS](CONTRIBUTORS), and he quickly learned the command line commit-push process and about creating GitHub Pull Requests to merge changes from a feature branch to the upstream repository main branch.
  - Makefile targets for syncing and clearing up branches were introduced and Ajay practised using these and began realising/appreciating the way the workflow were set up.
- [2026-02-03] GABM Repository created in [compolis](https://github.com/compolis/)
  - The idea is to develop GABM in part by abstracting general things from the Climate-Action-GABM Repository the specific parts to do with Climate Action will remain in the Climate-Action-GABM Repository.
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
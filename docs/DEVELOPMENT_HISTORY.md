# Development History and Project Journal

This document provides a chronological summary and reflective narrative of the development of this project, including key decisions, milestones, and collaborative experiences. Detailed session logs are stored in data/logs/dev_sessions/ and referenced here for transparency and archival purposes.

## Overview
 Project inception and goals
 Major milestones (automation, CI/CD, packaging, documentation, etc.)
 Collaborative development with GitHub Copilot (AI assistant)
 Lessons learned and future directions

## People
- Sorrel Harriet (Sorrel)
- Ajaykumar Manivannan (Ajay)
- Viktoria Spaiser (Viktoria)
- Patricia Ternes (Patricia)
- Andy Turner (Andy)
- Charlie Pilgrim (Charlie)

## Session Summaries
- Upcoming:
    - [2026-02-16] GABM Project meeting
        - Sorrel, Viktoria, Ajay, Andy
        - The goal is to further define what "success" looks like from a service perspective, reflect on the intesive work and progress over a 2 week period, and reach agreement on opening the repository. This will pave the way for releasing the project and submitting a draft article to JOSS. Preparation will continue in the meantime. Details of the JOSS submission are being captured in [JOSS_SUBMISSION.md](JOSS_SUBMISSION.md)
    - [2026-02-09] Onboarding Session 2 Ajay and Andy
        - ... 
- [2026-02-06] Onboarding Session 1 Ajay and Andy
	- Ajay had prepared by trying to step through the onboarding workflow but had a problem with running one of the workflows. We investigate this to try to workaround it and submitted [this issue on GitHub](https://github.com/compolis/GABM/issues/33), but our key focus was to learn the set up and practise key development workflows.
    - Andy presented the environment setup, workflow automation, and project structure. - Ajay's details were added to [CONTRIBUTORS](CONTRIBUTORS), and he quickly learned the command line commit-push process and about creating GitHub Pull Requests to merge changes upstream. Makefile targets for syncing and clearing up branches were introduced and Ajay practised using these and began realising/appreciating the workflow and set up being advocated.
    - This session marked an important step in building the contributor community and knowledge transfer for the project.
- [2026-02-02] GABM Project meeting
    - Viktoria, Sorrel, Ajay, Andy
    - Sorrel, a colleague in my team, has recently taken on the role of RSE Consultancy Lead for the Research Computing team Sorrel and I are part of. Sorrel is overseeing this project. Sorrel prompted the meeting to help define what "success" means for the project and to establish boundaries between our service team (supporting researchers at the University of Leeds) and the research team. Our Research Computing consutlancy service offers various types of support, with projects being a key offering. Projects involve budget transfer to resource activities. In research often it is hard to know what is feasible and things change, so it is often not a good idea to be too prescriptive and stick to a specification. Generally, we aim to be agile without getting bogged down with particular Agile methods and tools.
    - With the compolis organisation now set up in the University of Leeds GitHub Enterprise, the existing repository was transferred.
- [2026-01-25] Name of organisation agreed, [compolis](https://github.com/compolis/) set up in the [University of Leeds GitHub Enterprise](https://github.com/enterprises/the-university-of-leeds) and ownership transferred to Andy.
- [2026-01-22] From Overload to Clarity Workshop
    - Sorrel organised this and it shaped the direction of this work. A reflection on the workshop is being written up as a blog post for our organisation’s website and the intention is to link to it from here in due course.
- [2026-01-21] GABM Project Meeting
    - Key decision reached to get an organisation set up in the University of Leeds GitHub Enterprise for the project.
    - Ajay also agreed to transfer ownership of an existing GitHub repository into the new organisation for safe keeping and so that Andy could study this.
    - Retrieval Augmented Generation (RAG)
        - https://www.promptingguide.ai/techniques/rag
        - RAG takes an input and retrieves a set of relevant/supporting documents which are then also fed into the text generator which produces output. This makes RAG adaptive for situations where facts could evolve over time. RAG allows language models to bypass retraining, but allows new information to be input when deriving outputs via retrieval-based generation
- [2025-10-16] GABM Kick-off Meeting
    - Viktoria, Ajay, Patricia, Andy
    
...


## Reflective Narrative
(Add your thoughts, challenges, and insights here)

## Session Logs
Detailed logs of development sessions are stored in [data/logs/dev_sessions/](data/logs/dev_sessions/). Large logs may be managed with GitHub LFS and linked here as needed.

### Log Compression & Indexing
To keep logs organized and accessible, use the script:

```bash
python scripts/compress_dev_logs.py
```

This will compress all plain text/markdown logs in `data/logs/dev_sessions/` and generate an index file ([data/logs/dev_sessions/index.md](data/logs/dev_sessions/index.md)) with links to each compressed log. Reference this index for easy navigation and citation in the project history or JOSS write-up.

# Development History and Project Journal

This document provides a chronological summary and reflective narrative of the development of this project, including key decisions, milestones, and collaborative experiences. Detailed session logs are stored in data/logs/dev_sessions/ and referenced here for transparency and archival purposes.

## Overview
 Project inception and goals
 Major milestones (automation, CI/CD, packaging, documentation, etc.)
 Collaborative development with GitHub Copilot (AI assistant)
 Lessons learned and future directions

### Early Development Decisions
### Experience with VS Code and GitHub Copilot
### Reflection, Introspection, and Responsible Research
### Software Licensing and Collaboration
### Private Development and Timing of Release
### PyPI Release, Copilot Assistance, and Reflections on Permanence
### Reflections on Human-AI Collaboration and Documentation
This project demonstrates the value of pairing human expertise with AI assistance for rapid, reliable software development. The ability to quickly adapt best practices from other ecosystems (like Maven Central) to Python, and to automate release and cleanup tasks, highlights how AI copilots can bridge knowledge gaps and accelerate open science. Documenting not just technical steps, but also the reasoning and learning process, makes the project more reproducible and accessible for future contributors.

### Sphinx Documentation and Documentation Practices
### DRY Approach and Dependency Management
### Automated Documentation Folding: Makefiles and Sphinx
### Platform-Agnostic Automation with Python Scripts
### Inclusion of Requirements and .github Files in Documentation
### Project Directory Structure and .gitignore
### Reflections on AI Pair Programming and Documentation
### Good Practice: Naming, Commenting, and Alignment
### Logs, Caches, and Data Management
The project uses both logs and caches to capture information about LLM service interactions. Caches store prompts and responses, while logs record events and diagnostics. Both can become large and are excluded from the GitHub repository. Although some Makefile targets exist for general cleanup, dedicated tidy-up scripts for logs and caches are planned for version 0.2.0 (see ROADMAP). These tools will help users and developers manage storage and maintain a clean environment. Documentation will be updated as these features are implemented.
The project emphasizes clear, simple naming of files and scripts to improve maintainability and discoverability. Script files have been renamed to reflect standard norms and to align each script with its corresponding Makefile target. The Makefile itself contains descriptive comments, and each script in the scripts directory is well commented to clarify its purpose and usage. Similarly, Python source code files in the src directory are thoroughly commented and documented. These practices support collaboration, ease onboarding for new contributors, and help ensure the project remains understandable and maintainable as it evolves.
The addition of CODE_OF_CONDUCT.md exemplifies the benefits of AI pair programming. When Andy suggested including a code of conduct, the AI assistant quickly drafted, integrated, and ensured its inclusion in the Sphinx documentation. This accelerated workflow relieved Andy of a task and sped up project progress. However, it remains important to review all changes, as AI assistants have limited session memory and may occasionally miss details. Comprehensive documentation bridges this gap, enabling Andy to teach and guide the AI assistant as needed. This collaborative process shows how AI can normalize and accelerate good practice, while documentation ensures continuity and reproducibility for both human and AI contributors.
The overall structure of the project directories is explained in the DEV_GUIDE and README, but it is important to highlight hidden directories such as .github (for workflows, security, and contact files) and .git (for version control metadata). The .gitignore file specifies which files and directories should be excluded from version control, helping to keep the repository clean and secure. For this project, .gitignore excludes build artifacts, caches, large log files, and other files not needed for collaboration or distribution. This ensures that only essential code, documentation, and metadata are tracked, supporting reproducibility and maintainability.
The Python docs.py script in the scripts folder also copies requirements text files (requirements.txt and requirements-dev.txt) and files from the .github directory (such as SECURITY.md and CONTACT.md) into the Sphinx docs directory. This ensures that important project metadata, security information, and contact details are included in the published documentation, further supporting transparency and reproducibility.
To further enhance platform agnosticism, Python scripts are used alongside Makefiles to automate documentation workflows. One script automates the generation of Sphinx documentation by copying Markdown files from the root directory, modifying them for formatting, and temporarily adding them to the docs folder for Sphinx compilation. Following DRY principles, the main Sphinx index.html page is based on README.md, which is included via index.md in the docs directory. This approach ensures that core project information is maintained in a single place and consistently presented across both the repository and the documentation site.
Project documentation serves both the GitHub repository and the Sphinx documentation site. Automation is achieved using Makefile targets, which copy and fold Markdown files from the repository root into the Sphinx docs directory. This ensures consistency and reduces manual effort. Makefiles (and the make tool) provide a platform-agnostic way to define build, test, and documentation workflows, while Sphinx enables rich, navigable documentation generation from Markdown and reStructuredText sources. The combination of Makefiles and Sphinx streamlines the process of maintaining and publishing up-to-date documentation for users and developers.
The project aims to follow a Don't Repeat Yourself (DRY) approach in both code and documentation, improving maintainability and simplifying updates. Recent work has focused on developing distinct documentation for users and developers, including setup guides and in-depth references. API key requirements for LLMs were abstracted into a dedicated Markdown file for clarity. To support reproducibility, requirements.txt and requirements-dev.txt were used to specify dependencies: user requirements are pinned for consistency, while developer requirements allow more flexibility. Reflecting further on dependencies and reproducibility is important and will be addressed in a dedicated section.
Much of the work prior to organizing for PyPI deployment focused on getting the documentation for GABM organized. Updating documentation is an ongoing task as the project evolves, and several types of documentation are important:
- **Sphinx Documentation**: Used for generating user and developer guides, API references, and project history from Markdown and reStructuredText files. Sphinx, combined with MyST, enables rich, navigable documentation that is easy to maintain and publish.
- **Source Code Comments**: Inline comments and docstrings in the codebase provide immediate context for developers, aiding understanding and future maintenance.
- **Other File Comments**: Comments in configuration files, scripts, and data files help clarify intent and usage for both users and contributors.

The process of developing and maintaining documentation is iterative and collaborative, requiring regular review and updates as the project and its audience grow.
The most recent development changes focused on enabling GABM to be released on PyPI. GitHub Copilot greatly simplified this process by explaining the required steps and files to Andy, who was already experienced with Java/Maven releases to Maven Central. On Friday, a new Makefile target was also created to delete tagged releases on GitHub. While deleting a release on PyPI is possible, it is notoriously difficult on Maven Central, where releases are intended to be permanent. This permanence allows others to reliably depend on published artifacts, reducing the need for developers to distribute dependencies themselves. Such central repositories and caching mechanisms help optimize network usage and storage, benefiting the broader software ecosystem.
Viktoria and Ajay prefer to develop the project in private for now, with plans to open the repository in due course. Although an open source license has been applied, the repository is not yet public. For JOSS publication, the software must be released openly. The decision about when to open the repository rests with Viktoria and Ajay, but some workflows are currently hampered by the private status and cannot be fully tested. This highlights the balance between collaborative readiness and the requirements of open science publication.
A key aspect of responsible research software development is the application of an appropriate software license. A software license is a legal document that defines what users can do with the software, including redistribution and building upon it, and protects developers by limiting their liabilities. For GABM, the team chose the 3-clause BSD license, which is permissive and widely used in open science. This license allows broad use and redistribution, while protecting contributors from liability. While it is possible to change the license in the future, doing so becomes more complex as the project grows and more collaborators from different organizations contribute. The choice of license reflects a balance between openness, collaboration, and legal protection for all contributors.
Andy’s experience in UK e-Science training (2005–2011) emphasized the importance of reflection, introspection, and open protocols for accelerating and catalyzing research. While working in the social science domain as part of the UK National Centre for e-Social Science, Andy and colleagues explored how sharing tools, knowledge, and computational resources could achieve more together. Social science collaborators at the Oxford Internet Institute were particularly interested in how open processes change the research process itself, encouraging the community to lay bare their discoveries and development workflows for study and improvement.

This ethos of openness is balanced by the need for refinement and focus. In scientific research, the goal is not to mystify but to explain and make reproducible the process and results. Automation, reproducibility, and catalyzing positive change are essential for research and, arguably, for the survival of civilization. Andy notes that while people are both in awe of and fearful of AI, it is crucial to proceed with caution and reflect on the broader impacts of new technologies. Responsible application, checks and balances, and awareness of how technology can be used or misused—especially in political and social contexts—are vital. The influence of technology and media on elections and public opinion underscores the need for ethical reflection and responsible innovation.
In the two consultancy projects prior to GABM, Andy used Visual Studio Code and GitHub Copilot to accelerate development. The suggestion to use these tools came from Research Software Engineer Nick Rhodes, a member of Sorrel and Andy's team. Both earlier projects, MXG and RiboCode, were TypeScript-based:

- **MXG**: Developed a web-based UI for creating and processing XML input/output files for MESMER software. The project history is available at https://github.com/MESMER-kinetics/mxg, and the latest version is deployed at https://mesmer-kinetics.github.io/mxg/.
- **RiboCode**: An ongoing project orchestrating a UI based on two styled [Mol*](https://github.com/molstar/molstar) viewers for comparing ribosome datasets in 3D. Repository: https://github.com/ribocode-slola/ribocode1/. Like MXG, RiboCode is deployed as a [Progressive Web App (PWA)](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps) via GitHub Pages.

These experiences provided valuable background in using VS Code with Copilot and modern web technologies. Andy brought this expertise, along with broader IDE experience, to the GABM project. The use of AI pair programming is now seen as essential for productivity, much as IDEs became standard a decade ago. AI copilots enable developers to shortcut learning and implementation, harnessing machine reading and writing capabilities far beyond human limits.
The initial development of this repository began by reviewing preliminary work by Ajay and Charlie, who had explored communicating with LLMs using Python. In the project kick-off meeting with Viktoria and Ajay, the team decided to develop GABM primarily in Python. This decision was influenced by Ajay's familiarity with Python and the availability of Python libraries for LLM communication. At the time, none of the team were aware of any existing Agent Based Model (ABM) frameworks in Python suitable for their needs, but developing an ABM in Python was considered straightforward. Andy had prior experience teaching ABM concepts in Python and had developed learning resources for Geographers, which are available online: https://agdturner.github.io/Python0/public_html/home/index.html.

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

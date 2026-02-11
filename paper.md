---
title: "GABM: Generative Agent-Based Model Platform"
authors:
  - name: GitHub Copilot
    affiliation: 1
  - name: Sorrel Harriet
    affiliation: 2
  - name: Ajaykumar Manivannan
    affiliation: 2
  - name: Charlie Pilgrim
    affiliation: 2
  - name: Viktoria Spaiser
    affiliation: 2
  - name: Andy Turner
    affiliation: 2
affiliations:
  - name: AI Assistant
    index: 1
  - name: University of Leeds
    index: 2
---

# Introduction
GABM is a Python platform for agent-based modeling with integrated LLM support. This paper describes the platforming, onboarding, and open science practices.

The development of GABM began with Andy reviewing preliminary work by Ajay and Charlie, who had experimented with Python scripts to communicate with Large Language Model (LLM) services. Ajay had developed code to process some survey data into personas which could be provide with other context to LLM models to prompt responses tht reflect the repsonse of a persona as provided by the LLM model. The personas were derived from a YouGov survey and the context and responses for the use case are based on climate change mitigation.

Python libraries for using LLM Application Programming Interfaces(APIs) have been maturing for years. Developing an Agent Based Model (ABM) in Python is quite straightforward and something the development team had considerable experience with. It was decided to start the development with a requirement of Python >=3.12 as this wideley being used and would remain in maintenance for the project duration.


## Software Licensing
GABM is released under the 3-clause BSD license, which clearly defines user rights, redistribution, and liability limitations. This permissive license encourages broad adoption and collaboration while protecting developers.

## Documentation
Significant effort has gone into organizing and producing documentation for GABM. GABM documentation is designed for both the [GitHub repository](https://github.com/compolis/GABM) and the [Sphinx documentation site served via GitHub Pages from the repository](https://compolis.github.io/GABM).

Automation of [Sphinx](https://www.sphinx-doc.org/) documentation uses [GNU make](https://www.gnu.org/software/make/) and specific Makefile targets, which copy and preprocess Markdown files from the repository root into the `docs` directory ready to build the documentation. Sphinx, together with [MyST](https://mystmd.org/), generates rich, navigable documentation from Markdown and reStructuredText sources. This approach ensures consistency, reduces manual effort, and keeps user and developer documentation up to date.

GABM uses Python scripts alongside Makefiles to automate documentation workflows. For example, a dedicated script copies Markdown files from the root directory, modifies them for formatting, and temporarily adds them to the docs folder for Sphinx compilation. The main Sphinx index.html page is based on README.md, included via index.md in the docs directory, following DRY principles. This ensures that core project information is maintained in a single location and consistently presented across both the repository and the documentation site.

Python source code comment Docstrings and inline comments provide essential context for developers and maintainers.

Comments in scripts, configuration, and data files clarify intent and usage.

Maintaining high-quality documentation is an ongoing, collaborative effort that evolves with the project and its community.


## Naming, Commenting, and Alignment
GABM follows good practice by using clear, simple naming for files and scripts, making the project easier to maintain and navigate. Scripts are named to match their corresponding Makefile targets, and the Makefile includes descriptive comments. All scripts and Python source code files are well commented and documented, supporting collaboration and onboarding. These conventions help ensure the project remains accessible and maintainable for both current and future contributors.


## DRY Approach
A Don't Repeat Yourself (DRY) philosophy is adopted for both code and documentation, enhancing maintainability and ease of change. There are separate guides for users and developers.


## Build Requirements and Dependency Management
GABM is currently based on Python >=3.12. There are different dependency requirements for users and developers.

For reproducibile builds, requirements.txt and requirements-dev.txt clearly specify dependencies: user requirements are pinned, while developer dependencies are more flexible.


## Reflections on AI Pair Programming
Human expertise with AI assistance helped to rapidly develop GABM. GitHub Copilot was used to speed up development, improve documention, and adopt good practices.

The addition of CODE_OF_CONDUCT.md is an example of the benefits of AI pair programming. After suggesting the project should have a code of conduct, the AI assistant quickly drafted the file, integrated it into the repository, updated the docs.py script, and ensured its inclusion in the Sphinx documentation.

There is a need to check carefully what AI assistance is doing. Delegating workflow changes, code changes and execution tasks to an AI pair programmer should be done carefully. Multiple times during development there were major issues with suggested patches to code and asking for multiple changes makes it hard to check and be sure that what is being done is not unravelling good work that you want to keep. Obviously things can be unpicked adn undone especially if small changes are committed with sensible commit messages, but it can be easy to get lost and go around in circles.

To try to avoid problems and losing work, human developers should check carefully what an AI pair programmer is doing and suggesting rather than blindly accepting it is doing the right thing.

Having a lots of tests that can be automatically run, and improving and extending test coverage (documentation) as workflows are put in place and modified and as code is developed is well worth the efffort and provides a way to help check. Producing clear consise documentation that an AI pair programmer reads for context at the start of AI Pair programming development sessions is a good idea. The current generation of AI Pair programming tools learn what to do, but then forget and their memory between sessions is otherwise poor, so it is up to the developer using these tools to try to provide this. On reflection, it was a good idea to provide concise and clear context to help the AI pair programmer be more useful.


## PyPI Release and Reflections on Permanence
GABM is both available via the GitHub repository and is also released on PyPI. The process of making releases was made much easier with guidance from GitHub Copilot. A developer familiar with Java/Maven and Maven Central, found the Python release process more accessible thanks to AI Pair programmer explanations of the similarities. A Makefile target was also added to delete tagged releases on GitHub. It is understood that PyPI allows for release deletion whereas Maven Central is designed for permanence. However there is a major benefits of releasing on PyPI in that users can use Pip to install it.


## Logs, Caches, and Data Management
In addition to logging, the project implements caches to store prompts and responses for each LLM service. Both logs and caches can grow large and are not stored in the GitHub repository. Users and developers should be aware of their size and manage them appropriately. While some Makefile targets exist for general cleanup, dedicated tidy-up scripts for logs and caches are planned for version 0.2.0 (see ROADMAP). These tools will help users and developers maintain a clean working environment and manage storage efficiently.


## Developer Experience
Before starting to work on developing GABM, Andy had a foundation in using [Visual Studio Code](https://code.visualstudio.com/) with [GitHub Copilot](https://github.com/features/copilot) by leading development of other software in the last couple of years using these tools:
- **MXG**: A web-based User Interface (UI) for MESMER software XML files ([repo](https://github.com/MESMER-kinetics/mxg), [live](https://mesmer-kinetics.github.io/mxg/)).
- **RiboCode**: An tool for comparing ribosome datasets in 3D using [Mol*](https://github.com/molstar/molstar) ([repo](https://github.com/ribocode-slola/ribocode1/), [live](https://ribocode-slola.github.io/ribocode1/)).

Experience of using an Integrated Development Environment (IDE) along with an integrated AI pair programmer helps developers know about their capabilities and what they are good for. Their capabiities are probably fast improving and developers are strongly encouraged to cautiously embrace working with AI assistance for developing software.


## Relevance of Global Tipping Points

The Global Tipping Points Report (2025) [@globaltipping2025] synthesizes the latest research on both positive and negative tipping points in the Earth system, with contributions from 160 authors across 23 countries and 87 institutions. Viktoria, a co-author of part of this report, has helped consolidate knowledge on the governance, risks, and opportunities associated with climate and biosphere tipping points. The report is highly relevant to the GABM project, as our application aims to model and understand the dynamics of global tipping points and their implications for climate, ecosystems, and society. Insights from the report inform the design and intended use cases of GABM, particularly in exploring interventions to avoid harmful tipping points and trigger positive ones.


# Statement of Need
- Why could we not just use existing software?

The recent work by Vezhnevets et al. (2023) [@vezhnevets2023concordia] introduces Concordia, a library for generative agent-based modeling (GABM) that leverages large language models (LLMs) to enable agents to act, reason, and interact in simulated physical, social, or digital environments. Concordia’s architecture, which includes a Game Master agent to mediate between agent intentions and environment constraints, demonstrates the potential of LLM-driven ABMs to simulate complex, language-mediated behaviors and interactions. This work provides important context and inspiration for GABM, highlighting both the opportunities and challenges of integrating LLMs into agent-based modeling. Our platform builds on these ideas, aiming for modularity, extensibility, and transparency, and is designed to support a wide range of research and application domains.


# Functionality
- Multi-LLM support (OpenAI, DeepSeek, GenAI)
- Modular onboarding and setup
- Logging, documentation, and reproducibility


# Acknowledgements
- GABM was developed with significant assistance from [GitHub Copilot](https://github.com/features/copilot) for code generation, refactoring, and documentation improvements.
- We gratefully acknowledge support from the [University of Leeds](https://www.leeds.ac.uk/). Funding for this project comes from a UKRI Future Leaders Fellowship awarded to [Professor Viktoria Spaiser](https://essl.leeds.ac.uk/politics/staff/102/professor-viktoria-spaiser) (grant reference: [UKRI2043](https://gtr.ukri.org/projects?ref=UKRI2043)).


# AI Usage Disclosure
This project made extensive use of generative AI, specifically GitHub Copilot (GPT-4.1), for code generation, refactoring, documentation, and drafting of this paper. All AI-assisted outputs were reviewed, edited, and validated by the human authors, who made all core design decisions. GitHub Copilot is included as a co-author to reflect its substantial contribution to the development and documentation process, in line with the collaborative and transparent ethos of the project.


# References
See paper.bib for references.

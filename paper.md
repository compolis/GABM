---
title: "GABM: Generative Agent-Based Model Platform"
authors:
  - name: Ajaykumar Manivannan
    affiliation: 1
  - name: Charlie Pilgrim
    affiliation: 1
  - name: Viktoria Spaiser
    affiliation: 1
  - name: Andy Turner
    affiliation: 1
affiliations:
  - name: University of Leeds
    index: 1
---


# Introduction

GABM is a [Python](https://www.python.org/) platform for agent-based modeling with integrated LLM support.

GABM is available via [The Compolis GABM GitHub Repository](https://github.com/compolis/GABM) which is managed within the [University of Leeds GitHub Enterprise](https://github.com/enterprises/the-university-of-leeds). GABM is also released and made available via [PyPI](https://pypi.org/) as [https://pypi.org/project/gabm/](https://pypi.org/project/gabm/).

TODO: Introduce the Brussels Workshop

Before there was GABM, there were experimental Python scripts that used Large Language Model (LLM) services to send prompts and recieve responses. This work was funded as part of a Future Leaders Fellowship Grant awarded to Viktoria and the initial exploratory work was undertaken by Ajay and Charlie. The idea of GABM was to abstract the general functionality required for developing an Agent Base Model (ABM) to study climate change politics using LLMs. GABM would be for supporting use cases where a combination of ABM and LLM were wanted, specifically where agents defined in a model would use a LLMs to communicated and modify their opinions, beliefs, desires and behaviour. Climate-Action-GABM was developed to use GABM as a dependency and is specifically geared to study climate change politics (see [The Compolis Climate-Action-GABM GitHub Repository](https://github.com/compolis/Climate-Action-GABM)).


## Software Licensing

GABM is released under the 3-clause BSD license, which clearly defines user rights, redistribution, and liability limitations. This permissive license encourages broad adoption and collaboration while protecting developers.


## Documentation

Maintaining high-quality documentation is an ongoing, collaborative effort. The aim is for Python source code comment Docstrings and inline comments to provide essential context for developers and maintainers. Comments in scripts, configuration, and data files aim to clarify intent and usage.

GABM documentation is designed for the GitHub repository, the [Sphinx documentation site served via GitHub Pages from the repository](https://compolis.github.io/GABM), and a specific README is generated for the release on PyPI.

[Sphinx](https://www.sphinx-doc.org/) together with [MyST](https://mystmd.org/), generates rich, navigable documentation from Markdown and reStructuredText sources.

The Sphinx documentation and the PiPY README are automatically generated using [GNU make](https://www.gnu.org/software/make/) and specific Makefile targets as described below. The main Sphinx index.html page is based on the GitHub repository README.md. Following a Don't Repeat Yourself (DRY) philisophy helps to ensures that core project information is maintained in a single location.

There are separate guides for users and developers.


## Automation

To make development and deployment easier, [GNU make](https://www.gnu.org/software/make/) and specific Makefile targets along with Python scripts are used to automate workflows in a platform agnostic manner. [GitHub Actions](https://github.com/features/actions) are also used for checking and testing [GitHub Pull Requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests).

For example, a `docs` Makefile target calls a `docs.py` script to preprocess Markdown files from the repository root into the `docs` directory then builds the Sphinx documentation. This approach ensures consistency, reduces manual effort, and helps keep things up to date.

Makefile targets are chained as necessary to make the release process straightforward.


## Naming, Commenting, and Alignment

GABM follows good practice by using clear, simple naming for files and scripts, making the project easier to maintain and navigate. Scripts are named to match their corresponding Makefile targets, and the Makefile includes descriptive comments. All scripts and Python source code files are well commented and documented, supporting collaboration and onboarding. These conventions help ensure the project remains accessible and maintainable for both current and future contributors.


## DRY Approach
A Don't Repeat Yourself (DRY) philosophy is adopted for code as well as documentation, enhancing maintainability and ease of change.


## Build Requirements and Dependency Management

GABM is currently based on Python >=3.12. There are different dependency requirements for users and developers.

For reproducibile builds, requirements.txt and requirements-dev.txt clearly specify dependencies: user requirements are pinned, while developer dependencies are more flexible.

For users wanting to locally use LLMs and download these from [Hugging Face](https://huggingface.co/), a separate requirements-local-llm.txt is provided.


## Reflections on AI Pair Programming

GitHub Copilot was used to speed up development, improve documention, and adopt good practices.

The addition of CODE_OF_CONDUCT.md is an example of the benefits of AI pair programming. After suggesting the project should have a code of conduct, the AI assistant quickly drafted the file, integrated it into the repository, updated the docs.py script to include it in the Sphinx documentation.

There is a need to check carefully what AI assistance is doing. Delegating workflow changes, code changes and execution tasks to an AI pair programmer should be done carefully. Multiple times during development there were major issues with suggested patches to code. Human developers should check carefully what an AI pair programmer is doing and suggesting rather than blindly accepting suggestions.

Having a broad test coverage helps with identifying issues and robustness.

TODO: Producing clear consise documentation for an AI pair programmer was a useful stop gap before AGENTS.md and SKILLS.md files were developed (see https://chrisreddington.com/blog/building-your-agent-toolbox/)


## Logs, Caches, and Data Management

In addition to logging, the project implements caches to store prompts and responses for each LLM service. Both logs and caches can grow large and are not stored in the GitHub repository. Users and developers should be aware of their size and manage them appropriately.

TODO: Add Makefile targets and Python scripts to manage logs and caches.


## Developer Experience

[Visual Studio Code](https://code.visualstudio.com/) with the GitHub Copilot Pair Programmer extension provided an excellent tool for developing GABM.


# Statement of Need

TODO: Why not use existing software?

## [Concordia](https://github.com/google-deepmind/concordia)

Concordia is introduced in Vezhnevets et al. (2023) [@vezhnevets2023concordia] as a library for generative agent-based modelling that leverages LLMs to enable agents to act, reason, and interact in simulated physical, social, or digital environments. A Game Master agent mediates between agent intentions and environment constraints. Vezhnevets et al. (2023) [@vezhnevets2023concordia]  demonstrates the potential of LLM-driven ABMs to simulate complex, language-mediated behaviors and interactions.

## [Mesa-LLM](https://github.com/mesa/mesa-llm)


# GABM Functionality

LLM Services support for OpenAI, DeepSeek, GenAI and PublicAI.


# Acknowledgements

- GABM was developed with significant assistance from [GitHub Copilot](https://github.com/features/copilot) to help generate, refactor, document and test code.
- We gratefully acknowledge support from the [University of Leeds](https://www.leeds.ac.uk/). Funding for this project comes from a UKRI Future Leaders Fellowship awarded to [Professor Viktoria Spaiser](https://essl.leeds.ac.uk/politics/staff/102/professor-viktoria-spaiser) (grant reference: [UKRI2043](https://gtr.ukri.org/projects?ref=UKRI2043)).


# AI Usage Disclosure
This project used GitHub Copilot to help generate, refactor, document and test code. It was also used to draft and edit this paper.


# References
See paper.bib for references.

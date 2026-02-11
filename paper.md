---
title: "GABM: Generative Agent-Based Model Platform"
authors:
  - name: Andy Turner
    affiliation: 1
  - name: Ajaykumar Manivannan
    affiliation: 2
  - name: Viktoria Spaiser
    affiliation: 1
  - name: Sorrel Harriet
    affiliation: 1
  - name: GitHub Copilot
    affiliation: 3
affiliations:
  - name: University of Leeds
    index: 1
  - name: University of Leeds (Researcher)
    index: 2
  - name: AI Assistant
    index: 3
---

# What is GABM?

GABM is a Python platform for agent-based modeling with integrated LLM support. This paper describes the platforming, onboarding, and open science practices. The agent-based model and results are forthcoming.

## Software Licensing
GABM is released under the 3-clause BSD license, which clearly defines user rights, redistribution, and liability limitations. This permissive license encourages broad adoption and collaboration while protecting developers.

## Reflections on AI Pair Programming
Human expertise with AI assistance helped to rapidly develop GABM. GitHub Copilot was used to speed up development, improve documention, and adopt good practices.

## PyPI Release and Reflections on Permanence

## Documentation
Significant effort has gone into organizing and producing documentation for GABM. Documentation includes:
- **Sphinx Documentation**: For user/developer guides, API references, and project history, generated from Markdown and reStructuredText using Sphinx and MyST.
- **Source Code Comments**: Docstrings and inline comments provide essential context for developers and maintainers.
- **Other File Comments**: Comments in scripts, configuration, and data files clarify intent and usage.

Maintaining high-quality documentation is an ongoing, collaborative effort that evolves with the project and its community.

## DRY Approach and Dependency Management
## Automated Documentation Folding: Makefiles and Sphinx
## Platform-Agnostic Automation with Python Scripts
## Inclusion of Requirements and .github Files in Documentation
## Project Directory Structure and .gitignore
## Overview of Markdown Files

## Logs, Caches, and Data Management
In addition to logging, the project implements caches to store prompts and responses for each LLM service. Both logs and caches can grow large and are not stored in the GitHub repository. Users and developers should be aware of their size and manage them appropriately. While some Makefile targets exist for general cleanup, dedicated tidy-up scripts for logs and caches are planned for version 0.2.0 (see ROADMAP). These tools will help users and developers maintain a clean working environment and manage storage efficiently.

## Good Practice: Naming, Commenting, and Alignment
GABM follows good practice by using clear, simple naming for files and scripts, making the project easier to maintain and navigate. Scripts are named to match their corresponding Makefile targets, and the Makefile includes descriptive comments. All scripts and Python source code files are well commented and documented, supporting collaboration and onboarding. These conventions help ensure the project remains accessible and maintainable for both current and future contributors.

The addition of CODE_OF_CONDUCT.md is a prime example of the benefits of AI pair programming. After suggesting the project should have a code of conduct, the AI assistant quickly drafted the file, integrated it into the repository, updated the docs.py script, and ensured its inclusion in the Sphinx documentation. 

GABM uses Python scripts alongside Makefiles to automate documentation workflows. For example, a dedicated script copies Markdown files from the root directory, modifies them for formatting, and temporarily adds them to the docs folder for Sphinx compilation. The main Sphinx index.html page is based on README.md, included via index.md in the docs directory, following DRY principles. This ensures that core project information is maintained in a single location and consistently presented across both the repository and the documentation site.
GABM’s documentation is designed for both the GitHub repository and the Sphinx documentation site. Automation is handled via Makefile targets, which copy and fold Markdown files from the repository root into the Sphinx docs directory. Makefiles (using the make tool) provide a platform-agnostic way to manage build, test, and documentation workflows. Sphinx, together with MyST, generates rich, navigable documentation from Markdown and reStructuredText sources. This approach ensures consistency, reduces manual effort, and keeps user and developer documentation up to date.

A Don't Repeat Yourself (DRY) philosophy is adopted for both code and documentation, enhancing maintainability and ease of change. There are separate guides for users and developers.

For reproducibility, requirements.txt and requirements-dev.txt clearly specify dependencies: user requirements are pinned, while developer dependencies are more flexible.


The latest development work enabled GABM to be released on PyPI, a process made much easier with guidance from GitHub Copilot. Andy, familiar with Java/Maven and Maven Central, found the Python release process more accessible thanks to Copilot’s explanations. A Makefile target was also added to delete tagged releases on GitHub. While PyPI allows for release deletion, Maven Central is designed for permanence, ensuring that dependencies remain available for the long term. This reliability reduces the burden on developers and optimizes network and storage usage through centralized repositories and caching, which benefits the wider software community.





While scientific discovery values explanation over spectacle, the real value lies in making results reproducible and processes open to scrutiny. Automation and reproducibility are not just best practices—they are essential for catalyzing positive change. As AI becomes more powerful, it is vital to proceed with caution, reflect on societal impacts, and ensure technology is used for good. The potential for technology and media to influence elections and public opinion highlights the need for ethical reflection and responsible development in all research software projects.
Prior to GABM, Andy worked on two consultancy projects—MXG and RiboCode—using Visual Studio Code and GitHub Copilot to accelerate development. The adoption of these tools was suggested by Research Software Engineer Nick Rhodes, a member of Sorrel and Andy's team. Both projects were TypeScript-based:

- **MXG**: A web-based UI for MESMER software XML files ([repo](https://github.com/MESMER-kinetics/mxg), [live](https://mesmer-kinetics.github.io/mxg/)).
- **RiboCode**: An ongoing PWA for comparing ribosome datasets in 3D using [Mol*](https://github.com/molstar/molstar) ([repo](https://github.com/ribocode-slola/ribocode1/)).

These experiences gave Andy a strong foundation in using VS Code with Copilot and modern development workflows. The integration of AI pair programming is now considered as transformative as the adoption of IDEs was a decade ago, enabling rapid learning and productivity gains for developers.
## Relevance of Global Tipping Points

The Global Tipping Points Report (2025) [@globaltipping2025] synthesizes the latest research on both positive and negative tipping points in the Earth system, with contributions from 160 authors across 23 countries and 87 institutions. Viktoria, a co-author of part of this report, has helped consolidate knowledge on the governance, risks, and opportunities associated with climate and biosphere tipping points. The report is highly relevant to the GABM project, as our application aims to model and understand the dynamics of global tipping points and their implications for climate, ecosystems, and society. Insights from the report inform the design and intended use cases of GABM, particularly in exploring interventions to avoid harmful tipping points and trigger positive ones.
The development of GABM began by reviewing preliminary work by Ajay and Charlie, who had experimented with Python scripts to communicate with LLMs. In the project kick-off meeting, Viktoria and Ajay agreed with Andy to use Python as the main development language, given Ajay's experience and the strong ecosystem of Python libraries for LLM integration. Although the team was not aware of any ready-made Python ABM frameworks that fit their requirements, developing an ABM in Python was considered accessible. Andy brought experience from teaching ABM in Python and had created online resources for Geographers, which informed the early approach (see: https://agdturner.github.io/Python0/public_html/home/index.html).

## Generative Agent-Based Modeling and Concordia

The recent work by Vezhnevets et al. (2023) [@vezhnevets2023concordia] introduces Concordia, a library for generative agent-based modeling (GABM) that leverages large language models (LLMs) to enable agents to act, reason, and interact in simulated physical, social, or digital environments. Concordia’s architecture, which includes a Game Master agent to mediate between agent intentions and environment constraints, demonstrates the potential of LLM-driven ABMs to simulate complex, language-mediated behaviors and interactions. This work provides important context and inspiration for GABM, highlighting both the opportunities and challenges of integrating LLMs into agent-based modeling. Our platform builds on these ideas, aiming for modularity, extensibility, and transparency, and is designed to support a wide range of research and application domains.

# Statement of Need

(Describe the motivation and need for GABM, especially for integrating LLMs in ABM workflows.)

# Functionality

- Multi-LLM support (OpenAI, DeepSeek, GenAI)
- Modular onboarding and setup
- Logging, documentation, and reproducibility

# Acknowledgements

This project was developed with significant assistance from [GitHub Copilot](https://github.com/features/copilot) for code generation, refactoring, and documentation improvements.

We gratefully acknowledge support from the [University of Leeds](https://www.leeds.ac.uk/). Funding for this project comes from a UKRI Future Leaders Fellowship awarded to [Professor Viktoria Spaiser](https://essl.leeds.ac.uk/politics/staff/102/professor-viktoria-spaiser) (grant reference: [UKRI2043](https://gtr.ukri.org/projects?ref=UKRI2043)).

# AI Usage Disclosure

This project made extensive use of generative AI, specifically GitHub Copilot (GPT-4.1), for code generation, refactoring, documentation, and drafting of this paper. All AI-assisted outputs were reviewed, edited, and validated by the human authors, who made all core design decisions. GitHub Copilot is included as a co-author to reflect its substantial contribution to the development and documentation process, in line with the collaborative and transparent ethos of the project.

# References

See paper.bib for references.

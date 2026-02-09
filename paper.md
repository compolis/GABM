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

# Summary

GABM is a Python platform for agent-based modeling with integrated LLM support. This paper describes the platforming, onboarding, and open science practices. The agent-based model and results are forthcoming.

## Development Story
## Reflection and Responsible Innovation
## Software Licensing
## Private Development and Release Timing
## PyPI Release and Reflections on Permanence
## Reflections on Human-AI Collaboration and Documentation
This project illustrates the benefits of combining human expertise with AI assistance for efficient, reliable software development. GitHub Copilot enabled rapid knowledge transfer and adaptation of best practices, while the collaborative workflow ensured that both technical steps and the reasoning behind them were well documented. This approach enhances reproducibility and lowers barriers for future contributors.

## Sphinx Documentation and Documentation Practices
## DRY Approach and Dependency Management
## Automated Documentation Folding: Makefiles and Sphinx
## Platform-Agnostic Automation with Python Scripts
## Inclusion of Requirements and .github Files in Documentation
## Project Directory Structure and .gitignore
## Overview of Markdown Files
## Reflections on AI Pair Programming and Documentation
## Good Practice: Naming, Commenting, and Alignment
## Logs, Caches, and Data Management
In addition to logging, the project implements caches to store prompts and responses for each LLM service. Both logs and caches can grow large and are not stored in the GitHub repository. Users and developers should be aware of their size and manage them appropriately. While some Makefile targets exist for general cleanup, dedicated tidy-up scripts for logs and caches are planned for version 0.2.0 (see ROADMAP). These tools will help users and developers maintain a clean working environment and manage storage efficiently.
GABM follows good practice by using clear, simple naming for files and scripts, making the project easier to maintain and navigate. Scripts are named to match their corresponding Makefile targets, and the Makefile includes descriptive comments. All scripts and Python source code files are well commented and documented, supporting collaboration and onboarding. These conventions help ensure the project remains accessible and maintainable for both current and future contributors.
The addition of CODE_OF_CONDUCT.md is a prime example of the benefits of AI pair programming. When Andy suggested the project should have a code of conduct, the AI assistant quickly drafted the file, integrated it into the repository, updated the docs.py script, and ensured its inclusion in the Sphinx documentation. This streamlined workflow relieved Andy of a task and accelerated project progress. However, Andy found it important to review all changes, as AI assistants have limited session memory and may occasionally miss details. Comprehensive documentation helps bridge this gap, allowing Andy to teach and guide the AI assistant as needed. This collaborative process demonstrates how AI can normalize and accelerate good practice, while documentation ensures continuity and reproducibility for both human and AI contributors.
The project includes several Markdown files, each serving a specific purpose:

- **README.md**: Provides a project overview, setup instructions, and links to key documentation.
- **DEV_GUIDE.md**: Offers guidance for developers, including workflow, project structure, and best practices.
- **USER_GUIDE.md**: Contains instructions for end users on installing, configuring, and running GABM.
- **SETUP_GUIDE_USER.md**: Step-by-step environment setup for users.
- **SETUP_GUIDE_DEV.md**: Step-by-step environment setup for developers.
- **API_KEYS.md**: Details required API keys for LLMs and how to configure them.
- **CHANGE_LOG.md**: Tracks changes and updates across project releases.
- **ROADMAP.md**: Outlines planned features and future development goals.
- **CODE_OF_CONDUCT.md**: Defines expected behavior and reporting procedures.
- **CONTRIBUTORS.md**: Lists project contributors and their roles.
- **LICENSE.md**: Specifies the software license and terms of use.
- **requirements.txt**: Lists pinned dependencies for end users.
- **requirements-dev.txt**: Lists flexible dependencies for developers.
- **SECURITY.md**: Provides security guidelines and contact information.
- **CONTACT.md**: Offers contact details for maintainers and support.
- **DEVELOPMENT_HISTORY.md**: Chronicles the project’s development, milestones, and reflections.

This clear structure helps users and contributors find relevant information and understand the documentation layout. These files are referenced and included in the Sphinx documentation for consistency and accessibility.
The project’s directory structure is documented in the DEV_GUIDE and README, but it is also important to mention hidden directories such as .github (for workflows, security, and contact files) and .git (for version control metadata). The .gitignore file defines which files and directories are excluded from version control, such as build artifacts, caches, and large logs. This practice keeps the repository clean, secure, and focused on essential code and documentation, supporting reproducibility and maintainability.
The Python docs.py script (located in the scripts folder) also copies requirements text files and files from the .github directory (such as SECURITY.md and CONTACT.md) into the Sphinx docs directory. This ensures that key project metadata, security information, and contact details are included in the published documentation, supporting transparency and reproducibility.
To maximize platform agnosticism, GABM uses Python scripts alongside Makefiles to automate documentation workflows. A dedicated script copies Markdown files from the root directory, modifies them for formatting, and temporarily adds them to the docs folder for Sphinx compilation. The main Sphinx index.html page is based on README.md, included via index.md in the docs directory, following DRY principles. This ensures that core project information is maintained in a single location and consistently presented across both the repository and the documentation site.
GABM’s documentation is designed for both the GitHub repository and the Sphinx documentation site. Automation is handled via Makefile targets, which copy and fold Markdown files from the repository root into the Sphinx docs directory. Makefiles (using the make tool) provide a platform-agnostic way to manage build, test, and documentation workflows. Sphinx, together with MyST, generates rich, navigable documentation from Markdown and reStructuredText sources. This approach ensures consistency, reduces manual effort, and keeps user and developer documentation up to date.
The GABM project adopts a Don't Repeat Yourself (DRY) philosophy for both code and documentation, enhancing maintainability and ease of change. Recent documentation efforts have targeted separate guides for users and developers, as well as setup and advanced topics. API key requirements for LLMs were abstracted into a standalone Markdown file. For reproducibility, requirements.txt and requirements-dev.txt clearly specify dependencies: user requirements are pinned, while developer dependencies are more flexible. Further reflection on dependencies and reproducibility will be included, as these are critical for open science and sustainable software.
Prior to preparing for PyPI deployment, significant effort went into organizing and improving the documentation for GABM. Documentation is a continuous process, encompassing:
- **Sphinx Documentation**: For user/developer guides, API references, and project history, generated from Markdown and reStructuredText using Sphinx and MyST.
- **Source Code Comments**: Docstrings and inline comments provide essential context for developers and maintainers.
- **Other File Comments**: Comments in scripts, configuration, and data files clarify intent and usage.

Maintaining high-quality documentation is an ongoing, collaborative effort that evolves with the project and its community.
The latest development work enabled GABM to be released on PyPI, a process made much easier with guidance from GitHub Copilot. Andy, familiar with Java/Maven and Maven Central, found the Python release process more accessible thanks to Copilot’s explanations. A Makefile target was also added to delete tagged releases on GitHub. While PyPI allows for release deletion, Maven Central is designed for permanence, ensuring that dependencies remain available for the long term. This reliability reduces the burden on developers and optimizes network and storage usage through centralized repositories and caching, which benefits the wider software community.
At present, the project is being developed privately at the preference of Viktoria and Ajay, with plans to open the repository in due course. Although an open source license is in place, the repository is not yet public. For JOSS publication, the software must be released. The timing of this decision is up to the lead collaborators, but some workflows are currently limited by the private status and cannot be fully tested. This reflects the balance between collaborative development and the requirements of open science publication.
A critical part of open and responsible research software is the choice of license. GABM is released under the 3-clause BSD license, which clearly defines user rights, redistribution, and liability limitations. This permissive license encourages broad adoption and collaboration while protecting developers. Although license changes are possible, they become more difficult as the project matures and more organizations contribute. The initial choice of the BSD license reflects the project’s commitment to openness, collaboration, and legal clarity for all contributors.
Andy’s background in UK e-Science and e-Social Science (2005–2011) instilled the importance of reflection, introspection, and open science. The community, including colleagues at the Oxford Internet Institute, promoted sharing tools, knowledge, and computational resources to accelerate research and better understand the research process itself. This project continues that tradition, aiming for transparency and reproducibility rather than mystique.

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

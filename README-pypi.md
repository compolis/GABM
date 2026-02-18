<!-- Badges -->
<p align="left">
  <a href="https://github.com/compolis/GABM/blob/main/LICENSE" title="License">
    <img src="https://img.shields.io/github/license/compolis/GABM" alt="License" />
  </a>
  <a href="https://www.python.org/downloads/release/python-31212/" title="Python Version">
    <img src="https://img.shields.io/badge/python-3.12%2B-blue.svg" alt="Python Version" />
  </a>
  <a href="https://compolis.github.io/GABM/" title="Documentation">
    <img src="https://img.shields.io/badge/docs-Sphinx-green" alt="Documentation" />
  </a>
</p>
# GABM: Generative Agent-Based Model

[GABM](https://github.com/compolis/GABM/) is a flexible, extensible [Python](https://www.python.org/) framework for developing agent-based models that use large language models (LLMs) as agent reasoning engines. It supports use of multiple LLM providers and implements persistent response caching.

## Features
- Flexible, extensible agent-based modeling with LLMs
- Multi-provider LLM support
- Persistent response caching

## API Keys
You need a `data/api_key.csv` file with your API keys. This file is not included in the repository for security reasons.


Create `data/api_key.csv` yourself in the following CSV format:


You must sign up with each LLM provider to obtain an API key:

- **OpenAI:** Go to [platform.openai.com/signup](https://platform.openai.com/signup) and create an account. After logging in, visit [API Keys](https://platform.openai.com/api-keys) to generate a key. Use `openai` as the API name.
- **DeepSeek:** Register at [deepseek.com](https://deepseek.com/) and follow their documentation to obtain an API key. Use `deepseek` as the API name.
- **GenAI (Google):** Go to [makersuite.google.com](https://makersuite.google.com/) and sign in with your Google account. Follow instructions to get an API key. Use `genai` as the API name.
- **PublicAI (Apertus):** Sign up at [publicai.co](https://publicai.co/) to get your API key. Use `publicai` as the API name.

You can also add your [Hugging Face](https://huggingface.co/) token for downloading private or gated models:

## Installation
```bash
pip install gabm
```

## Run the Main Program
When you run GABM (e.g., with `python3 -m gabm`), the default behavior is to execute an Agent-Based Model (ABM) simulation. Here’s what happens:

### Agent Groups and Opinions

- The simulation creates three groups of agents: Negative, Positive, and Neutral.
- You can configure the number of agents in each group by editing variables at the top of the main script.
- Negative agents start with an opinion of -1.0, Positive agents with 1.0, and Neutral agents with 0.0.

### Communication Rounds

- The simulation runs for several rounds (configurable).
- In each round, agents from the Negative and Positive groups communicate with randomly selected Neutral agents.
- When a Neutral agent communicates, both the Neutral agent and the other agent update their opinions to the average of their current opinions. This models opinion mixing and convergence.

### Output and Visualization

- The simulation logs the state of the environment and the average opinion after each round to `data/logs/run_main.log`.
- After the simulation, a boxplot is generated showing the distribution of agent opinions at each round. This plot is saved to `data/output/test.png`.
- The boxplot helps visualize how opinions change and converge over time.
- The `data/logs` directory should contain `run_main.log`.

### Customization

- You can change the number of agents in each group, the number of rounds, and other parameters by editing the main script.
- The random seed is set for reproducibility, so results are consistent across runs unless you change the seed.

This ABM demonstration is a starting point, it does not show how LLMs can be used in an ABM yet!

## Documentation
Full documentation: https://compolis.github.io/GABM/

## Acknowledgements
This project was developed with significant assistance from [GitHub Copilot](https://github.com/features/copilot) for code generation, refactoring, and documentation improvements.

We gratefully acknowledge support from the [University of Leeds](https://www.leeds.ac.uk/). Funding for this project comes from a UKRI Future Leaders Fellowship awarded to [Professor Viktoria Spaiser](https://essl.leeds.ac.uk/politics/staff/102/professor-viktoria-spaiser) (grant reference: [UKRI2043](https://gtr.ukri.org/projects?ref=UKRI2043)).

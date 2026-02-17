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
From the project root:

```bash
python3 -m gabm
```

Depending on what LLM services are running and working, and what LLM API Keys are provided and valid, you will get different console messages and files created in the `data` directory.


The `data/logs` directory should contain the following file:
- `run_main.log`

The `data/logs/llm` directory should contain the following files:
- `deepseek.log`
- `genai.log`
- `openai.log`,
- `publicai.log`

The `data/llm` directory should contain directories for each of the LLM services that accepted the API keys provided and provided a response to the prompt given by running the main program.

## Documentation
Full documentation: https://compolis.github.io/GABM/

## Acknowledgements
This project was developed with significant assistance from [GitHub Copilot](https://github.com/features/copilot) for code generation, refactoring, and documentation improvements.

We gratefully acknowledge support from the [University of Leeds](https://www.leeds.ac.uk/). Funding for this project comes from a UKRI Future Leaders Fellowship awarded to [Professor Viktoria Spaiser](https://essl.leeds.ac.uk/politics/staff/102/professor-viktoria-spaiser) (grant reference: [UKRI2043](https://gtr.ukri.org/projects?ref=UKRI2043)).

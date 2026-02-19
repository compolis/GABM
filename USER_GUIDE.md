# User Guide


## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
- [Run the Main Program](#run-the-main-program)
- [Managing Logs and Caches](#managing-logs-and-caches)
- [Using LLM Modules](#using-llm-modules)
- [Troubleshooting](#troubleshooting)
- [Additional Resources](#additional-resources)


## Overview

This guide helps users get started with GABM, find documentation, and get support. Documentation will be updated as more features and configuration options are added.

In the rest of the document "you" means you as a GABM user.


## Getting Started

### Prerequisites

 You will either need a local installation of [Conda](https://conda.org/), or [Python](https://www.python.org/) at or above version 3.12. To check your default Python version run:

```bash
python3 --version
```

### Initial set up

#### Using Conda
If you use [Conda](https://conda.org/) which is distributed with [Anaconda](https://www.anaconda.com/), [Miniconda](https://docs.conda.io/en/latest/miniconda.html), or [Miniforge](https://github.com/conda-forge/miniforge), you can set up GABM in a new environment as follows:

```bash
conda create -n gabm
conda activate gabm
conda install python=3.12
pip install gabm==0.2.5
```

You can then check all installed dependencies and create your own requirements file with:

```bash
conda list -e > requirements.txt
```


#### Using Python >=3.12

Install from [PyPI](https://pypi.org/) using [Pip](https://pypi.org/project/pip/) as follows:

```bash
python3 -m venv gabm-venv
source gabm-venv/bin/activate  # On Windows: gabm-venv\\Scripts\\activate
pip install --upgrade pip
pip install gabm==0.2.5
```

You can then check installed dependencies with:

```bash
pip freeze > requirements.txt
```


#### Optional: Local LLM Support

By default, GABM installs only the dependencies needed for hosted LLM providers (OpenAI, Google, DeepSeek, etc.).
If you want to run LLMs locally (e.g., downloaded from Hugging Face), you need additional dependencies:

- torch
- transformers

These are listed in requirements-local-llm.txt in the project root.

To install with local LLM support, use:

```bash
pip install gabm[llm-local]
```

Or, manually install from requirements-local-llm.txt:

```bash
pip install -r requirements-local-llm.txt
```

This keeps the core installation lightweight for users who only use hosted LLMs.


### Set Up API Keys

Create `data/api_key.csv` with your API keys. For all supported LLM providers (including PublicAI/Apertus), see [API_KEYS.md](API_KEYS.md) for up-to-date details and instructions.



#### Using Local Apertus LLM Models

For instructions on downloading, authenticating, and using local Apertus LLM models (and other Hugging Face models), see [HUGGING_FACE.md](HUGGING_FACE.md).


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
- After the simulation, a separate boxplot is generated for each opinion topic (negative, neutral, positive), showing the distribution of agent opinions at each round. These plots are saved as `opinions_negative.png`, `opinions_neutral.png`, and `opinions_positive.png` in `data/output`.
- The boxplots help visualize how opinions change and converge over time for each topic. You should see positive and negative opinions mix and converge, while neutral opinions may behave differently depending on the communication rules.
- The `data/logs` directory should contain `run_main.log`.

### Customization

- You can change the number of agents in each group, the number of rounds, and other parameters by editing the main script.
- The random seed is set for reproducibility, so results are consistent across runs unless you change the seed.

This ABM demonstration is a starting point, it does not show how LLMs can be used in an ABM yet!


## Managing Logs and Caches

GABM creates logs and caches (such as prompt/response caches for LLM services and logs for ABM runs) that can grow large over time. Logs for LLM modules are written to `data/logs/llm/`, and logs for ABM runs are written to `data/logs/run_main.log`.

Check these log files for troubleshooting API issues, prompt/response errors, or cache problems. User-friendly ways to tidy up logs and caches and compile data into reproducible research objects are being developed for a future release. More details will be provided as these features are implemented.


## Using LLM Modules

GABM provides unified interfaces for sending prompts to various LLMs and listing available models. Each LLM module exposes a service class with the following functions:
```python
def send(self, api_key, message, model=None):
    """
    Send a prompt to the LLM and return the response object.
    Args:
        api_key (str): The API key for the LLM service.
        message (str): The message to send.
        model (str, optional): The model to use for the request.
    Returns:
        The response object from the LLM.
    """

def list_available_models(self, api_key):
    """
    List available models for the LLM service.
    Args:
        api_key (str): The API key for the LLM service.
    Returns:
        A list of available models.
    """
```

Caching and Logging:
- Responses are cached for reproducibility; repeated prompts return cached results.
- All send/responses are logged for audit and debugging.

Example Usage (where ```<User_API_Key>``` should be replaced with the user's API key for the OpenAI Service):
```python
from gabm.io.llm.openai import OpenAIService
service = OpenAIService()
response = service.send(api_key="<User_API_Key>", message="Hello!", model="gpt-3.5-turbo")
service.list_available_models(api_key="<User_API_Key>")
```

The `data/logs/llm` directory is for log files for each LLM service used.

The `data/llm` directory is for caches of prompts and responses for each LLM service used.


## Troubleshooting

If you encounter errors, check your Python version and that all dependencies are installed. If all versions match the documentation, please peruse [reported issues](https://github.com/compolis/GABM/issues), comment on a relevant open issue or [open an issue](https://github.com/compolis/GABM/issues/new/choose) to request support.


## Additional Resources

- [README.md](README.md)
- [Reported Issues](https://github.com/compolis/GABM/issues)
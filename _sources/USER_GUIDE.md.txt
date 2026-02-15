# User Guide


## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
- [Troubleshooting](#troubleshooting)
- [Running Models](#running-models)
- [Managing Logs and Caches](#managing-logs-and-caches)
- [Additional Resources](#additional-resources)


## Overview

This guide helps users get started with GABM, find documentation, and get support. Documentation will be updated as more features and configuration options are added.

In the rest of the document "you" means you as a GABM user.


## Getting Started

### Pre-requisits

 You will either need a local installation of [Conda](https://conda.org/), or [Python](https://www.python.org/) at or above version 3.12. To check your default Python version run:

```bash
python3 --version
```

### Initial set up

#### Using Conda
If you use [Conda](https://conda.org/) which is distributed with[Anaconda](https://www.anaconda.com/)/[Miniconda](https://docs.conda.io/en/latest/miniconda.html) and [Miniforge](https://github.com/conda-forge/miniforge) you can set up GABM in a new environment as follows:

```bash
conda create -n gabm
conda activate gabm
conda install python=3.12
pip install gabm==0.1.4
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
pip install gabm==0.1.4
```

You can then check installed dependencies with:

```bash
pip freeze > requirements.txt
```


### Set Up API Keys

Create `data/api_key.csv` with your API keys. For all supported LLM providers (including PublicAI/Apertus), see [API_KEYS.md](API_KEYS.md) for up-to-date details and instructions.


#### Using Local Apertus LLM Models

For instructions on downloading, installing, and using local Apertus LLM models, see [Apertus.md](Apertus.md). This guide covers both local and API-based usage, storage requirements, and troubleshooting.


### Run the Main Program

From the project root:

```bash
python3 -m gabm
```

Depending on what LLM services are running and working, and if your LLM API Keys are valid, you will get different console mesages and files created in the `data` directory.

The console messages should look something along the following lines:

```
2026-02-11 22:48:01,988 [INFO] Running gabm...
2026-02-11 22:48:01,989 [INFO] API Keys: {'openai': 'sk-Key', 'deepseek': 'sk-Key', 'genai': 'Key'}
2026-02-11 22:48:01,989 [WARNING] Model list file not found: data/llm/openai/models.txt
2026-02-11 22:48:01,989 [WARNING] Model list file not found: data/llm/genai/models.txt
2026-02-11 22:48:01,989 [WARNING] Model list file not found: data/llm/deepseek/models.txt
2026-02-11 22:48:01,989 [INFO] OpenAI API Key: sk-Key
2026-02-11 22:48:02,191 [ERROR] [openai] Error: Client.__init__() got an unexpected keyword argument 'proxies'
2026-02-11 22:48:02,191 [INFO] Listing available models for OpenAI...
2026-02-11 22:48:02,191 [ERROR] Error listing models for OpenAI: Client.__init__() got an unexpected keyword argument 'proxies'
2026-02-11 22:48:02,191 [ERROR] OpenAI response: None (API error or timeout)
2026-02-11 22:48:02,192 [INFO] GenAI API Key: Key
2026-02-11 22:48:15,205 [INFO] gabm.io.llm.genai: Cache updated for model=models/gemini-2.5-pro, message=Hello, GenAI!
2026-02-11 22:48:15,205 [INFO] Cache updated for model=models/gemini-2.5-pro, message=Hello, GenAI!
2026-02-11 22:48:15,205 [INFO] Full GenAI response:
{'_done': True, '_iterator': None, '_result': candidates {
  index: 0
  content {
    parts {
      text: "Hello there! It\'s great to connect with you.\n\nHow can I help you today? I\'m ready for any questions, creative ideas, or tasks you have in mind."
    }
    role: "model"
  }
  finish_reason: STOP
}
, '_chunks': [candidates {
  index: 0
  content {
    parts {
      text: "Hello there! It\'s great to connect with you.\n\nHow can I help you today? I\'m ready for any questions, creative ideas, or tasks you have in mind."
    }
    role: "model"
  }
  finish_reason: STOP
}
], '_error': None}
2026-02-11 22:48:15,205 [ERROR] GenAI response content: [Error accessing content: 'dict' object has no attribute 'text']
2026-02-11 22:48:15,206 [INFO] DeepSeek API Key: sk-Key
2026-02-11 22:48:15,209 [INFO] gabm.io.llm.deepseek: Cache updated for model=deepseek-model-1, message=Hello, DeepSeek!
2026-02-11 22:48:15,209 [INFO] Cache updated for model=deepseek-model-1, message=Hello, DeepSeek!
2026-02-11 22:48:15,209 [INFO] Full DeepSeek response:
{'model': 'deepseek-model-1', 'message': 'Hello, DeepSeek!', 'result': '[Placeholder DeepSeek response]'}
```

The `data/logs` directory should contain the following files:
`deepseek.log`,  `genai.log`, `openai.log`, `run_main.log`

The `data/llm` directory should contain directories for each of the LLM services that accepted the API keys provided and provided a response to the prompt given by running the main program.


## Troubleshooting

If you experience issues when installing, configuring, or running GABM, check here for guidance or updates. As the project evolves, troubleshooting tips and frequently asked questions will be added here.

If you encounter errors, check your Python version and that all dependencies are installed. If all versions match the documentation, please peruse [reported issues](https://github.com/compolis/GABM/issues), comment on a relevent open issue or [open an issue](https://github.com/compolis/GABM/issues/new/choose) to request support.


## Running Models

It is intended that you will be able to configure and run models. This section is to explain how to do this. This documentation will be updated in due course...


## Managing Logs and Caches

GABM creates logs and caches (such as prompt/response caches for LLM services) that can grow large over time. Logs for LLM modules are now written to:

  data/logs/llm/

Check these log files for troubleshooting LLM API issues, prompt/response errors, or cache problems. User friendly ways to tidy up logs and caches and compile data into reproducible research objects are being developed for a future release. More details will be provided as these features are implemented.


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


## Additional Resources

- [README.md](README.md)
- [Reported Issues](https://github.com/compolis/GABM/issues)
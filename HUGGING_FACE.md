# Hugging Face Model Usage Guide

## Table of Contents
- [Overview](#overview)
- [Authentication](#authentication)
- [Model Setup](#model-setup)
  - [Using a Model from Hugging Face](#using-a-model-from-hugging-face)
  - [Using a Downloaded Model from Local Cache](#using-a-downloaded-model-from-local-cache)
- [Comparing Local and Remote Outputs](#comparing-local-and-remote-outputs)
- [Troubleshooting](#troubleshooting)


## Overview

This guide explains how to set up and use Hugging Face-hosted models (including Apertus LLMs) with GABM, both locally and via remote APIs.


## Authentication

Some models require authentication to download from Hugging Face.

- **Recommended:** Store your Hugging Face token in `data/api_key.csv` as described in [API_KEYS.md](API_KEYS.md). GABM setup scripts will automatically set the `HF_TOKEN` environment variable from this file if present and not already set.


## Model Setup

### Using a Model from Hugging Face
1. Visit the [Apertus LLM collection](https://huggingface.co/collections/swiss-ai/apertus-llm) and choose a model.
2. Install the required package:
   ```bash
   pip install transformers
   ```
3. Load and use the model in Python:
   ```python
   from transformers import AutoModelForCausalLM, AutoTokenizer

   model_name = "swiss-ai/apertus-llm-7b"  # Example
   tokenizer = AutoTokenizer.from_pretrained(model_name)
   model = AutoModelForCausalLM.from_pretrained(model_name)

   prompt = "Give me a brief explanation of gravity in simple terms."
   inputs = tokenizer(prompt, return_tensors="pt")
   outputs = model.generate(**inputs, max_new_tokens=256)
   output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
   print(output_text)
   ```
   For chat-style prompting, see the [Hugging Face chat templating docs](https://huggingface.co/docs/transformers/main/en/chat_templating) or the model card.


### Using a Downloaded Model from Local Cache

If you have already downloaded a model (e.g., `swiss-ai/Apertus-8B-2509`), you can load it directly from your Hugging Face cache directory. This avoids re-downloading and works even if the model is no longer public.

Example (all platforms, adjust path as needed):
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

local_model_path = os.path.expanduser("~/.cache/huggingface/hub/models--swiss-ai--Apertus-8B-2509")
tokenizer = AutoTokenizer.from_pretrained(local_model_path)
model = AutoModelForCausalLM.from_pretrained(local_model_path)
```
Replace the path with your actual cache location if different. On Windows, the cache is typically in `%USERPROFILE%\.cache\huggingface\hub`.


## Comparing Local and Remote Outputs

You can compare the output of a local model and the same model accessed via a service API (e.g., PublicAI) to ensure consistency.

Example comparison script:
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import requests
import os

prompt = "Give me a brief explanation of gravity in simple terms."

# Local inference
local_model_path = os.path.expanduser("~/.cache/huggingface/hub/models--swiss-ai--Apertus-8B-2509")
tokenizer = AutoTokenizer.from_pretrained(local_model_path)
model = AutoModelForCausalLM.from_pretrained(local_model_path)
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=256)
local_result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("Local output:", local_result)

# Remote (PublicAI API example)
api_key = "YOUR_PUBLICAI_KEY"  # Replace with your key
url = "https://api.publicai.co/v1/chat/completions"
headers = {
   "Content-Type": "application/json",
   "Authorization": f"Bearer {api_key}",
   "User-Agent": "GABM/1.0"
}
data = {
   "model": "swiss-ai/apertus-8b-instruct",  # or 70b-instruct
   "messages": [{"role": "user", "content": prompt}]
}
response = requests.post(url, headers=headers, json=data)
remote_result = response.json()
print("Remote output:", remote_result)
```
This lets you verify that your local and remote model outputs are similar or spot differences.


## Troubleshooting

- If you see "401 Unauthorized", check your Hugging Face authentication and token.
- **Tip:** If you want to use only locally downloaded models, you do not need to set HF_TOKEN.
- For more details, see [API_KEYS.md](API_KEYS.md) and the Hugging Face documentation.

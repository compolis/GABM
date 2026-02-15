# Using Apertus LLM Models

This guide explains how to set up and use Apertus LLM models locally and via API in GABM.

## Table of Contents
- [Overview](#overview)
- [Local Setup](#local-setup)
- [API Integration](#api-integration)
- [Integration with GABM](#integration-with-gabm)
- [Troubleshooting](#troubleshooting)

## Overview
Apertus LLM models are available for download from Hugging Face and can also be accessed via API. This guide covers both approaches.

## Local Setup
1. Visit [Apertus LLM on Hugging Face](https://huggingface.co/collections/swiss-ai/apertus-llm) and choose a model.
2. Install Hugging Face Transformers:
   ```bash
   pip install transformers
   ```
3. Download and load the model in Python:
   ```python
   from transformers import AutoModelForCausalLM, AutoTokenizer

   model_name = "swiss-ai/apertus-llm-7b"  # Example
   tokenizer = AutoTokenizer.from_pretrained(model_name)
   model = AutoModelForCausalLM.from_pretrained(model_name)

   # Some models may not have a chat template. If you get an error about 'chat_template',
   # use a plain prompt instead of apply_chat_template:
   prompt = "Give me a brief explanation of gravity in simple terms."
   model_inputs = tokenizer(prompt, return_tensors="pt")
   generated_ids = model.generate(**model_inputs, max_new_tokens=256)
   output_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
   print(output_text)

   # If you want to use chat-style prompting and the model supports it, see:
   # https://huggingface.co/docs/transformers/main/en/chat_templating
   # or check the model card for a recommended template.
   ```
4. Integrate this into your GABM framework for local inference.

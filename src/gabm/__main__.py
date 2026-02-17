#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Entry point for running the GABM application.
To run: python3 -m gabm
This script tests LLM integrations, generates model lists, and caches responses, similar to setup-llms.py.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.2.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

import os
import sys
import logging
from pathlib import Path
from gabm.io.read_data import read_api_keys

# Enable/disable LLMs to test
ENABLED_LLMS = {
    "openai": True,
    "genai": True,
    "deepseek": True,
    "publicai": True,
    "apertus": False,  # Local model
}

# Map LLM names to their service class names
SERVICE_CLASSES = {
    "openai": "OpenAIService",
    "genai": "GenAIService",
    "deepseek": "DeepSeekService",
    "publicai": "PublicAIService",
}

# Default prompts and models for each LLM
DEFAULT_PROMPTS = {
    "openai": ("gpt-3.5-turbo", "Hello OpenAI!"),
    "genai": ("models/gemini-2.5-pro", "Hello GenAI!"),
    "deepseek": ("deepseek-chat", "Hello DeepSeek!"),
    "publicai": ("swiss-ai/apertus-70b-instruct", "Give me a brief explanation of gravity in simple terms."),
}

# Mapping from API model names to local Hugging Face model names
API_TO_LOCAL_MODEL = {
    "swiss-ai/apertus-8b-instruct": "swiss-ai/Apertus-8B-2509",
    "swiss-ai/apertus-70b-instruct": "swiss-ai/Apertus-70B-2509",
}

def model_list_files_exist(llm_name):
    base_dir = Path(f"data/llm/{llm_name}")
    json_file = base_dir / "models.json"
    txt_file = base_dir / "models.txt"
    return json_file.exists() and txt_file.exists()

def test_llm(llm, module, service_class, api_key, model, prompt):
    try:
        mod = __import__(module, fromlist=[service_class])
        Service = getattr(mod, service_class)
        service = Service()
        logging.info(f"Testing {llm} with model '{model}'...")
        resp = service.send(api_key, prompt, model=model)
        if resp:
            logging.info(f"  Success: Received response.")
        else:
            logging.warning(f"  Warning: No response received.")
    except Exception as e:
        logging.error(f"  Error testing {llm}: {e}")

def main():
    logging.info("\n--- GABM LLM Integration Test ---\n")
    # Load API keys
    api_keys = read_api_keys('data/api_key.csv')
    # Optionally set HF_TOKEN for Hugging Face if present and not already set
    if 'huggingface' in api_keys and not os.environ.get('HF_TOKEN'):
        os.environ['HF_TOKEN'] = api_keys['huggingface']
        logging.info("Set HF_TOKEN from data/api_key.csv for Hugging Face usage.")

    # Test each enabled LLM
    for llm, enabled in ENABLED_LLMS.items():
        if not enabled:
            continue
        api_key = api_keys.get(llm)
        if not api_key or api_key.startswith("YOUR_"):
            logging.warning(f"[SKIP] {llm}: API key not set.")
            continue
        module = f"gabm.io.llm.{llm}"
        service_class = SERVICE_CLASSES.get(llm)
        if not service_class:
            logging.warning(f"[SKIP] {llm}: No service class mapping.")
            continue
        # Generate model list if needed
        if not model_list_files_exist(llm):
            try:
                mod = __import__(module, fromlist=[service_class])
                Service = getattr(mod, service_class)
                service = Service()
                logging.info(f"Generating model list for {llm}...")
                service.list_available_models(api_key)
                logging.info(f"  Model list generated.")
            except Exception as e:
                logging.error(f"  Error generating model list for {llm}: {e}")
        # Test prompt/response and cache
        if llm in DEFAULT_PROMPTS:
            model, prompt = DEFAULT_PROMPTS[llm]
            test_llm(llm, module, service_class, api_key, model, prompt)
            # If PublicAI, also test local model for comparison
            if llm == "publicai":
                local_model = API_TO_LOCAL_MODEL.get(model)
                if local_model:
                    try:
                        from gabm.io.llm.apertus import local_apertus_infer
                        local_response = local_apertus_infer(local_model, prompt, device="cuda" if os.environ.get("CUDA_VISIBLE_DEVICES") else "cpu")
                        logging.info(f"Local Apertus response for '{local_model}':\n{local_response}")
                    except Exception as e:
                        logging.error(f"Error testing local Apertus model '{local_model}': {e}")
                else:
                    logging.warning(f"No local model mapping found for API model '{model}'.")

    # Optionally test Apertus local model ONLY if enabled
    if ENABLED_LLMS.get("apertus") is True:
        logging.info("\n--- Testing Apertus Local Model ---\n")
        try:
            from gabm.io.llm.apertus import local_apertus_infer
            api_model_id = "swiss-ai/apertus-70b-instruct"
            local_model_id = API_TO_LOCAL_MODEL.get(api_model_id, api_model_id)
            prompt = "Give me a brief explanation of gravity in simple terms."
            response = local_apertus_infer(local_model_id, prompt, device="cuda" if os.environ.get("CUDA_VISIBLE_DEVICES") else "cpu")
            logging.info(f"Apertus response:\n{response}")
        except Exception as e:
            logging.error(f"Error testing Apertus local model: {e}")
    logging.info("\nGABM LLM integration test complete. Check data/llm/* for model lists and caches.")

if __name__ == "__main__":
    # Set up logging to file and console
    log_dir = Path("data/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "run_main.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, mode="w"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    main()

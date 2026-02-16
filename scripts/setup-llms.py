#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup utility for LLM onboarding: tests API keys, generates model lists, and initializes caches.
Run with: python3 setup-llms.py
Or use the provided Makefile target `make setup-llms`.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.2.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import re
import os
import sys
from pathlib import Path
import logging
# Import function to read API keys from CSV
from gabm.io.read_data import read_api_keys


# Set to True to generate model lists for LLM services (requires valid API keys and may take time)
# Set to False to skip generate model lists for LLM services and just test sending a prompt and caching the response. 
GENERATE_MODEL_LISTS = True

# Enable/disable LLMs to test
ENABLED_LLMS = {
    "openai": True,
    "genai": True,
    "deepseek": True,
    "publicai": True,
    "apertus": False,  # Local model
}

def model_list_files_exist(llm_name):
    """
    Check if both the JSON and TXT model list files exist for the given LLM.
    """
    base_dir = Path(f"data/llm/{llm_name}")
    json_file = base_dir / "models.json"
    txt_file = base_dir / "models.txt"
    return json_file.exists() and txt_file.exists()

# Load API keys from CSV
API_KEYS = read_api_keys('data/api_key.csv')

# Optionally set HF_TOKEN for Hugging Face if present and not already set
if 'huggingface' in API_KEYS and not os.environ.get('HF_TOKEN'):
    os.environ['HF_TOKEN'] = API_KEYS['huggingface']
    logging.info("Set HF_TOKEN from data/api_key.csv for Hugging Face usage.")

# LLMS configuration: (llm_name, module_path)
LLMS = []
if ENABLED_LLMS["openai"]:
    LLMS.append(("openai", "gabm.io.llm.openai"))
if ENABLED_LLMS["genai"]:
    LLMS.append(("genai", "gabm.io.llm.genai"))
if ENABLED_LLMS["deepseek"]:
    LLMS.append(("deepseek", "gabm.io.llm.deepseek"))
if ENABLED_LLMS["publicai"]:
    LLMS.append(("publicai", "gabm.io.llm.publicai"))

# Map LLM names to their service class names
SERVICE_CLASSES = {
    "openai": "OpenAIService",
    "genai": "GenAIService",
    "deepseek": "DeepSeekService",
    "publicai": "PublicAIService",
}

# Default prompts and models for each LLM
DEFAULT_PROMPTS = {}
if ENABLED_LLMS["openai"]:
    DEFAULT_PROMPTS["openai"] = ("gpt-3.5-turbo", "Hello OpenAI!")
if ENABLED_LLMS["genai"]:
    DEFAULT_PROMPTS["genai"] = ("models/gemini-2.5-pro", "Hello GenAI!")
if ENABLED_LLMS["deepseek"]:
    DEFAULT_PROMPTS["deepseek"] = ("deepseek-chat", "Hello DeepSeek!")
if ENABLED_LLMS["publicai"]:
    DEFAULT_PROMPTS["publicai"] = ("swiss-ai/apertus-70b-instruct", "Give me a brief explanation of gravity in simple terms.")
    #DEFAULT_PROMPTS["publicai"] = ("swiss-ai/apertus-8b-instruct", "Give me a brief explanation of gravity in simple terms.")

# Mapping from API model names to local Hugging Face model names
API_TO_LOCAL_MODEL = {
    "swiss-ai/apertus-8b-instruct": "swiss-ai/Apertus-8B-2509",
    "swiss-ai/apertus-70b-instruct": "swiss-ai/Apertus-70B-2509",
    # Add more mappings as needed
}

def test_llm(llm, module, service_class, api_key, model, prompt):
    """
    Test sending a prompt to the specified LLM and print the result.
    Args:
        llm (str): The LLM name.
        module (str): The module path.
        service_class (str): The service class name.
        api_key (str): The API key for the LLM.
        model (str): The model name to use.
        prompt (str): The prompt message to send.
    """
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
    """
    Main setup function to generate model lists and test LLMs.
    """
    logging.info("\n--- LLM Setup Utility ---\n")

    for llm, module in LLMS:
        api_key = API_KEYS.get(llm)
        if not api_key or api_key.startswith("YOUR_"):
            logging.warning(f"[SKIP] {llm}: API key not set.")
            continue
        try:
            mod = __import__(module, fromlist=[SERVICE_CLASSES[llm]])
            Service = getattr(mod, SERVICE_CLASSES[llm])
            service = Service()
            if GENERATE_MODEL_LISTS:
                if model_list_files_exist(llm):
                    logging.info(f"Model list files already exist for {llm}, skipping generation.")
                else:
                    logging.info(f"Generating model list for {llm}...")
                    service.list_available_models(api_key)
                    logging.info(f"  Model list generated.")
        except Exception as e:
            logging.error(f"  Error generating model list for {llm}: {e}")
        # Test prompt/response and cache
        if llm in DEFAULT_PROMPTS:
            model, prompt = DEFAULT_PROMPTS[llm]
            test_llm(llm, module, SERVICE_CLASSES[llm], api_key, model, prompt)
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
    logging.info("\nSetup complete. Check data/llm/* for model lists and caches.")

if __name__ == "__main__":
    # Set up logging to file and console
    log_dir = Path("data/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "setup_llms.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, mode="w"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    main()

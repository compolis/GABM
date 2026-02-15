#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup utility for LLM onboarding: tests API keys, generates model lists, and initializes caches.
Run with: python3 setup-llms.py
Or use the provided Makefile target `make setup-llms`.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import re
import os
import sys
from pathlib import Path
import logging
# Import function to read API keys from CSV
from gabm.io.read_data import read_api_keys

# Either set to True to generate model lists for all LLMs (requires valid API keys and may take time), or False to skip this step and just test sending a prompt and caching the response. 
GENERATE_MODEL_LISTS = False
#GENERATE_MODEL_LISTS = True

# Load API keys from CSV
API_KEYS = read_api_keys('data/api_key.csv')

# LLM configuration
LLMS = []
if True:
    # Uncomment the LLMs you want to set up and test. Make sure to set API keys in data/api_key.csv before running.
    LLMS.append(("openai", "gabm.io.llm.openai"))
    #LLMS.append(("genai", "gabm.io.llm.genai"))
    #LLMS.append(("deepseek", "gabm.io.llm.deepseek"))
    #LLMS.append(("publicai", "gabm.io.llm.publicai"))

# Map LLM names to their service class names
SERVICE_CLASSES = {
    "openai": "OpenAIService",
    "genai": "GenAIService",
    "deepseek": "DeepSeekService",
    "publicai": "PublicAIService",
}

# Default test prompts and models for each LLM
DEFAULT_PROMPTS = {}
if True: 
    # Uncomment and customize the default prompts and models for testing each LLM. These will be used to send a test prompt and check the response, as well as initialize the cache.
    DEFAULT_PROMPTS["openai"] = ("gpt-3.5-turbo", "Hello OpenAI!")
    #DEFAULT_PROMPTS["genai"] = ("models/gemini-2.5-pro", "Hello GenAI!")
    #DEFAULT_PROMPTS["deepseek"] = ("deepseek-model-1", "Hello DeepSeek!")
    #DEFAULT_PROMPTS["publicai"] = ("swiss-ai/Apertus-8B-2509", "Give me a brief explanation of gravity in simple terms."),

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
                logging.info(f"Generating model list for {llm}...")
                service.list_available_models(api_key)
                logging.info(f"  Model list generated.")
        except Exception as e:
            logging.error(f"  Error generating model list for {llm}: {e}")
        # Test prompt/response and cache
        if llm in DEFAULT_PROMPTS:
            model, prompt = DEFAULT_PROMPTS[llm]
            test_llm(llm, module, SERVICE_CLASSES[llm], api_key, model, prompt)
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

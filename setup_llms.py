#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup utility for LLM onboarding: tests API keys, generates model lists, and initializes caches.
Run with: python3 setup_llms.py
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

# LLM configuration
LLMS = [
    ("openai", "src.io.llm.openai", "list_available_models"),
    ("genai", "src.io.llm.genai", "list_available_models"),
    ("deepseek", "src.io.llm.deepseek", "list_available_models"),
]

# Environment variable names for API keys
API_KEY_ENV = {
    "openai": "OPENAI_API_KEY",
    "genai": "GENAI_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
}

# Default test prompts and models for each LLM
DEFAULT_PROMPTS = {
    "openai": ("gpt-3.5-turbo", "Hello OpenAI!"),
    "genai": ("models/gemini-2.5-pro", "Hello GenAI!"),
    "deepseek": ("deepseek-model-1", "Hello DeepSeek!"),
}

def test_llm(llm, module, send_func, api_key, model, prompt):
    """
    Test sending a prompt to the specified LLM and print the result.
    Args:
        llm (str): The LLM name.
        module (str): The module path.
        send_func (str): The function name to send prompts.
        api_key (str): The API key for the LLM.
        model (str): The model name to use.
        prompt (str): The prompt message to send.
    """
    try:
        mod = __import__(module, fromlist=[send_func])
        send = getattr(mod, send_func)
        logging.info(f"Testing {llm} with model '{model}'...")
        resp = send(api_key, prompt, model=model)
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
    for llm, module, list_func in LLMS:
        api_key = os.environ.get(API_KEY_ENV[llm])
        if not api_key or api_key.startswith("YOUR_"):
            logging.warning(f"[SKIP] {llm}: API key not set.")
            continue
        try:
            mod = __import__(module, fromlist=[list_func])
            list_models = getattr(mod, list_func)
            logging.info(f"Generating model list for {llm}...")
            list_models(api_key)
            logging.info(f"  Model list generated.")
        except Exception as e:
            logging.error(f"  Error generating model list for {llm}: {e}")
        # Test prompt/response and cache
        if llm in DEFAULT_PROMPTS:
            model, prompt = DEFAULT_PROMPTS[llm]
            test_llm(llm, module, "send", api_key, model, prompt)
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

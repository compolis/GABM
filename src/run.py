#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the entry point for running the GABM application.
To run, use the command:
    python3 run.py
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import re
import sys
import logging
from pathlib import Path

def check_model_in_txt(models_txt_path, model_name):
    """
    Check if the specified model name exists in the models TXT file.
    Args:
        models_txt_path (Path): Path to the models TXT file.
        model_name (str): The model name to check.
    Returns:
        bool: True if the model is found or file does not exist, False otherwise.
    """
    if not models_txt_path.exists():
        logging.warning(f"Model list file not found: {models_txt_path}")
        return True  # Allow if no list exists
    with models_txt_path.open("r", encoding="utf-8") as f:
        content = f.read()
    # Look for exact model name in the file
    if re.search(rf"Model ID: (?:models/)?{re.escape(model_name)}\\b", content):
        return True
    logging.warning(f"Model '{model_name}' not found in {models_txt_path}. Please check available models.")
    return False

def main():
    """
    Main function for GABM.
    """
    logging.info("Running gabm...")
    # Get the api keys
    # Importing here to avoid circular imports
    from src.io.read_data import read_api_keys
    # Read API keys from the default location
    api_keys = read_api_keys(file_path='data/api_key.csv')
    # Print the API keys
    logging.info(f"API Keys: {api_keys}")
    
    if not api_keys:
        logging.error("No API keys found. Exiting.")
        return

    def handle_llm(name, key_name, module_name, message, content_path=None, model=None):
        if key_name not in api_keys:
            logging.warning(f"{name} API key not found. Skipping.")
            return
        api_key = api_keys.get(key_name)
        logging.info(f"{name} API Key: {api_key}")
        module = __import__(f"src.io.llm.{module_name}", fromlist=[module_name])
        send_func = getattr(module, "send")
        import inspect
        send_params = inspect.signature(send_func).parameters
        if "model" in send_params:
            response = send_func(api_key, message, model=model)
        else:
            response = send_func(api_key, message)
        if response is None:
            if hasattr(module, "list_available_models"):
                logging.info(f"Listing available models for {name}...")
                try:
                    module.list_available_models(api_key)
                except Exception as e:
                    logging.error(f"Error listing models for {name}: {e}")
            logging.error(f"{name} response: None (API error or timeout)")
            return
        # Log full response if possible
        if hasattr(response, "model_dump_json"):
            logging.info(f"Full {name} response:\n{response.model_dump_json(indent=2)}")
        else:
            logging.info(f"Full {name} response:\n{response}")
        # Log content if path provided
        if content_path:
            try:
                content = response
                for attr in content_path:
                    if isinstance(attr, int):
                        content = content[attr]
                    else:
                        content = getattr(content, attr)
                logging.info(f"{name} response content:\n{content}")
            except Exception as e:
                logging.error(f"{name} response content: [Error accessing content: {e}]")

    # Require explicit model names for each LLM
    #openai_model = None  # e.g., "gpt-3.5-turbo"
    openai_model = "gpt-3.5-turbo"
    #genai_model = None   # e.g., "models/gemini-2.5-pro"
    genai_model = "models/gemini-2.5-pro"
    #deepseek_model = None  # e.g., "deepseek-model-1"
    deepseek_model = "deepseek-model-1"
    # Add more as needed

    # Prompt or error if any model is not set
    missing_models = []
    if not openai_model:
        missing_models.append("openai_model")
    if not genai_model:
        missing_models.append("genai_model")
    if not deepseek_model:
        missing_models.append("deepseek_model")
    if missing_models:
        logging.error(f"You must explicitly set the following model variable(s) in run.py: {', '.join(missing_models)}")
        logging.error("See data/llm/{provider}/models.json for available models.")
        return

    # Check models.txt for each LLM if present
    from pathlib import Path
    openai_models_txt = Path("data/llm/openai/models.txt")
    genai_models_txt = Path("data/llm/genai/models.txt")
    deepseek_models_txt = Path("data/llm/deepseek/models.txt")
    if not check_model_in_txt(openai_models_txt, openai_model):
        print(f"[OpenAI] '{openai_model}' may not be available. See {openai_models_txt}.")
    if not check_model_in_txt(genai_models_txt, genai_model):
        print(f"[GenAI] '{genai_model}' may not be available. See {genai_models_txt}.")
    if not check_model_in_txt(deepseek_models_txt, deepseek_model):
        print(f"[DeepSeek] '{deepseek_model}' may not be available. See {deepseek_models_txt}.")
    # Handle each LLM
    handle_llm("OpenAI", "openai", "openai", "Hello, OpenAI!", ["choices", 0, "message", "content"], model=openai_model)
    handle_llm("GenAI", "genai", "genai", "Hello, GenAI!", ["text"], model=genai_model)
    handle_llm("DeepSeek", "deepseek", "deepseek", "Hello, DeepSeek!", None, model=deepseek_model)
    
if __name__ == "__main__":
    """
    Entry point for the script. Calls the main function.
    """
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

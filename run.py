#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the entry point for running the GABM application.
To run, use the command:
    python3 run.py
"""
# Metadata
__author__ = "Andy Turner <agdturner@gmail.com>"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

import re
def check_model_in_txt(models_txt_path, model_name):
    if not models_txt_path.exists():
        print(f"[Warning] Model list file not found: {models_txt_path}")
        return True  # Allow if no list exists
    with models_txt_path.open("r", encoding="utf-8") as f:
        content = f.read()
    # Look for exact model name in the file
    if re.search(rf"Model ID: (?:models/)?{re.escape(model_name)}\\b", content):
        return True
    print(f"[Warning] Model '{model_name}' not found in {models_txt_path}. Please check available models.")
    return False

def main():
    """
    Main function for GABM.
    """
    print("Running gabm...")
    # Get the api keys
    # Importing here to avoid circular imports
    from src.io.read_data import read_api_keys
    # Read API keys from the default location
    api_keys = read_api_keys(file_path='data/api_key.csv')
    # Print the API keys
    print("API Keys:", api_keys)
    
    if not api_keys:
        print("No API keys found. Exiting.")
        return

    def handle_llm(name, key_name, module_name, message, content_path=None, model=None):
        if key_name not in api_keys:
            print(f"{name} API key not found. Skipping.")
            return
        api_key = api_keys.get(key_name)
        print(f"{name} API Key:", api_key)
        module = __import__(f"src.io.llm.{module_name}", fromlist=[module_name])
        send_func = getattr(module, "send")
        # Pass model if supported
        import inspect
        send_params = inspect.signature(send_func).parameters
        if "model" in send_params:
            response = send_func(api_key, message, model=model)
        else:
            response = send_func(api_key, message)
        if response is None:
            # If the module has a list_available_models function, call it
            if hasattr(module, "list_available_models"):
                print(f"Listing available models for {name}...")
                try:
                    module.list_available_models(api_key)
                except Exception as e:
                    print(f"Error listing models for {name}: {e}")
            print(f"{name} response: None (API error or timeout)")
            return
        # Print full response if possible
        if hasattr(response, "model_dump_json"):
            print(f"\nFull {name} response:")
            print(response.model_dump_json(indent=2))
        else:
            print(f"\nFull {name} response:")
            print(response)
        # Print content if path provided
        if content_path:
            try:
                content = response
                for attr in content_path:
                    if isinstance(attr, int):
                        content = content[attr]
                    else:
                        content = getattr(content, attr)
                print(f"\n{name} response content:")
                print(content)
            except Exception as e:
                print(f"{name} response content: [Error accessing content: {e}]")

    # Require explicit model names for each LLM
    openai_model = None  # e.g., "gpt-3.5-turbo"
    genai_model = None   # e.g., "gemini-pro"
    deepseek_model = None  # e.g., "deepseek-model-1"
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
        print(f"Error: You must explicitly set the following model variable(s) in run.py: {', '.join(missing_models)}")
        print("See data/llm/{provider}/models.json for available models.")
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

    handle_llm("OpenAI", "openai", "openai", "Hello, OpenAI!", ["choices", 0, "message", "content"], model=openai_model)
    handle_llm("GenAI", "genai", "genai", "Hello, GenAI!", ["text"], model=genai_model)
    handle_llm("DeepSeek", "deepseek", "deepseek", "Hello, DeepSeek!", None, model=deepseek_model)
    #
    # # For Anthropic, check for both 'anthropic' and 'claude' keys
    # anthropic_key_name = "anthropic" if "anthropic" in api_keys else ("claude" if "claude" in api_keys else None)
    # if anthropic_key_name:
    #     handle_llm("Anthropic", anthropic_key_name, "anthropic", "Hello, Anthropic!", ["content", 0, "text"])
    # else:
    #     print("Anthropic API key not found. Skipping.")
    
if __name__ == "__main__":
    """
    Entry point for the script. Calls the main function.
    """
    main()

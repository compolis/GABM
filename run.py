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

    def handle_llm(name, key_name, module_name, message, content_path=None):
        if key_name not in api_keys:
            print(f"{name} API key not found. Skipping.")
            return
        api_key = api_keys.get(key_name)
        print(f"{name} API Key:", api_key)
        module = __import__(f"src.io.llm.{module_name}", fromlist=[module_name])
        response = getattr(module, "send")(api_key, message)
        if response is None:
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

    handle_llm("OpenAI", "openai", "openai", "Hello, OpenAI!", ["choices", 0, "message", "content"])
    """
    handle_llm("GenAI", "genai", "genai", "Hello, GenAI!", ["text"])
    # For Anthropic, check for both 'anthropic' and 'claude' keys
    anthropic_key_name = "anthropic" if "anthropic" in api_keys else ("claude" if "claude" in api_keys else None)
    if anthropic_key_name:
        handle_llm("Anthropic", anthropic_key_name, "anthropic", "Hello, Anthropic!", ["content", 0, "text"])
    else:
        print("Anthropic API key not found. Skipping.")
    """
    
if __name__ == "__main__":
    """
    Entry point for the script. Calls the main function.
    """
    main()

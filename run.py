#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The main GABM file. 
This is the entry point for running the GABM application.
To run, use the command:
    python3 run.py

@author: Andy Turner <agdturner@gmail.com>
@version: 0.1.0
@Copyright (c) 2026 GABM contributors, University of Leeds
"""
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
    # For demonstration, print the API keys
    print("API Keys:", api_keys)
    # For demonstration look up a specific API key
    openai = api_keys.get('openai', 'Not Found')
    print("OpenAI API Key:", openai)

if __name__ == "__main__":
    main()

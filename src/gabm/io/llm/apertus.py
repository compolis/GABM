"""
This script demonstrates how to use the Apertus-8B-2509 model from the Hugging Face Transformers library. It loads the model and tokenizer, prepares a prompt, generates a response, and prints the output.
To run this script, ensure you have the `transformers` library installed and access to the specified model. You can install the library using pip:
    pip install transformers
Adjust the `device` variable to "cuda" if you have a compatible GPU for faster inference.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.2.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
from pathlib import Path
import time
# Hugging Face Transformers for local model loading and inference
from transformers import AutoModelForCausalLM, AutoTokenizer
# Shared utilities for caching and logging
from .utils import load_llm_cache, cache_and_log, get_llm_cache_paths

def download_apertus_model(model_name: str) -> None:
    """
    Downloads and caches the specified Apertus model and tokenizer using Hugging Face Transformers.
    Args:
        model_name (str): The Hugging Face model name to download (e.g., 'swiss-ai/apertus-70b-instruct').
    """
    print(f"Downloading model and tokenizer for: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    print("Download complete. Model and tokenizer are now cached locally.")

from typing import Any, Optional, Dict

def local_apertus_infer(
    model_name: str,
    prompt: str,
    device: str = "cpu",
    cache: Optional[Dict[Any, Any]] = None,
    cache_path: Optional[str] = None,
    max_new_tokens: int = 32768,
    logger: Optional[Any] = None
) -> str:
    """
    Run local inference with an Apertus model, using shared cache and logging utilities.
    Args:
        model_name (str): The Hugging Face model name to use (e.g., 'swiss-ai/apertus-70b-instruct').
        prompt (str): The input prompt to send to the model.
        device (str): The device to run inference on ('cpu' or 'cuda').
        cache (dict, optional): An optional cache dictionary to use for caching responses.
        cache_path (str, optional): An optional path to the cache file. If not provided, uses default paths.
        max_new_tokens (int): The maximum number of new tokens to generate.
        logger: Optional logger for logging messages.
    Returns:
        str: The generated response from the model.
    """
    messages_think = [{"role": "user", "content": prompt}]
    cache_key = (model_name, prompt)
    # Use standard cache/log paths if not provided
    if cache_path is None:
        cache_path, jsonl_path = get_llm_cache_paths("apertus")
    else:
        cache_path = Path(cache_path)
        jsonl_path = cache_path.parent / "prompt_response_cache.jsonl"
    # Load cache if not provided
    if cache is None:
        cache = load_llm_cache(cache_path, logger)
    # Check cache
    if cache_key in cache:
        if logger:
            logger.info(f"Cache hit for model={model_name}, prompt={prompt}")
        return cache[cache_key]
    if logger:
        logger.info(f"Loading tokenizer and model for {model_name} on {device}...")
    t0 = time.time()
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
    t1 = time.time()
    if logger:
        logger.info(f"Model loaded in {t1-t0:.2f} seconds. Preparing input...")
    # Use chat template if available, else use prompt as-is
    if getattr(tokenizer, "chat_template", None):
        text = tokenizer.apply_chat_template(
            messages_think,
            tokenize=False,
            add_generation_prompt=True,
        )
    else:
        text = prompt
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    if logger:
        logger.info(f"Starting generation (max_new_tokens={max_new_tokens})...")
    t2 = time.time()
    generated_ids = model.generate(**model_inputs, max_new_tokens=max_new_tokens)
    t3 = time.time()
    if logger:
        logger.info(f"Generation complete in {t3-t2:.2f} seconds. Decoding output...")
    output_ids = generated_ids[0][len(model_inputs["input_ids"][0]):]
    response = tokenizer.decode(output_ids, skip_special_tokens=True)
    # Cache and log response using shared utility
    cache_and_log(
        cache,
        cache_key,
        response,
        cache_path,
        jsonl_path,
        prompt=prompt,
        model=model_name,
        logger=logger
    )
    if logger:
        logger.info(f"Local inference complete for model={model_name}.")
    return response
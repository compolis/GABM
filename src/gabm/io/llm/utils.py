"""
Utility functions for LLM API error handling, model listing, caching, and validation.

- Provides a decorator for safe API calls.
- Provides utilities to write model lists as both JSON and TXT for all LLMs.
- Provides a loader for model lists from JSON for validation and selection.

This supports a unified workflow for model management across all LLM providers in the project.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.2.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports

from datetime import datetime
import functools
import json
import logging
import os
from pathlib import Path
import pickle
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union


def safe_api_call(api_name: str) -> Callable:
    """
    Decorator to handle exceptions for LLM API calls and log errors gracefully.

    Args:
        api_name (str): Name of the API for logging purposes.

    Returns:
        function: Decorator that wraps the target function, returning None on error.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error(f"[{api_name}] Error: {e}")
                return None
        return wrapper
    return decorator

def list_models_to_txt(
    models: Iterable[Any],
    models_path: Path,
    formatter: Callable[[Any], str],
    header: Optional[str] = None
) -> None:
    """
    Write a list of models to a text file with a custom formatter.

    Args:
        models (iterable): List of model objects.
        models_path (Path): Path to the output file.
        formatter (callable): Function that takes a model and returns a string.
        header (str, optional): Header string for the file.
    """
    lines = [header] if header else []
    for model in models:
        lines.append(formatter(model))
    output = "\n".join(lines)
    logging.info(f"Writing model list to {models_path}")
    models_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with models_path.open("w", encoding="utf-8") as f:
            f.write(output)
    except Exception as e:
        logging.error(f"Error writing model list to {models_path}: {e}")

def write_models_json_and_txt(
    models: Iterable[Any],
    models_json_path: Path,
    models_txt_path: Path,
    formatter: Callable[[Any], str],
    header: Optional[str] = None
) -> None:
    """
    Write a list of models to both JSON and TXT files for LLM model management.

    Args:
        models (iterable): List of model objects or dicts.
        models_json_path (Path): Path to the output JSON file.
        models_txt_path (Path): Path to the output TXT file.
        formatter (callable): Function that takes a model and returns a string for TXT output.
        header (str, optional): Header string for the TXT file.

    This enables both human-readable and machine-readable model lists for all LLMs.
    """
    # Write JSON
    models_json_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        # If model is a dict, keep as is; if string, keep as is; if object, use __dict__
        def model_to_json(model):
            if isinstance(model, dict):
                return model
            elif isinstance(model, str):
                return model
            else:
                return model.__dict__
        with models_json_path.open("w", encoding="utf-8") as f:
            json.dump([model_to_json(model) for model in models], f, indent=2)
        logging.info(f"Wrote models to JSON: {models_json_path}")
    except Exception as e:
        logging.error(f"Error writing models to JSON {models_json_path}: {e}")
    # Write TXT
    lines = [header] if header else []
    for model in models:
        lines.append(formatter(model))
    output = "\n".join(lines)
    try:
        with models_txt_path.open("w", encoding="utf-8") as f:
            f.write(output)
        logging.info(f"Wrote models to TXT: {models_txt_path}")
    except Exception as e:
        logging.error(f"Error writing models to TXT {models_txt_path}: {e}")

def load_models_from_json(models_json_path: Path) -> List[Any]:
    """
    Load a list of models from a JSON file for validation and selection.

    Args:
        models_json_path (Path): Path to the JSON file.
    Returns:
        list: List of model dicts.
    """
    if not models_json_path.exists():
        logging.warning(f"Model JSON file not found: {models_json_path}")
        return []
    try:
        with models_json_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading models from JSON {models_json_path}: {e}")
        return []

def load_llm_cache(cache_path: Path, logger: Optional[Any] = None) -> Dict[Any, Any]:
    """
    Load a pickle cache from the given path. Returns an empty dict if not found or on error.
    Args:
        cache_path (Path): Path to the pickle file.
        logger: Logger for warnings (optional).
    Returns:
        dict: The loaded cache or an empty dict.
    """
    if cache_path.exists():
        try:
            with cache_path.open("rb") as f:
                return pickle.load(f)
        except Exception as e:
            if logger:
                logger.warning(f"Failed to load cache: {e}")
    return {}

def cache_and_log(
    cache: Dict[Any, Any],
    cache_key: Any,
    response: Any,
    cache_path: Union[Path, str],
    jsonl_path: Union[Path, str],
    prompt: Optional[str] = None,
    model: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
    logger: Optional[Any] = None
) -> None:
    """
    Cache and log the prompt/response pair to a JSONL file.
    Args:
        cache: The in-memory cache dictionary to update.
        cache_key: The key to use for caching the response.
        response: The response object to cache and log.
        cache_path (Path or str): Path to the pickle file for caching.
        jsonl_path (Path or str): Path to the JSONL file for logging.
        prompt (str, optional): The prompt that was sent (for logging).
        model (str, optional): The model used for the request (for logging).
        extra (dict, optional): Any extra information to include in the log entry.
        logger: Logger for info/error messages (optional).
    """
    cache[cache_key] = response
    cache_path = Path(cache_path)
    jsonl_path = Path(jsonl_path)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with cache_path.open("wb") as f:
            pickle.dump(cache, f)
        if logger:
            logger.info(f"Cache updated for model={model}, prompt={prompt}")
    except Exception as e:
        if logger:
            logger.error(f"Failed to write cache: {e}")
    # Write JSONL log
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "model": model,
        "prompt": prompt,
        "response": extract_text_from_response(response),
    }
    if extra:
        log_entry.update(extra)
    try:
        with jsonl_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        if logger:
            logger.info(f"Appended send/response to {jsonl_path}")
    except Exception as e:
        if logger:
            logger.error(f"Failed to write JSONL log: {e}")

def extract_text_from_response(response: Any) -> str:
    """
    Extract the text content from the LLM response object for logging.
    For local LLMs, this is just str(response). For remote, can be overridden.
    """
    return str(response)

def get_llm_cache_paths(service_name: str) -> Tuple[Path, Path]:
    """
    Return the cache (pickle) and JSONL log paths for a given LLM service.
    Args:
        service_name (str): The name of the LLM service (e.g., 'openai').
    Returns:
        tuple: (cache_path, jsonl_path) as Path objects
    """
    base = Path(f"data/llm/{service_name}")
    name = "prompt_response_cache"
    return (
        base / f"{name}.pkl",
        base / f"{name}.jsonl"
    )

def pre_send_check_and_cache(
    api_key: str,
    message: str,
    model: str,
    cache: Dict[Any, Any],
    logger: Any,
    service_name: str,
    api_key_env_var: str
) -> Optional[Any]:
    """
    Generic pre-send checks: API key presence, cache hit, and env var setup.
    Args:
        api_key (str): The API key for the LLM service.
        message (str): The message being sent.
        model (str): The model being used.
        cache (dict): The in-memory cache dictionary.
        logger: Logger for info/error messages.
        service_name (str): Name of the LLM service (for error messages).
        api_key_env_var (str): The environment variable name for the API key.
    Returns:
        The cached response if a cache hit occurs, or None if no cache hit or on error
    """
    if not api_key:
        logger.error(f"{service_name} API key must be provided.")
        raise RuntimeError(f"{service_name} API key must be provided.")
    cache_key = (message, model)
    if cache_key in cache:
        logger.info(f"Cache hit for model={model}, message={message}")
        return cache[cache_key]
    os.environ[api_key_env_var] = api_key
    return None

def call_and_cache_response(
    api_call: Callable[[], Any],
    cache_and_log_func: Callable,
    cache: Dict[Any, Any],
    cache_key: Any,
    cache_path: Any,
    jsonl_path: Any,
    prompt: Any,
    model: Any,
    api_key: str,
    logger: Any,
    service_name: str,
    list_available_models_func: Callable[[str], Any]
) -> Optional[Any]:
    """
    Generic try/except, error logging, model listing, and caching for LLM send methods.
    Args:
        api_call (callable): Function that performs the LLM API call and returns the response.
        cache_and_log_func (callable): Function to cache and log the response.
        cache (dict): The in-memory cache dictionary.
        cache_key: The cache key for this request.
        cache_path: Path to the pickle file for caching.
        jsonl_path: Path to the JSONL file for logging.
        prompt: The prompt/message sent.
        model: The model used.
        api_key: The API key (for model listing on error).
        logger: Logger for info/error messages.
        service_name (str): Name of the LLM service (for error messages).
        list_available_models_func (callable): Function to list available models.
    Returns:
        The response object or None on error.
    """
    try:
        response = api_call()
    except Exception as e:
        logger.error(f"[{service_name}] Error: {e}")
        if "404" in str(e) or "not found" in str(e) or "not supported" in str(e):
            list_available_models_func(api_key)
        return None
    cache_and_log_func(cache, cache_key, response, cache_path, jsonl_path, prompt=prompt, model=model, logger=logger)
    return response

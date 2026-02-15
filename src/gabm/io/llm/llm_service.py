"""
Base class for LLM service modules.
Provides shared cache, logging, and path management utilities.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
import pickle
import json
import os
from datetime import datetime
from pathlib import Path
from abc import ABC, abstractmethod
# Shared utilities for LLM modules
from gabm.utils.logging import setup_module_logger
from .utils import write_models_json_and_txt

def get_llm_cache_paths(service_name):
    """
    Return the cache (pickle) and JSONL log paths for a given LLM service.
    Args:
        service_name (str): The name of the LLM service (e.g., 'openai').
    Returns:
        tuple: (cache_path, jsonl_path) as Path objects
    """
    base = Path(f"data/llm/{service_name}")
    name = "prompts_response";
    return (
        base / f"{name}.pkl",
        base / f"{name}.jsonl"
    )

def load_llm_cache(cache_path, logger=None):
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


def cache_and_log(self, cache_key, response, prompt=None, model=None, extra=None):
def _write_model_list(self, models, formatter, header=None):

class LLMService(ABC):
    """
    Abstract base class for LLM service modules. Provides shared cache management, logging, and model list utilities.
    Subclasses must implement the send() and list_available_models() methods.
    """

        SERVICE_NAME = None  # Should be overridden by subclasses

    def __init__(self, logger=None):
        """
        Initialize the LLM service, setting up logger, cache paths, and loading cache.
        """
        if self.SERVICE_NAME is None:
            raise ValueError("SERVICE_NAME must be set in subclass.")
        self.logger = logger or setup_module_logger(__name__, f"{self.SERVICE_NAME}.log")
        self.cache_path, self.jsonl_path = get_llm_cache_paths(self.SERVICE_NAME)
        self.cache = load_llm_cache(self.cache_path, self.logger)

    @property
    def API_KEY_ENV_VAR(self):
        """Environment variable name for the API key."""
        return self.SERVICE_NAME.upper() + "_API_KEY"

    @staticmethod
    def _cache_and_log_response(
        cache: dict,
        cache_key,
        response,
        cache_path: Path,
        jsonl_path: Path,
        prompt=None,
        model=None,
        extra: dict = None,
        logger=None):
        """
        Cache the response and log the prompt/response pair to a JSONL file. Used by all LLM service modules for a unified workflow.
        Args:
            cache (dict): The in-memory cache dictionary to update.
            cache_key: The key to use for caching the response.
            response: The response object to cache and log.
            cache_path (Path): Path to the pickle file for caching.
            jsonl_path (Path): Path to the JSONL file for logging.
            prompt (str, optional): The prompt that was sent (for logging).
            model (str, optional): The model used for the request (for logging).
            extra (dict, optional): Any extra information to include in the log entry.
            logger: Logger for info/error messages (optional).
        """
        cache[cache_key] = response
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
            "response": response,
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

    def set_api_key_env(self, api_key):
        """
        Set the API key environment variable for this service.
        Args:
            api_key (str): The API key to set in the environment variable.
        """
        os.environ[self.API_KEY_ENV_VAR] = api_key

    def cache_and_log(self, cache_key, response, prompt=None, model=None, extra=None):
        """
        Cache and log a response using the standard mechanism.
        Args:
            cache_key: The key to use for caching the response.
            response: The response object to cache and log.
            prompt (str, optional): The prompt that was sent (for logging).
            model (str, optional): The model used for the request (for logging).
            extra (dict, optional): Any extra information to include in the log entry.
        """
        self._cache_and_log_response(
            self.cache,
            cache_key,
            response,
            self.cache_path,
            self.jsonl_path,
            prompt=prompt,
            model=model,
            extra=extra,
            logger=self.logger
        )

    def _write_model_list(self, models, formatter, header=None):
        """
        Write a list of models to JSON and TXT files using a formatter.
        Args:
            models (iterable): List of model objects or dicts.
            formatter (callable): Function that takes a model and returns a string for TXT output.
            header (str, optional): Header string for the TXT file.
        """
        model_json_path = getattr(self, 'model_json_path', None) or self.cache_path.parent / "models.json"
        model_txt_path = getattr(self, 'model_txt_path', None) or self.cache_path.parent / "models.txt"
        write_models_json_and_txt(
            models,
            model_json_path,
            model_txt_path,
            formatter,
            header=header
        )

    @abstractmethod
    def send(self, api_key, message, model=None):
        """
        Send a prompt to the LLM and return the response object.
        Args:
            api_key (str): The API key for the LLM service.
            message (str): The message to send.
            model (str, optional): The model to use for the request.
        Returns:
            The response object from the LLM.
        """
        pass

    @abstractmethod
    def list_available_models(self, api_key):
        """
        List available models for the LLM service.
        Args:
            api_key (str): The API key for the LLM service.
        Returns:
            A list of available models.
        """
        pass

    def _pre_send_check_and_cache(self, api_key, message, model):
        """
        Generic pre-send checks: API key presence, cache hit, and env var setup.
        Args:          
            api_key (str): The API key for the LLM service.
            message (str): The message being sent.
            model (str): The model being used.
        Returns:
            The cached response if a cache hit occurs, or None if no cache hit or on error
        """
        if not api_key:
            self.logger.error(f"{self.SERVICE_NAME} API key must be provided.")
            raise RuntimeError(f"{self.SERVICE_NAME} API key must be provided.")
        cache_key = (message, model)
        if cache_key in self.cache:
            self.logger.info(f"Cache hit for model={model}, message={message}")
            return self.cache[cache_key]
        self.set_api_key_env(api_key)
        return None

    def _call_and_cache_response(self, api_call, cache_key, prompt, model, api_key):
        """
        Generic try/except, error logging, model listing, and caching for LLM send methods.
        Args:
            api_call (callable): Function that performs the LLM API call and returns the response.
            cache_key: The cache key for this request.
            prompt: The prompt/message sent.
            model: The model used.
            api_key: The API key (for model listing on error).
        Returns:
            The response object or None on error.
        """
        try:
            response = api_call()
        except Exception as e:
            self.logger.error(f"[{self.SERVICE_NAME}] Error: {e}")
            if "404" in str(e) or "not found" in str(e) or "not supported" in str(e):
                self.list_available_models(api_key)
            return None
        self.cache_and_log(cache_key, response, prompt=prompt, model=model)
        return response

"""
Base class for LLM service modules.
Provides shared cache, logging, and path management utilities.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
import os
from abc import ABC, abstractmethod
# Shared utilities for caching and logging
from gabm.utils.logging import setup_module_logger
from .utils import write_models_json_and_txt, get_llm_cache_paths, load_llm_cache, cache_and_log, pre_send_check_and_cache, call_and_cache_response


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

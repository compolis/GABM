"""
For sending prompts to OpenAI, receiving responses, and managing model lists and cache.

Features:
- Send prompts to OpenAI and cache responses for reproducibility.
- List available models from the OpenAI API and save as both JSON and TXT for validation and reference.
- Validate selected model names against the cached JSON model list.
- Unified workflow for model management, matching other LLM modules in the project.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.2.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# OpenAI client library
from openai import OpenAI
# LLM service base class
from .llm_service import LLMService
# Shared utilities for caching and logging
from .utils import pre_send_check_and_cache, call_and_cache_response, cache_and_log, write_models_json_and_txt


class OpenAIService(LLMService):
    """
    Service class for OpenAI LLM integration. 
    Handles prompt sending, response caching, logging, and model listing.
    """
    SERVICE_NAME = "openai"

    def send(self, api_key, message, model="gpt-3.5-turbo"):
        """
        Send a prompt to OpenAI and return the response object.
        Caches and logs the response for reproducibility.
        Args:
            api_key (str): OpenAI API key.
            message (str): Prompt to send.
            model (str): Model name (default: "gpt-3.5-turbo").
        Returns:
            Response object or None on error.
        """
        cached = pre_send_check_and_cache(api_key, message, model, self.cache, self.logger, self.SERVICE_NAME, self.API_KEY_ENV_VAR)
        if cached is not None:
            return cached
        cache_key = (message, model)
        client = OpenAI()
        def api_call():
            return client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message}]
            )
        return call_and_cache_response(
            api_call,
            cache_and_log,
            self.cache,
            cache_key,
            self.cache_path,
            self.jsonl_path,
            message,
            model,
            api_key,
            self.logger,
            self.SERVICE_NAME,
            self.list_available_models,
            extract_text_from_response=None
        )

    def list_available_models(self, api_key):
        """
        List available OpenAI models and write them to JSON and TXT files.
        Args:
            api_key (str): OpenAI API key.
        """
        client = OpenAI(api_key=api_key)
        models = client.models.list()
        def formatter(model):
            return (f"Model ID: {model.id}\n"
                    f"  Owned by: {getattr(model, 'owned_by', 'N/A')}\n"
                    f"  Created: {getattr(model, 'created', 'N/A')}\n")
        self.logger.info(f"Writing {self.SERVICE_NAME} model list to JSON and TXT.")
        write_models_json_and_txt(
            models,
            self.cache_path.parent / "models.json",
            self.cache_path.parent / "models.txt",
            formatter,
            header=f"Available {self.SERVICE_NAME} models:\n"
        )
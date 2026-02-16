"""
For sending prompts to DeepSeek, receiving responses, and managing model lists and cache.

Features:
- Send prompts to DeepSeek and cache responses for reproducibility.
- List available models from the DeepSeek API and save as both JSON and TXT for validation and reference.
- Validate selected model names against the cached JSON model list.
- Unified workflow for model management, matching other LLM modules in the project.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.2.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# DeepSeek client library
from deepseek import DeepSeekAPI
# LLM service base class
from .llm_service import LLMService
# Shared utilities for caching and logging
from .utils import pre_send_check_and_cache, call_and_cache_response, cache_and_log


class DeepSeekService(LLMService):
    """
    Service class for DeepSeek LLM integration. 
    Handles prompt sending, response caching, logging, and model listing.
    """
    SERVICE_NAME = "deepseek"

    def send(self, api_key, message, model="deepseek-model-1"):
        """
        Send a prompt to DeepSeek and return the response object.
        Caches and logs the response for reproducibility.
        Args:
            api_key (str): DeepSeek API key.
            message (str): Prompt to send.
            model (str): Model name (default: "deepseek-model-1").
        Returns:
            Response object (dict) or None on error.
        """
        cached = pre_send_check_and_cache(api_key, message, model, self.cache, self.logger, self.SERVICE_NAME, self.API_KEY_ENV_VAR)
        if cached is not None:
            return cached
        cache_key = (message, model)
        try:
            client = DeepSeekAPI(api_key=api_key)
        except Exception as e:
            self.logger.error(f"[deepseek] Could not initialize DeepSeekAPI: {e}")
            return None
        def api_call():
            kwargs = {"prompt": message}
            if model:
                kwargs["model"] = model
            return client.chat_completion(**kwargs)
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
            self.list_available_models
        )

    def list_available_models(self, api_key):
        """
        List available DeepSeek models and write them to JSON and TXT files.
        Args:
            api_key (str): DeepSeek API key.
        """
        try:
            client = DeepSeekAPI(api_key=api_key)
        except Exception as e:
            self.logger.error(f"[deepseek] Could not initialize DeepSeekAPI: {e}")
            return
        models = client.get_models()
        self.logger.info(f"Raw model list from DeepSeek: {models}")
        # Handle both string and dict model formats
        def formatter(model):
            if isinstance(model, dict):
                return (f"Model ID: {model.get('id', model.get('model', 'N/A'))}\n"
                        f"  Description: {model.get('description', 'N/A')}\n")
            else:
                return f"Model: {model}\n"
        self.logger.info("Writing DeepSeek model list to JSON and TXT.")
        self._write_model_list(
            models,
            formatter,
            header=f"Available {self.SERVICE_NAME.capitalize()} models:\n"
        )
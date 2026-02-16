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
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# DeepSeek client library
import deepseek
# LLM service base class
from .llm_service import LLMService

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
        cached = self._pre_send_check_and_cache(api_key, message, model)
        if cached is not None:
            return cached
        cache_key = (message, model)
        if deepseek is None:
            self.logger.error("[deepseek] Python client not installed. Cannot send request.")
            return None
        # TODO: Replace with actual DeepSeek client usage
        # client = deepseek.Client(api_key=api_key)
        # def api_call():
        #     return client.chat.completions.create(model=model, messages=[{"role": "user", "content": message}])
        # For now, just a placeholder response:
        def api_call():
            return {"model": model, "message": message, "result": "[Placeholder DeepSeek response]"}
        return self._call_and_cache_response(api_call, cache_key, message, model, api_key)

    def list_available_models(self, api_key):
        """
        List available DeepSeek models and write them to JSON and TXT files.
        Args:
            api_key (str): DeepSeek API key.
        """
        if deepseek is None:
            self.logger.error("[deepseek] Python client not installed. Cannot list models.")
            return
        # TODO: Replace with actual DeepSeek client usage
        # client = deepseek.Client(api_key=api_key)
        # models = client.list_models()
        # For now, just a placeholder:
        models = [
            {"id": "deepseek-model-1", "description": "Example model 1"},
            {"id": "deepseek-model-2", "description": "Example model 2"},
        ]
        def formatter(model):
            return (f"Model ID: {model['id']}\n"
                    f"  Description: {model.get('description', 'N/A')}\n")
        self.logger.info("Writing DeepSeek model list to JSON and TXT.")
        self._write_model_list(
            models,
            formatter,
            header=f"Available {self.SERVICE_NAME.capitalize()} models:\n"
        )
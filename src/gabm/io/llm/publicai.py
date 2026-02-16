"""
For sending prompts to PublicAI (Apertus), receiving responses, and managing model lists and cache.

Features:
- Send prompts to PublicAI and cache responses for reproducibility.
- List available models from the PublicAI API and save as both JSON and TXT for validation and reference.
- Validate selected model names against the cached JSON model list.
- Unified workflow for model management, matching other LLM modules in the project.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"



import requests
from .llm_service import LLMService

class PublicAIService(LLMService):
    """
    Service class for PublicAI LLM integration. Handles prompt sending, response caching, logging, and model listing.
    """
    SERVICE_NAME = "publicai"

    def send(self, api_key, message, model="swiss-ai/apertus-8b-instruct"):
        """
        Send a prompt to PublicAI and return the response object.
        Caches and logs the response for reproducibility.
        Args:
            api_key (str): PublicAI API key.
            message (str): Prompt to send.
            model (str): Model name (default: "apertus-llm-7b").
        Returns:
            Response object (dict) or None on error.
        """
        cached = self._pre_send_check_and_cache(api_key, message, model)
        if cached is not None:
            return cached
        cache_key = (message, model)
        def api_call():
            url = "https://api.publicai.co/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "GABM/1.0"
            }
            data = {
                "model": model,
                "messages": [
                    {"role": "user", "content": message}
                ]
            }
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        return self._call_and_cache_response(api_call, cache_key, message, model, api_key)

    def list_available_models(self, api_key):
        """
        List available PublicAI models and write them to JSON and TXT files.
        Args:
            api_key (str): PublicAI API key.
        """
        url = "https://api.publicai.co/v1/models"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "GABM/1.0"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        models_data = response.json()
        # The API returns a dict with a 'data' key containing the list of models
        models = models_data.get("data", [])
        def formatter(model):
            if isinstance(model, dict):
                return (f"Model ID: {model.get('id', model.get('model', 'N/A'))}\n"
                        f"  Description: {model.get('description', 'N/A')}\n")
            else:
                return f"Model: {model}\n"
        self.logger.info("Writing PublicAI model list to JSON and TXT.")
        self._write_model_list(
            models,
            formatter,
            header="Available PublicAI models:\n"
        )

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


from .llm_service import LLMService

class PublicAIService(LLMService):
    """
    Service class for PublicAI LLM integration. Handles prompt sending, response caching, logging, and model listing.
    """
    SERVICE_NAME = "publicai"

    def send(self, api_key, message, model="apertus-llm-7b"):
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
        # TODO: Implement actual PublicAI API call here
        # For now, just a placeholder response:
        def api_call():
            return {"model": model, "message": message, "result": "[Placeholder PublicAI response]"}
        return self._call_and_cache_response(api_call, cache_key, message, model, api_key)

    def list_available_models(self, api_key):
        """
        List available PublicAI models and write them to JSON and TXT files.
        Args:
            api_key (str): PublicAI API key.
        """
        # TODO: Implement actual PublicAI API call here
        # For now, just a placeholder:
        models = [
            {"id": "apertus-llm-7b", "description": "Apertus LLM 7B"},
            {"id": "apertus-llm-8b", "description": "Apertus LLM 8B"},
        ]
        def formatter(model):
            return (f"Model ID: {model['id']}\n"
                    f"  Description: {model.get('description', 'N/A')}\n")
        self.logger.info("Writing PublicAI model list to JSON and TXT.")
        self._write_model_list(
            models,
            formatter,
            header="Available PublicAI models:\n"
        )

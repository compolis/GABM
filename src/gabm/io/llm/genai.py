"""
For sending prompts to Google Generative AI (genai), receiving responses, and managing model lists and cache.

Features:
- Send prompts to GenAI and cache responses for reproducibility.
- List available models from the GenAI API and save as both JSON and TXT for validation and reference.
- Validate selected model names against the cached JSON model list.
- Unified workflow for model management, matching other LLM modules in the project.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Google Generative AI client library
import google.generativeai as genai
# LLM service base class
from .llm_service import LLMService

class GenAIService(LLMService):
    """
    Service class for Google Generative AI LLM integration. 
    Handles prompt sending, response caching, logging, and model listing.
    """
    SERVICE_NAME = "genai"

    def send(self, api_key, message, model="models/gemini-2.5-pro"):
        """
        Send a prompt to Google Generative AI and return the response object.
        Caches and logs the response for reproducibility.
        Args:
            api_key (str): Google API key.
            message (str): Prompt to send.
            model (str): Model name (default: "models/gemini-2.5-pro").
        Returns:
            Response object (dict) or None on error.
        """
        cached = self._pre_send_check_and_cache(api_key, message, model)
        if cached is not None:
            return cached
        cache_key = (message, model)
        genai.configure(api_key=api_key)
        def api_call():
            model_obj = genai.GenerativeModel(model)
            response = model_obj.generate_content(message)
            # Convert to dict if possible
            if hasattr(response, 'to_dict'):
                return response.to_dict()
            elif hasattr(response, '__dict__'):
                return dict(response.__dict__)
            else:
                return response
        return self._call_and_cache_response(api_call, cache_key, message, model, api_key)

    def list_available_models(self, api_key):
        """
        List available GenAI models and write them to JSON and TXT files.
        Args:
            api_key (str): Google API key.
        """
        genai.configure(api_key=api_key)
        models = list(genai.list_models())
        def formatter(model):
            if isinstance(model, dict):
                name = model.get('name', 'N/A')
                desc = model.get('description', 'N/A')
                methods = model.get('supported_generation_methods', 'N/A')
            else:
                name = getattr(model, 'name', 'N/A')
                desc = getattr(model, 'description', 'N/A')
                methods = getattr(model, 'supported_generation_methods', 'N/A')
            return (f"Model ID: {name}\n"
                    f"  Description: {desc}\n"
                    f"  Supported methods: {methods}\n")
        self.logger.info("Writing GenAI model list to JSON and TXT.")
        self._write_model_list(
            models,
            formatter,
            header=f"Available {self.SERVICE_NAME.capitalize()} models and supported methods:\n"
        )

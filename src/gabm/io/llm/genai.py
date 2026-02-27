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
__version__ = "0.3.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"

# Standard library imports
import ast
# Google Generative AI client library
#import google.generativeai as genai
import google.genai as genai
# OpenAI-compatible client for dynamic model listing
from openai import OpenAI
# LLM service base class
from .llm_service import LLMService
# Shared utilities for caching and logging
from .utils import pre_send_check_and_cache, call_and_cache_response, cache_and_log, write_models_json_and_txt

class GenAIService(LLMService):
    """
    Service class for Google Generative AI LLM integration. 
    Handles prompt sending, response caching, logging, and model listing.
    """
    SERVICE_NAME = "genai"

    def send(self, api_key, message, model="models/gemini-2.5-flash"):
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
        cached = pre_send_check_and_cache(api_key, message, model, self.cache, self.logger, self.SERVICE_NAME, self.API_KEY_ENV_VAR)
        if cached is not None:
            return cached
        cache_key = (message, model)
        def api_call():
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=model,
                contents={"text": message}
            )
            client.close()
            # Convert to dict if possible
            if hasattr(response, 'to_dict'):
                return response.to_dict()
            elif hasattr(response, '__dict__'):
                return dict(response.__dict__)
            else:
                return response
        return self._call_with_error_handling(
            call_and_cache_response,
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
            extract_text_from_response=self.extract_text_from_response
        )

    def list_available_models(self, api_key):
        """
        Dynamically fetches the list of available Gemini models using the OpenAI-compatible API.
        Requires the openai package and a valid Gemini API key.
        """
        def api_call():
            client = OpenAI(
                api_key=api_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )
            models = list(client.models.list())
            model_dicts = []
            for model in models:
                model_dicts.append({
                    "id": getattr(model, "id", None),
                    "object": getattr(model, "object", None),
                    "owned_by": getattr(model, "owned_by", None),
                    "description": getattr(model, "description", ""),
                })
            def formatter(model):
                return (f"Model ID: {model.get('id', 'N/A')}\n"
                        f"  Description: {model.get('description', 'N/A')}\n"
                        f"  Owned by: {model.get('owned_by', 'N/A')}\n")
            self.logger.info("Writing GenAI model list to JSON and TXT (dynamic list from OpenAI-compatible endpoint).")
            write_models_json_and_txt(
                model_dicts,
                self.cache_path.parent / "models.json",
                self.cache_path.parent / "models.txt",
                formatter,
                header=f"Available {self.SERVICE_NAME.capitalize()} models (dynamic list):\n"
            )
            return model_dicts
        return self._call_with_error_handling(api_call)

    def extract_text_from_response(self, response):
        """
        Extract the text content from a GenAI response object for logging.
        Recursively searches for the first 'text' value in any nested structure.
        Logs a warning if no text is found.
        """
        def find_text(obj):
            if isinstance(obj, dict):
                # Direct text field
                if "text" in obj and isinstance(obj["text"], str):
                    return obj["text"]
                # Recursively search all values
                for v in obj.values():
                    result = find_text(v)
                    if result:
                        return result
            elif isinstance(obj, list):
                for item in obj:
                    result = find_text(item)
                    if result:
                        return result
            return None

        # Debug: log the type and a preview of the response
        if hasattr(self, 'logger') and self.logger:
            self.logger.debug(f"[GenAI] extract_text_from_response type={type(response)} preview={str(response)[:200]}")

        # If response is a string that looks like a dict, try to eval/parse it
        if isinstance(response, str) and response.strip().startswith("{"):
            try:
                resp_dict = ast.literal_eval(response)
                text = find_text(resp_dict)
                if text:
                    return text
            except Exception:
                pass
        # If response is a dict or list, search recursively
        if isinstance(response, (dict, list)):
            text = find_text(response)
            if text:
                return text
        # If response is an object, try attribute access
        if hasattr(response, "text") and isinstance(response.text, str):
            return response.text
        if hasattr(response, "candidates") and response.candidates:
            text = find_text(response.candidates)
            if text:
                return text
        # Fallback
        if hasattr(self, 'logger') and self.logger:
            self.logger.warning(f"[GenAI] Could not extract text from response: {str(response)[:200]}")
        return str(response)

"""
For testing local LLM integration (e.g., Apertus) without relying on external APIs.

Note:
    The @pytest.mark.timeout decorator is used to limit test duration. However, for large deep learning models
    (such as Apertus), model loading and inference may not always be interrupted reliably by pytest-timeout,
    especially if the underlying library (e.g., PyTorch, Transformers) is executing C/CUDA code or subprocesses.
    If a test appears to hang or exceed the timeout, manual interruption may be required.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


# Standard library imports
import os
import pytest
# Local imports
from gabm.io.llm.apertus import local_apertus_infer

# Mapping from API model names to local Hugging Face model names
API_TO_LOCAL_MODEL = {
    "swiss-ai/apertus-8b-instruct": "swiss-ai/Apertus-8B-2509",
    "swiss-ai/apertus-70b-instruct": "swiss-ai/Apertus-70B-2509",
}

@pytest.mark.slow
@pytest.mark.timeout(120)
@pytest.mark.parametrize("api_model_id", [
    "swiss-ai/apertus-8b-instruct",
    "swiss-ai/apertus-70b-instruct",
])
def test_local_apertus(api_model_id):
    """Test a locally installed Apertus LLM for multiple models."""
    local_model_id = API_TO_LOCAL_MODEL.get(api_model_id, api_model_id)
    prompt = "Give me a brief explanation of gravity in simple terms."
    device = "cuda" if os.environ.get("CUDA_VISIBLE_DEVICES") else "cpu"
    response = local_apertus_infer(local_model_id, prompt, device=device)
    assert response is not None and len(str(response)) > 0
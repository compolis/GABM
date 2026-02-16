"""
This script demonstrates how to use the Apertus-8B-2509 model from the Hugging Face Transformers library. It loads the model and tokenizer, prepares a prompt, generates a response, and prints the output.
To run this script, ensure you have the `transformers` library installed and access to the specified model. You can install the library using pip:
    pip install transformers
Adjust the `device` variable to "cuda" if you have a compatible GPU for faster inference.
"""
# Metadata
__author__ = ["Andy Turner <agdturner@gmail.com>"]
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2026 GABM contributors, University of Leeds"


from transformers import AutoModelForCausalLM, AutoTokenizer

def download_apertus_model(model_name: str):
    """
    Downloads and caches the specified Apertus model and tokenizer using Hugging Face Transformers.
    Args:
        model_name (str): The Hugging Face model name to download (e.g., 'swiss-ai/apertus-70b-instruct').
    """
    from transformers import AutoModelForCausalLM, AutoTokenizer
    print(f"Downloading model and tokenizer for: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    print("Download complete. Model and tokenizer are now cached locally.")

def local_apertus_infer(model_name: str, prompt: str, device: str = "cpu", cache: dict = None, cache_path: str = None, max_new_tokens: int = 32768):
    """
    Run local inference with an Apertus model, optionally caching the response.
    Args:
        model_name (str): Hugging Face model name (e.g., 'swiss-ai/Apertus-8B-2509').
        prompt (str): The prompt to send.
        device (str): 'cpu' or 'cuda'.
        cache (dict, optional): In-memory cache to use.
        cache_path (str, optional): Path to pickle file for caching.
        max_new_tokens (int): Maximum tokens to generate.
    Returns:
        str: The generated response text.
    """
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import pickle
    messages_think = [{"role": "user", "content": prompt}]
    cache_key = (model_name, prompt)
    # Check cache
    if cache is not None and cache_key in cache:
        return cache[cache_key]
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
    text = tokenizer.apply_chat_template(
        messages_think,
        tokenize=False,
        add_generation_prompt=True,
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    generated_ids = model.generate(**model_inputs, max_new_tokens=max_new_tokens)
    output_ids = generated_ids[0][len(model.inputs_ids[0]) :]
    response = tokenizer.decode(output_ids, skip_special_tokens=True)
    # Cache response
    if cache is not None:
        cache[cache_key] = response
        if cache_path:
            try:
                with open(cache_path, "wb") as f:
                    pickle.dump(cache, f)
            except Exception as e:
                print(f"Failed to write cache: {e}")
    return response
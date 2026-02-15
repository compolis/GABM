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

model_name = "swiss-ai/Apertus-8B-2509"
#device = "cuda"  # for GPU usage or "cpu" for CPU usage
device = "cpu"  # for GPU usage or "cpu" for CPU usage

# load the tokenizer and the model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
).to(device)

# prepare the model input
prompt = "Give me a brief explanation of gravity in simple terms."
messages_think = [
    {"role": "user", "content": prompt}
]

text = tokenizer.apply_chat_template(
    messages_think,
    tokenize=False,
    add_generation_prompt=True,
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

# Generate the output
generated_ids = model.generate(**model_inputs, max_new_tokens=32768)

# Get and decode the output
output_ids = generated_ids[0][len(model_inputs.input_ids[0]) :]
print(tokenizer.decode(output_ids, skip_special_tokens=True))
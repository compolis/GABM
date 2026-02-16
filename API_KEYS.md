# API Key Setup

You need a `data/api_key.csv` file with your API keys. This file is not included in the repository for security reasons.

> **Security Warning:** Never commit your API keys or other secrets to the repository. The `.gitignore` file is configured to exclude `data/api_key.csv` and other sensitive files from version control. Always keep your keys private and secure.

Create `data/api_key.csv` yourself in the following CSV format:

## How to Obtain API Keys

You must sign up with each LLM provider to obtain an API key:

- **OpenAI:** Go to [platform.openai.com/signup](https://platform.openai.com/signup) and create an account. After logging in, visit [API Keys](https://platform.openai.com/api-keys) to generate a key. Use `openai` as the API name.
- **DeepSeek:** Register at [deepseek.com](https://deepseek.com/) and follow their documentation to obtain an API key. Use `deepseek` as the API name.
- **GenAI (Google):** Go to [makersuite.google.com](https://makersuite.google.com/) and sign in with your Google account. Follow instructions to get an API key. Use `genai` as the API name.
- **PublicAI (Apertus):** Sign up at [publicai.co](https://publicai.co/) to get your API key. Use `publicai` as the API name.

Add each key to your `data/api_key.csv` file as shown below:

```
openai,sk-...
deepseek,sk-...
genai,YOUR_GOOGLE_KEY
publicai,YOUR_PUBLICAI_KEY
```

The syntax requirements for the `data/api_key.csv` file is strict. Each entry should be on a new line, the API names `openai`, `deepseek`, `genai` and `publicai` must be exactly as shown and there should be nothing but a comma character `,` separating the API name and the API key. Everything is case sensitive. 

The `api_key.csv` file must be stored in the `data/` directory.


## Quick Setup

To quickly initialize your environment, test your API keys, and generate model lists and caches for all supported LLMs, use the provided setup utility:

```bash
make setup-llms
```

This will:
- Check for expected API keys (OpenAI, GenAI, DeepSeek, PublicAI)
- Test each key with a default prompt and model
- If provided with a valid API key and the services work expect:
  - `data\llm\` directories to be populated with
    - `models.json` and `models.txt` files for each LLM with detailing what LLM models are available for each service
    - Initialize response caches (`prompt_response_cache.pkl`) for the test prompts sent to the default model of each service.
- Log files are created to diagnose problems if something does not work, for example if the `api_key.csv` file is missing or not found or badly formatted, and if there are any issues with accessing the LLM services, such as problems with the service or the API keys provided.
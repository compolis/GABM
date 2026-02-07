# API Key Setup

You need a `data/api_key.csv` file with your API keys. This file is not included in the repository for security reasons.

> **Security Warning:** Never commit your API keys or other secrets to the repository. The `.gitignore` file is configured to exclude `data/api_key.csv` and other sensitive files from version control. Always keep your keys private and secure.

Create `data/api_key.csv` yourself in the following CSV format:

```
api,key
openai,sk-...
deepseek,sk-...
genai,YOUR_GOOGLE_KEY
```

The syntax requirements for the `data/api_key.csv` file is strict. Each entry should be on a new line, the API names "openai", "deepseek" and "genai" must be exactly as shown and there should be nothing but a comma character "," separating the API name and the API key. Everything is case sensitive. 

The `api_key.csv` file must be stored in the `data/` directory.

## Quick Setup

To quickly initialize your environment, test your API keys, and generate model lists and caches for all supported LLMs, use the provided setup utility:

```bash
make setup-llms
```

This will:
- Check for expected API keys (OpenAI, GenAI, DeepSeek)
- Test each key with a default prompt and model
- If provided with a valid API key and the services work expect:
  - `data\llm\` directories to be populated with
    - `models.json` and `models.txt` files for each LLM with detailing what LLM models are available for each service
    - Initialize response caches (`cache.pkl`) for the test `Hello` prompts sent to the default model of each service.
- Log files are created to diagnose problems if something does not work, for example if the `api_key.csv` file is missing or not found or badly formatted, and if there are any issues with accessing the LLM services, such as problems with the service or the API keys provided.
# Local LLM Setup Guide

This guide describes how to run GABM locally using the  OpenAI-compatible inference engine [Ollama](https://ollama.com/).

## 1) Install local LLM dependencies

```bash
pip install gabm[llm-local]
```

or:

```bash
pip install -r requirements-local-llm.txt
```

## 2) Start a local OpenAI-compatible server

Example with Ollama:

```bash
ollama pull qwen3:8b
ollama serve
```

Sanity check from another terminal:

```bash
curl http://127.0.0.1:11434/v1/models
```

If the endpoint returns model JSON, the server is ready.

## 3) Run the chat example against your local endpoint

Set `OPENAI_BASE_URL` to your local endpoint and provide an API key/token string
accepted by the endpoint (for Ollama, a placeholder token such as `ollama` is
typically sufficient):

```bash
OPENAI_BASE_URL=http://127.0.0.1:11434/v1 \
PYTHONPATH=src python3 src/gabm/examples/chat/sim.py \
  --llm-service openai \
  --model qwen3:8b \
  --api-key ollama \
  --seed 42 \
  --year 2026
```

The same `OPENAI_BASE_URL` pattern also applies to:

- `src/gabm/examples/chat/ensembles/similarity_sweep.py`
- `src/gabm/examples/chat_opinion/sim.py`
- `src/gabm/examples/chat_opinion/ensembles/similarity_sweep.py`

## 4) Optional: keep local settings in environment variables

For repeated runs, export the endpoint once:

```bash
export OPENAI_BASE_URL=http://127.0.0.1:11434/v1
```

Then use your usual commands while passing a local model name and API key.

## 5) Runtime planning and scaling guidance

For runtime estimation, benchmark logging, and guidance on whether to run
locally, on hosted APIs, on HPC, or on cloud infrastructure, see:

- [experiments/Runtime_Planning_and_Benchmarking.md](./experiments/Runtime_Planning_and_Benchmarking.md)

## Notes

- `OPENAI_BASE_URL` is optional. If omitted, the OpenAI SDK default endpoint is
  used.
- In typical local setups, Ollama runs as a single daemon process. If another
  long-running Ollama workload is active, wait for it to complete before
  starting a new one in the same user/session environment.
- For Hugging Face-hosted local model workflows, see [HUGGING_FACE.md](../../HUGGING_FACE.md).

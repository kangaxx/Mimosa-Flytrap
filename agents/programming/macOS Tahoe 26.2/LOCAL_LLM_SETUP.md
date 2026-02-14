Local LLM (Ollama) + deepseek-r1:8b — macOS Tahoe 26.2

This guide covers installing and running a local LLM via Ollama and using
deepseek-r1:8b for embeddings on macOS (Tahoe 26.2). It assumes you already
have Ollama and deepseek-r1:8b downloaded, but includes verification and
helpful commands.

Prerequisites
- Homebrew (recommended)
- Ollama installed and reachable via `ollama` CLI
- deepseek embedding service or local endpoint running (set `DEEPSEEK_API_URL`)
- Python 3.11+ and `pip`

Quick overview
1. Install system deps (Homebrew + python)
2. Pull/start Ollama model(s)
3. Configure environment (`.env`) with Ollama + deepseek settings
4. Create Python venv and install packages
5. Run tests and start the programming agent

Commands

1) Install Homebrew & Python (if needed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew update
brew install python@3.11 curl
```

2) Verify `ollama` and pull models

```bash
ollama --version
# pull a model you want to use for completions (example: llama2-13b-chat or deepseek-r1:8b)
ollama pull llama2-13b-chat
# or deepseek-r1:8b , DeepSeek-R1:8B is better suited for Chinese programming environments.
# ensure your model for completions is ready; list models:
ollama list
```

3) Configure environment (.env)

Copy the example and edit values:

```bash
cd agents/programming/macOS\ Tahoe\ 26.2
cp .env.example .env
# Edit .env and set: OLLAMA_BASE_URL, OLLAMA_MODEL, DEEPSEEK_API_URL, DEEPSEEK_API_KEY
# Ensure DEEPSEEK_MODEL=deepseek-r1:8b (the repo examples use this)
```

You can run the included sync script to append missing variables and update
`DEEPSEEK_MODEL` to the example value (it backs up `.env` first):

```bash
chmod +x sync_env.sh
./sync_env.sh
```

4) Create venv and install Python deps

```bash
chmod +x setup_environment.sh
./setup_environment.sh
```

5) Start Ollama with OpenAI-compatible layer (helper script)

```bash
chmod +x start_ollama_openai.sh
./start_ollama_openai.sh
# or run directly: ollama serve --openai --host 127.0.0.1 --port 11434
```

6) Test the OpenAI-style endpoint

```bash
curl -sS http://127.0.0.1:11434/v1/models | jq .
```

7) Verify deepseek embeddings (example HTTP call)

```bash
curl -sS -X POST "$DEEPSEEK_API_URL" \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-r1:8b","input":["hello world"]}' | jq .
```

8) Start the programming agent (interactive)

```bash
chmod +x start_programming_agent.sh
./start_programming_agent.sh
```

9) Run the included test script

```bash
chmod +x test_setup.sh
./test_setup.sh
```

Notes & tips
- If `curl` or `jq` are missing, install via Homebrew: `brew install curl jq`.
- If Ollama fails to expose `/v1/models`, try different serve flags or check
  `ollama_serve.log` created by `start_ollama_openai.sh`.
- For production or long-running usage consider running Ollama under `launchctl`
  or `brew services` to manage restarts.
- Keep API keys out of source control. Ensure `.env` is excluded by `.gitignore`.

Troubleshooting
- `permission denied` on scripts: run `chmod +x <script>`.
- `connection refused` to `http://127.0.0.1:11434`: ensure Ollama is running and
  check firewall / port conflicts.
- deepseek errors: verify `DEEPSEEK_API_URL` and `DEEPSEEK_API_KEY` are correct and
  that the service accepts `deepseek-r1:8b` as model identifier.

References
- See `start_ollama_openai.sh`, `run_programming_agent.py`, and `sync_env.sh` in
  this folder for helper automation.

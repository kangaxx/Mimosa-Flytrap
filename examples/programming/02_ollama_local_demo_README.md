02_ollama_local_demo — README

Purpose
- A small demo showing how to call a local Ollama OpenAI-compatible HTTP
  endpoint to request chat completions (e.g., generate code). The demo script
  is `02_ollama_local_demo.py`.

Quick start
1. Ensure Ollama is running with an OpenAI-compatible endpoint (default:
   `http://127.0.0.1:11434`). See `start_ollama_openai.sh` in the repo for a helper.
2. (Optional) Set environment variables:

```bash
export OLLAMA_BASE_URL=http://127.0.0.1:11434
export OLLAMA_API_KEY=ollama
export DEEPSEEK_MODEL=deepseek-r1:8b
```

3. Run the demo (uses `requests` if available, otherwise falls back to `curl`):

```bash
python examples/programming/02_ollama_local_demo.py --prompt "生成一份网页爬虫Python代码"
```

Options
- `--model` : model id to request (default from `DEEPSEEK_MODEL` env)
- `--temperature` : sampling temperature (default 0.7)
- `--max-tokens` : max tokens to request (default 2000)
- `--use-curl` : force use of `curl` instead of `requests`

Dependencies
- Python 3.8+
- `requests` (optional; if missing the script will call `curl`)

Example curl equivalent

```bash
curl http://127.0.0.1:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ollama" \
  -d '{"model":"deepseek-r1:8b","messages":[{"role":"user","content":"生成一份网页爬虫Python代码"}],"temperature":0.7,"max_tokens":2000}'
```

Notes
- The script prints the `choices[0].message.content` (or `choices[0].text`) when present.
- Be careful executing generated code; review and run in a safe environment.

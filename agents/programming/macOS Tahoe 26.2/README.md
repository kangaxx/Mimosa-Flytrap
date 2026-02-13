MacOS Tahoe (26.2) — Ollama + deepseek-r1 setup

This folder contains macOS-specific helper scripts and an example agent configured
to run with Ollama (local LLM) and deepseek-r1 embeddings.

Files:
- .env.example — sample environment variables
- install_dependencies.sh — install Homebrew deps (if available) and helpful tools
- setup_ollama.sh — guidance + helper commands to install/start Ollama on macOS
- setup_environment.sh — create Python venv and install Python deps
- test_setup.sh — sanity checks (python, venv, ollama, minimal run)
- requirements.txt — Python packages for the agent
- run_langchain_agent.py — example LangChain agent integrated with Ollama and a
  placeholder deepseek-r1 embedding client
- QUICKSTART.md — minimal step-by-step to get started

Security
- Do NOT commit real API keys to git. Use the `.env` file and keep it out of
  source control.

Notes
- `deepseek-r1` client is represented here by a minimal HTTP wrapper. Replace
  with an official SDK if/when available.

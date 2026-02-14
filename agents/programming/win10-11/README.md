Windows 11 — Ollama + deepseek-r1 setup

This folder contains Windows 11 (PowerShell) helper scripts and an example
agent configured to run with Ollama (local LLM) and deepseek-r1 embeddings.

Files:
- .env.example — sample environment variables
- QUICKSTART.md — quick start with PowerShell commands
- requirements.txt — Python dependencies
- install_dependencies.ps1 — instructs/attempts to install Python via winget
- setup_ollama.ps1 — guidance to install/check Ollama on Windows
- setup_environment.ps1 — create virtualenv and install Python packages
- test_setup.ps1 — sanity checks and example run
- start_programming_agent.ps1 — activates venv and runs the agent
- run_programming_agent.py — example interactive programming agent

Security
- Keep API keys out of version control. Copy `.env.example` to `.env` and
  populate secrets there.

Notes
- Scripts use PowerShell Core or Windows PowerShell. Run them from an
  elevated terminal if installing system packages.

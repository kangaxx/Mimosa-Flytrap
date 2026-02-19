VisaBot — macOS Tahoe 26.2

This folder provides a runnable VisaBot environment for macOS, with scripts to:
- install system dependencies,
- create a Python virtual environment,
- validate setup,
- and start VisaBot.

Files:
- .env.example — sample environment variables
- requirements.txt — Python dependencies
- install_dependencies.sh — install Homebrew dependencies
- setup_environment.sh — create venv and install Python deps
- test_setup.sh — run sanity checks
- start_visabot.sh — start VisaBot with venv activation
- run_visabot.py — VisaBot runtime (supports ollama/openai)
- QUICKSTART.md — step-by-step operations guide

Security:
- Do not commit real API keys.
- Keep credentials only in `.env`.

VisaBot — macOS Tahoe 26.2

This folder provides a runnable VisaBot environment for macOS, with scripts to:
- install system dependencies,
- create a Python virtual environment,
- install AutoGen (pyautogen) and Playwright,
- install Playwright browsers,
- validate setup,
- and start VisaBot.

Files:
- .env.example — sample environment variables
- requirements.txt — Python dependencies
- install_dependencies.sh — install Homebrew dependencies
- setup_environment.sh — create venv and install Python deps
- sync_env.sh — sync missing keys from .env.example into .env (keeps your values)
- activate_venv.sh — convenience script (must be sourced) to activate .venv
- test_setup.sh — run sanity checks
- start_visabot.sh — start VisaBot with venv activation
- run_visabot.py — VisaBot runtime (supports ollama/openai)
- QUICKSTART.md — step-by-step operations guide

Notes:
- Playwright downloads browser binaries on first setup. You can control which browsers are installed via:
	- `PLAYWRIGHT_BROWSERS=chromium` (default)
	- `PLAYWRIGHT_BROWSERS=all`

Security:
- Do not commit real API keys.
- Keep credentials only in `.env`.

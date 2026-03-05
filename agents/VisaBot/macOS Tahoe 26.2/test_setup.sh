#!/usr/bin/env bash
set -euo pipefail

echo "==> VisaBot setup sanity checks"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found"
  exit 1
fi

if [ -f .venv/bin/activate ]; then
  echo "Virtualenv present"
else
  echo "Virtualenv not found. Run ./setup_environment.sh"
  exit 1
fi

source .venv/bin/activate
python -c "import requests; print('requests OK')"
python -c "import autogen_agentchat; print('autogen_agentchat OK')"
python -c "import autogen_core; print('autogen_core OK')"
python -c "from playwright.sync_api import sync_playwright; print('playwright OK')"

if [ "${RUN_LLM_SMOKE_TEST:-0}" = "1" ]; then
  echo "Running optional LLM smoke test (RUN_LLM_SMOKE_TEST=1)"
  python run_visabot.py --question "请用三句话介绍你能做什么" >/dev/null
else
  echo "Skipping LLM smoke test. Set RUN_LLM_SMOKE_TEST=1 to enable."
fi

echo "All checks passed"

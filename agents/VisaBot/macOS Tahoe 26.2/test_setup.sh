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
python -c "import requests; print('Python deps OK')"
python run_visabot.py --question "请用三句话介绍你能做什么" >/dev/null

echo "All checks passed"

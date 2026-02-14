#!/usr/bin/env pwsh
Write-Host "==> Basic sanity checks (Windows)"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "python not found. Run setup_environment.ps1 or install Python."
    exit 1
}

if (-not (Test-Path .venv\Scripts\Activate.ps1)) {
    Write-Warning "Virtualenv not present. Run .\setup_environment.ps1"
} else {
    Write-Host "Virtualenv present"
}

if (Get-Command ollama -ErrorAction SilentlyContinue) {
    Write-Host "ollama found"
} else {
    Write-Warning "ollama not found — ensure Ollama is installed and running"
}

Write-Host "Running minimal agent test"
python run_programming_agent.py --model-type ollama --prompt "Say hello from Windows"

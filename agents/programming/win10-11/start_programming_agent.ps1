#!/usr/bin/env pwsh
Write-Host "Activating virtualenv (if present) and starting programming agent"
if (Test-Path .\.venv\Scripts\Activate.ps1) {
    & .\.venv\Scripts\Activate.ps1
} else {
    Write-Warning ".venv not found. Run .\setup_environment.ps1 first."
}

Write-Host "Starting agent (interactive). Use -Auto to allow auto execution."
python run_programming_agent.py $args

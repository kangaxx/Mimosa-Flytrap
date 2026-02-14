#!/usr/bin/env pwsh
Write-Host "==> Setup/check Ollama on Windows"

if (Get-Command ollama -ErrorAction SilentlyContinue) {
    Write-Host "ollama found"
    & ollama status
} else {
    Write-Warning "ollama not found. You can install via the official installer from https://ollama.com/docs"
    Write-Host "If you have winget you may try: winget install Ollama.Ollama";
}

Write-Host "Pull models with: ollama pull <model-name>"

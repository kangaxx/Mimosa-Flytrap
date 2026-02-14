# Quickstart — Windows 11 (Ollama + deepseek-r1)

1. Open PowerShell (recommended: run as Administrator when installing).

2. Install Python (if missing) using `winget` (or from python.org):

```powershell
winget install --id Python.Python.3
```

3. Install system dependencies (optional):

```powershell
.\install_dependencies.ps1
```

4. Install or start Ollama (see `setup_ollama.ps1`).

5. Create Python environment and install packages:

```powershell
.\setup_environment.ps1
```

6. Copy `.env.example` to `.env` and fill API keys.

```powershell
Copy-Item .env.example .env
# Edit .env in Notepad or VS Code
notepad .env
```

7. Run quick test:

```powershell
.\test_setup.ps1
```

8. Start the interactive programming agent:

```powershell
.\start_programming_agent.ps1
```

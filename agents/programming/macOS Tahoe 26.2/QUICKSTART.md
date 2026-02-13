# Quickstart — macOS Tahoe (Ollama + deepseek-r1)

1. Install Homebrew (if not present):

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install system dependencies (will try `brew`):

```bash
chmod +x install_dependencies.sh
./install_dependencies.sh
```

3. Install Ollama (see `setup_ollama.sh`) and start the service.

4. Create Python environment and install packages:

```bash
chmod +x setup_environment.sh
./setup_environment.sh
```

5. Copy `.env.example` to `.env` and fill API keys and endpoints.

6. Run the quick test:

```bash
chmod +x test_setup.sh
./test_setup.sh
```

7. Run the example agent:

```bash
python run_langchain_agent.py --model-type ollama --prompt "Say hello"
```

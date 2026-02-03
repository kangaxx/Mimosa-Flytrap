# Quick Start Guide - Ubuntu 22.04 LangChain Setup

## 🚀 5-Minute Setup

Get up and running with LangChain, Ollama, and GPT-3.5 in minutes!

### Step 1: Run Automated Setup

```bash
cd agents/programming/ubuntu\ 22.04\ LTS\ \(ali\ server\)/

# Install system dependencies (requires sudo)
sudo ./install_dependencies.sh

# Install and configure Ollama
./setup_ollama.sh

# Set up Python environment and LangChain
./setup_environment.sh
```

### Step 2: Configure API Keys

```bash
# Copy environment template
cp .env.example .env

# Edit with your OpenAI API key
nano .env
# Set: OPENAI_API_KEY=sk-your-actual-key-here
```

### Step 3: Test Your Setup

```bash
# Verify everything is working
./test_setup.sh

# Activate Python environment
source langchain-env/bin/activate
```

### Step 4: Run Your First Agent

```bash
# Using GPT-3.5 (cloud)
python run_langchain_agent.py --model gpt --prompt "What is LangChain?"

# Using Ollama (local)
python run_langchain_agent.py --model ollama --prompt "What is AI?"

# Interactive mode
python run_langchain_agent.py --interactive
```

## 📋 What Gets Installed

- **System Packages**: Python 3.10, build tools, curl, git
- **Ollama**: Local LLM runtime with model(s) of your choice
- **Python Packages**: LangChain, OpenAI SDK, and dependencies
- **Example Scripts**: Ready-to-run AI agent implementations

## 🔑 Getting Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key and add it to your `.env` file

## 🤔 Troubleshooting

### Scripts fail with permission errors
```bash
chmod +x *.sh
```

### Ollama not responding
```bash
# Restart Ollama
ollama serve &
```

### Python packages not found
```bash
source langchain-env/bin/activate
pip install -r requirements.txt
```

### OpenAI API errors
Check that your API key is correct in `.env` and you have credits in your OpenAI account.

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore example use cases and advanced configurations
- Customize the agent script for your specific needs
- Try different Ollama models: `ollama pull mistral`

## 💡 Tips

- **For local-only use**: Skip the OpenAI key and use `--model ollama`
- **For privacy-sensitive data**: Use Ollama models exclusively
- **For best results**: Use GPT-3.5 for complex tasks
- **For speed**: Use smaller Ollama models like mistral

## 🆘 Need Help?

- Check the [full README](README.md) for detailed troubleshooting
- Review the [main FAQ](../../FAQ.md)
- Ensure Ubuntu 22.04 LTS is fully updated

---

**Ready to build AI agents? Let's go! 🚀**

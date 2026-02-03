# Ubuntu 22.04 LTS LangChain Environment Setup Guide

This guide provides comprehensive instructions for setting up a LangChain-based AI agent environment on Ubuntu 22.04 LTS, including local Ollama installation, GPT-3.5 integration, and LLM agent configuration.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Installation](#detailed-installation)
  - [Step 1: System Dependencies](#step-1-system-dependencies)
  - [Step 2: Ollama Installation](#step-2-ollama-installation)
  - [Step 3: Python Environment Setup](#step-3-python-environment-setup)
  - [Step 4: LangChain Installation](#step-4-langchain-installation)
  - [Step 5: Environment Configuration](#step-5-environment-configuration)
- [Configuration](#configuration)
- [Running Your First Agent](#running-your-first-agent)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)

## 🎯 Overview

This setup enables you to:
- Run LLM models locally using Ollama
- Use OpenAI GPT-3.5 for cloud-based inference
- Build AI agents with the LangChain framework
- Switch between local and cloud models seamlessly
- Deploy production-ready AI applications

## ✅ Prerequisites

### System Requirements
- **OS:** Ubuntu 22.04 LTS (Jammy Jellyfish)
- **RAM:** 8GB minimum (16GB recommended for larger models)
- **Disk Space:** 20GB+ free space
- **CPU:** Modern multi-core processor (GPU optional but beneficial)
- **Internet:** Required for initial setup and GPT-3.5 access

### Required Accounts
- OpenAI account with API access (for GPT-3.5)
- GitHub account (for downloading models and tools)

### Knowledge Prerequisites
- Basic Linux command line familiarity
- Basic Python programming knowledge
- Understanding of environment variables

## 🚀 Quick Start

For a rapid setup, run the automated installation scripts:

```bash
# Navigate to this directory
cd examples/programming/ubuntu\ 22.04\ LTS\(阿里服务器\)/

# Run the complete setup (requires sudo)
chmod +x install_dependencies.sh setup_ollama.sh setup_environment.sh
sudo ./install_dependencies.sh
./setup_ollama.sh
./setup_environment.sh

# Configure your environment
cp .env.example .env
# Edit .env with your OpenAI API key

# Test the setup
./test_setup.sh
```

## 📦 Detailed Installation

### Step 1: System Dependencies

Update your system and install required packages:

```bash
# Update package lists
sudo apt update && sudo apt upgrade -y

# Install Python and essential tools
sudo apt install -y python3.10 python3.10-venv python3-pip
sudo apt install -y build-essential curl wget git

# Install additional dependencies
sudo apt install -y libssl-dev libffi-dev python3-dev
sudo apt install -y software-properties-common
```

Or use the provided script:
```bash
sudo ./install_dependencies.sh
```

### Step 2: Ollama Installation

Ollama allows you to run large language models locally on your machine.

#### Manual Installation

```bash
# Download and install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version

# Start Ollama service
ollama serve &

# Pull a model (e.g., Llama 2)
ollama pull llama2

# You can also pull other models
ollama pull mistral
ollama pull codellama
```

#### Using the Installation Script

```bash
./setup_ollama.sh
```

This script will:
- Install Ollama
- Set up the Ollama service
- Download recommended models (llama2, mistral)
- Configure environment variables

### Step 3: Python Environment Setup

Create an isolated Python environment for your LangChain projects:

```bash
# Create a virtual environment
python3 -m venv langchain-env

# Activate the environment
source langchain-env/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

To deactivate the environment later:
```bash
deactivate
```

### Step 4: LangChain Installation

Install LangChain and related packages:

```bash
# Activate your virtual environment first
source langchain-env/bin/activate

# Install core LangChain packages
pip install langchain langchain-community langchain-core

# Install OpenAI integration
pip install langchain-openai openai

# Install Ollama integration
pip install langchain-ollama

# Install additional useful packages
pip install python-dotenv requests tiktoken

# For document processing
pip install pypdf chromadb

# For advanced features
pip install faiss-cpu  # Vector store
pip install sentence-transformers  # Embeddings
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### Step 5: Environment Configuration

Configure your API keys and settings:

```bash
# Copy the example environment file
cp .env.example .env

# Edit with your favorite editor
nano .env  # or vim, code, etc.
```

Add your credentials:
```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# LangChain Configuration
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=  # Optional: for LangSmith tracing

# Agent Configuration
DEFAULT_TEMPERATURE=0.7
MAX_TOKENS=2000
```

## ⚙️ Configuration

### Model Selection

You can choose between local (Ollama) and cloud (GPT-3.5) models:

**For GPT-3.5 (Cloud):**
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)
```

**For Ollama (Local):**
```python
from langchain_community.llms import Ollama

llm = Ollama(
    model="llama2",
    base_url="http://localhost:11434"
)
```

### Available Ollama Models

Popular models you can use locally:

| Model | Size | Use Case | Pull Command |
|-------|------|----------|--------------|
| llama2 | 7B | General purpose | `ollama pull llama2` |
| mistral | 7B | Fast, efficient | `ollama pull mistral` |
| codellama | 7B-34B | Code generation | `ollama pull codellama` |
| llama2:13b | 13B | Better quality | `ollama pull llama2:13b` |
| neural-chat | 7B | Conversational | `ollama pull neural-chat` |

### GPU Acceleration (Optional)

If you have an NVIDIA GPU:

```bash
# Install CUDA toolkit
sudo apt install -y nvidia-cuda-toolkit

# Verify GPU is available
nvidia-smi

# Ollama will automatically use GPU if available
```

## 🎮 Running Your First Agent

### Basic Example

```bash
# Activate your environment
source langchain-env/bin/activate

# Run the example agent
python run_langchain_agent.py
```

### Python Script Example

Create a simple agent:

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the model
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7
)

# Create a prompt template
prompt = ChatPromptTemplate.from_template(
    "You are a helpful AI assistant. {question}"
)

# Create a chain
chain = LLMChain(llm=llm, prompt=prompt)

# Run the agent
response = chain.run(question="What is LangChain?")
print(response)
```

## ✅ Verification

Test your setup with the verification script:

```bash
./test_setup.sh
```

This will check:
- ✓ Python installation
- ✓ Virtual environment
- ✓ Required packages
- ✓ Ollama service status
- ✓ Model availability
- ✓ API key configuration
- ✓ Network connectivity

### Manual Verification

```bash
# Check Python version
python3 --version

# Check Ollama
ollama list

# Test Ollama locally
ollama run llama2 "Hello, world!"

# Check installed Python packages
pip list | grep langchain
```

## 🔧 Troubleshooting

### Common Issues

#### Issue: Ollama service not running
```bash
# Start Ollama service
ollama serve &

# Or as a systemd service
sudo systemctl start ollama
sudo systemctl enable ollama
```

#### Issue: Python import errors
```bash
# Ensure virtual environment is activated
source langchain-env/bin/activate

# Reinstall packages
pip install -r requirements.txt
```

#### Issue: OpenAI API errors
```bash
# Verify API key is set
echo $OPENAI_API_KEY

# Test API connectivity
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

#### Issue: Out of memory with Ollama
```bash
# Use smaller models
ollama pull llama2:7b-chat

# Or set memory limit
OLLAMA_MAX_LOADED_MODELS=1 ollama serve
```

#### Issue: Port 11434 already in use
```bash
# Check what's using the port
sudo lsof -i :11434

# Kill the process or change Ollama port
OLLAMA_HOST=0.0.0.0:11435 ollama serve
```

### Log Files

Check logs for detailed error information:

```bash
# Ollama logs
journalctl -u ollama -f

# Python script logs
python run_langchain_agent.py --verbose

# System logs
tail -f /var/log/syslog
```

## 🚀 Advanced Usage

### Using Multiple Models

Switch between models dynamically:

```python
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama

# Cloud model for complex tasks
gpt_llm = ChatOpenAI(model="gpt-3.5-turbo")

# Local model for privacy-sensitive tasks
local_llm = Ollama(model="llama2")

# Use based on requirements
if sensitive_data:
    response = local_llm.invoke(prompt)
else:
    response = gpt_llm.invoke(prompt)
```

### Retrieval-Augmented Generation (RAG)

Build a RAG system:

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

# Load and split documents
documents = load_documents()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
texts = text_splitter.split_documents(documents)

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(texts, embeddings)

# Create QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(),
    retriever=vectorstore.as_retriever()
)
```

### Agent with Tools

Create an agent with custom tools:

```python
from langchain.agents import initialize_agent, Tool
from langchain.tools import DuckDuckGoSearchRun

# Define tools
search = DuckDuckGoSearchRun()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Search the web for current information"
    )
]

# Initialize agent
agent = initialize_agent(
    tools=tools,
    llm=ChatOpenAI(),
    agent="zero-shot-react-description",
    verbose=True
)

# Run agent
result = agent.run("What's the latest news about AI?")
```

### Production Deployment

For production use:

```bash
# Use systemd for Ollama
sudo systemctl enable ollama
sudo systemctl start ollama

# Set up nginx reverse proxy for API
sudo apt install nginx

# Configure log rotation
sudo logrotate -f /etc/logrotate.conf

# Set up monitoring
pip install prometheus-client
```

## 📚 Additional Resources

### Documentation
- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Documentation](https://ollama.ai/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)

### Model Cards
- [Llama 2 Model Card](https://huggingface.co/meta-llama/Llama-2-7b)
- [Mistral Model Card](https://huggingface.co/mistralai/Mistral-7B-v0.1)

### Tutorials
- [LangChain Quickstart](https://python.langchain.com/docs/get_started/quickstart)
- [Building RAG Applications](https://python.langchain.com/docs/use_cases/question_answering/)
- [Creating Custom Agents](https://python.langchain.com/docs/modules/agents/)

### Community
- [LangChain Discord](https://discord.gg/langchain)
- [Ollama Discord](https://discord.gg/ollama)
- [Stack Overflow - LangChain](https://stackoverflow.com/questions/tagged/langchain)

## 🔐 Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Local Models**: Keep Ollama models updated for security patches
3. **Network**: Use HTTPS for production deployments
4. **Access Control**: Implement authentication for API endpoints
5. **Data Privacy**: Use local models for sensitive data

## 📝 License

This setup guide is part of the Mimosa-Flytrap project and follows the same MIT License.

## 🤝 Contributing

Found an issue or want to improve this guide? Please:
1. Open an issue describing the problem
2. Submit a pull request with improvements
3. Share your experience and tips

---

**Last Updated:** 2026-02-03  
**Tested On:** Ubuntu 22.04 LTS (Jammy Jellyfish)  
**LangChain Version:** 0.1.x+  
**Ollama Version:** 0.1.x+

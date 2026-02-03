# Installation Guide

This guide provides instructions for setting up AI agents in various environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Docker Installation](#docker-installation)
- [Cloud Deployment](#cloud-deployment)
- [Environment-Specific Guides](#environment-specific-guides)

## Prerequisites

### General Requirements

- Python 3.8 or higher
- pip or conda package manager
- Git
- 4GB+ RAM (8GB+ recommended)
- GPU (optional but recommended for image/video processing)

### API Keys (as needed)

- OpenAI API key (for GPT models)
- Anthropic API key (for Claude models)
- Hugging Face API key (for various models)
- Google Cloud credentials (for Google AI services)
- AWS credentials (for AWS AI services)

## Local Development Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/kangaxx/Mimosa-Flytrap.git
cd Mimosa-Flytrap
```

### Step 2: Create Virtual Environment

**Using venv:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Using conda:**
```bash
conda create -n mimosa-flytrap python=3.10
conda activate mimosa-flytrap
```

### Step 3: Install Dependencies

For all agents:
```bash
pip install -r requirements.txt
```

For specific categories:
```bash
# Programming agents
pip install -r agents/programming/requirements.txt

# Document processing
pip install -r agents/document-processing/requirements.txt

# Image processing
pip install -r agents/image-processing/requirements.txt
```

### Step 4: Configure Environment

Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
HUGGINGFACE_API_KEY=your_hf_key
```

### Step 5: Verify Installation

```bash
python verify_setup.py
```

## Docker Installation

### Using Docker Compose

```bash
# Build and start all services
docker-compose up -d

# Start specific agent category
docker-compose up -d programming-agents
```

### Using Dockerfile

```bash
# Build the image
docker build -t mimosa-flytrap .

# Run a container
docker run -it --rm \
  -v $(pwd):/workspace \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  mimosa-flytrap
```

## Cloud Deployment

### AWS

```bash
# Using AWS Elastic Beanstalk
eb init -p python-3.10 mimosa-flytrap
eb create mimosa-flytrap-env
eb deploy
```

### Google Cloud Platform

```bash
# Using Cloud Run
gcloud run deploy mimosa-flytrap \
  --source . \
  --platform managed \
  --region us-central1
```

### Azure

```bash
# Using Azure Container Instances
az container create \
  --resource-group mimosa-flytrap-rg \
  --name mimosa-flytrap \
  --image mimosa-flytrap:latest
```

## Environment-Specific Guides

### Ubuntu 22.04 LTS - LangChain Setup

For a complete guide to setting up LangChain with Ollama and GPT-3.5 on Ubuntu 22.04 LTS:

📚 **[Ubuntu 22.04 LTS LangChain Environment Setup Guide](ubuntu-22.04-langchain-setup/README.md)**

This comprehensive guide includes:
- System dependencies installation
- Ollama local LLM setup
- LangChain framework configuration
- OpenAI GPT-3.5 integration
- Automated setup scripts
- Example AI agent implementation

### GPU Support

For CUDA support (NVIDIA GPUs):
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

For Apple Silicon (M1/M2):
```bash
pip install torch torchvision torchaudio
# PyTorch will automatically use Metal Performance Shaders
```

### Jupyter Notebook

```bash
pip install jupyter
jupyter notebook
```

### VS Code Integration

1. Install Python extension
2. Select the virtual environment
3. Configure `.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.envFile": "${workspaceFolder}/.env"
}
```

## Troubleshooting

### Common Issues

**Issue: Import errors**
- Solution: Ensure virtual environment is activated
- Solution: Run `pip install -r requirements.txt`

**Issue: API key errors**
- Solution: Verify `.env` file exists and contains valid keys
- Solution: Check environment variables are loaded

**Issue: GPU not detected**
- Solution: Install CUDA toolkit
- Solution: Install correct PyTorch version for your CUDA version

**Issue: Memory errors**
- Solution: Use smaller batch sizes
- Solution: Enable model quantization
- Solution: Use CPU fallback

### Getting Help

- Check [FAQ](../FAQ.md)
- Review agent-specific documentation
- Check the issue tracker
- Join community discussions

## Next Steps

After installation:
1. Review [Configuration Guide](../configuration/README.md)
2. Explore [Examples](../../examples/)
3. Try your first agent script
4. Read best practices documentation

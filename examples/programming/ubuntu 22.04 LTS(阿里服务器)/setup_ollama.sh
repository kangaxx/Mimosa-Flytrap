#!/bin/bash

###############################################################################
# Ollama Installation and Configuration Script
# 
# This script installs Ollama and downloads recommended LLM models for
# local inference.
#
# Usage: ./setup_ollama.sh
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Ollama Installation Script${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if Ollama is already installed
if command -v ollama &> /dev/null; then
    echo -e "${YELLOW}Ollama is already installed.${NC}"
    ollama --version
    read -p "Do you want to reinstall? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping Ollama installation."
    else
        echo -e "${YELLOW}Reinstalling Ollama...${NC}"
        curl -fsSL https://ollama.com/install.sh | sh
    fi
else
    echo -e "${YELLOW}Installing Ollama...${NC}"
    curl -fsSL https://ollama.com/install.sh | sh
fi

echo ""
echo -e "${GREEN}Ollama installed successfully!${NC}"
ollama --version

# Start Ollama service
echo ""
echo -e "${YELLOW}Starting Ollama service...${NC}"

# Check if systemd service exists
if systemctl list-unit-files | grep -q ollama.service; then
    sudo systemctl start ollama
    sudo systemctl enable ollama
    echo -e "${GREEN}Ollama service started and enabled.${NC}"
else
    # Start Ollama in background
    echo -e "${YELLOW}Starting Ollama server in background...${NC}"
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
    echo -e "${GREEN}Ollama server started.${NC}"
fi

# Wait for Ollama to be ready
echo -e "${YELLOW}Waiting for Ollama to be ready...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${GREEN}Ollama is ready!${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}Error: Ollama failed to start within 30 seconds${NC}"
        exit 1
    fi
    sleep 1
done

# Download recommended models
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Downloading Recommended Models${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

echo -e "${BLUE}Available models to download:${NC}"
echo "  1. llama2 (7B) - General purpose, good balance"
echo "  2. mistral (7B) - Fast and efficient"
echo "  3. codellama (7B) - Optimized for code"
echo "  4. Skip model download"
echo ""

read -p "Select models to download (e.g., 1 2 3 or 1,2,3): " model_choice

# Parse user input
IFS=', ' read -ra MODELS <<< "$model_choice"

for model in "${MODELS[@]}"; do
    case $model in
        1)
            echo ""
            echo -e "${YELLOW}Downloading llama2...${NC}"
            ollama pull llama2
            echo -e "${GREEN}llama2 downloaded successfully!${NC}"
            ;;
        2)
            echo ""
            echo -e "${YELLOW}Downloading mistral...${NC}"
            ollama pull mistral
            echo -e "${GREEN}mistral downloaded successfully!${NC}"
            ;;
        3)
            echo ""
            echo -e "${YELLOW}Downloading codellama...${NC}"
            ollama pull codellama
            echo -e "${GREEN}codellama downloaded successfully!${NC}"
            ;;
        4)
            echo "Skipping model download."
            ;;
        *)
            echo -e "${RED}Invalid choice: $model${NC}"
            ;;
    esac
done

# List installed models
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Installed Models${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
ollama list

# Test Ollama
echo ""
echo -e "${YELLOW}Testing Ollama installation...${NC}"

if ollama list | grep -q -E 'llama2|mistral|codellama'; then
    echo ""
    read -p "Would you like to test a model? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Get first available model
        MODEL=$(ollama list | tail -n +2 | head -n 1 | awk '{print $1}')
        echo -e "${BLUE}Testing with model: $MODEL${NC}"
        echo ""
        echo "Prompt: Say 'Hello, I am working!' in one sentence."
        echo ""
        ollama run $MODEL "Say 'Hello, I am working!' in one sentence." --verbose false
        echo ""
    fi
fi

# Configure environment variables
echo ""
echo -e "${YELLOW}Configuring environment variables...${NC}"

# Add to bashrc if not already present
if ! grep -q "OLLAMA_BASE_URL" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# Ollama Configuration" >> ~/.bashrc
    echo "export OLLAMA_BASE_URL=http://localhost:11434" >> ~/.bashrc
    echo "export OLLAMA_HOST=0.0.0.0:11434" >> ~/.bashrc
    echo -e "${GREEN}Environment variables added to ~/.bashrc${NC}"
else
    echo -e "${YELLOW}Environment variables already configured.${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Ollama Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Ollama is running and ready to use."
echo ""
echo -e "Useful commands:"
echo -e "  ${YELLOW}ollama list${NC}          - List installed models"
echo -e "  ${YELLOW}ollama pull <model>${NC}  - Download a new model"
echo -e "  ${YELLOW}ollama run <model>${NC}   - Run a model interactively"
echo -e "  ${YELLOW}ollama serve${NC}         - Start Ollama server"
echo ""
echo -e "Next step:"
echo -e "  Run ${YELLOW}./setup_environment.sh${NC} to set up Python environment"
echo ""

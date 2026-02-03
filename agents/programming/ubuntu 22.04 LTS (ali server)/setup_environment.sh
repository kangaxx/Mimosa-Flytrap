#!/bin/bash

###############################################################################
# Python Environment Setup Script for LangChain
# 
# This script creates a Python virtual environment and installs all necessary
# packages for LangChain-based AI agents.
#
# Usage: ./setup_environment.sh
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

VENV_DIR="langchain-env"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}LangChain Environment Setup${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if Python 3.10 is installed
if ! command -v python3.10 &> /dev/null; then
    echo -e "${RED}Error: Python 3.10 is not installed.${NC}"
    echo "Please run ./install_dependencies.sh first."
    exit 1
fi

echo "Python version: $(python3.10 --version)"
echo ""

# Check if virtual environment already exists
if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Virtual environment '$VENV_DIR' already exists.${NC}"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Removing existing environment...${NC}"
        rm -rf "$VENV_DIR"
    else
        echo "Using existing environment."
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3.10 -m venv "$VENV_DIR"
    echo -e "${GREEN}Virtual environment created: $VENV_DIR${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo ""
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel

# Install packages from requirements.txt
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Installing Python Packages${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    echo -e "${YELLOW}Installing packages from requirements.txt...${NC}"
    pip install -r "$SCRIPT_DIR/requirements.txt"
else
    echo -e "${YELLOW}requirements.txt not found. Installing essential packages...${NC}"
    
    # Core LangChain packages
    echo -e "${BLUE}Installing LangChain core...${NC}"
    pip install langchain langchain-community langchain-core
    
    # OpenAI integration
    echo -e "${BLUE}Installing OpenAI integration...${NC}"
    pip install langchain-openai openai
    
    # Ollama integration
    echo -e "${BLUE}Installing Ollama integration...${NC}"
    pip install langchain-ollama
    
    # Essential utilities
    echo -e "${BLUE}Installing utilities...${NC}"
    pip install python-dotenv requests tiktoken
    
    # Document processing
    echo -e "${BLUE}Installing document processing tools...${NC}"
    pip install pypdf chromadb
    
    # Vector stores and embeddings
    echo -e "${BLUE}Installing vector store and embeddings...${NC}"
    pip install faiss-cpu sentence-transformers
    
    # Additional useful packages
    echo -e "${BLUE}Installing additional packages...${NC}"
    pip install pydantic beautifulsoup4 lxml
fi

# Verify installation
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Verifying Installation${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

echo "Installed packages:"
pip list | grep -E "langchain|openai|ollama|dotenv"

# Create .env file if it doesn't exist
echo ""
echo -e "${YELLOW}Setting up environment configuration...${NC}"

if [ ! -f "$SCRIPT_DIR/.env" ]; then
    if [ -f "$SCRIPT_DIR/.env.example" ]; then
        cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
        echo -e "${GREEN}.env file created from template.${NC}"
        echo -e "${YELLOW}Please edit .env and add your API keys.${NC}"
    else
        echo -e "${YELLOW}.env.example not found. Skipping .env creation.${NC}"
    fi
else
    echo -e "${GREEN}.env file already exists.${NC}"
fi

# Test imports
echo ""
echo -e "${YELLOW}Testing package imports...${NC}"

python3 << EOF
import sys
try:
    import langchain
    print("✓ LangChain imported successfully")
    import langchain_openai
    print("✓ LangChain OpenAI imported successfully")
    import langchain_community
    print("✓ LangChain Community imported successfully")
    from dotenv import load_dotenv
    print("✓ python-dotenv imported successfully")
    print("\n✓ All essential packages imported successfully!")
except ImportError as e:
    print(f"✗ Import error: {e}", file=sys.stderr)
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Setup Complete!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "Your LangChain environment is ready to use!"
    echo ""
    echo -e "To activate the environment:"
    echo -e "  ${YELLOW}source $VENV_DIR/bin/activate${NC}"
    echo ""
    echo -e "To deactivate:"
    echo -e "  ${YELLOW}deactivate${NC}"
    echo ""
    echo -e "Next steps:"
    echo -e "  1. Edit ${YELLOW}.env${NC} with your OpenAI API key"
    echo -e "  2. Run ${YELLOW}./test_setup.sh${NC} to verify everything works"
    echo -e "  3. Try ${YELLOW}python run_langchain_agent.py${NC} to run your first agent"
    echo ""
else
    echo ""
    echo -e "${RED}Setup encountered errors. Please check the output above.${NC}"
    exit 1
fi

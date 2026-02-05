#!/bin/bash

###############################################################################
# Ubuntu 22.04 LTS System Dependencies Installation Script
# 
# This script installs all necessary system-level dependencies for running
# LangChain-based AI agents with Ollama and GPT-3.5 integration.
#
# Usage: sudo ./install_dependencies.sh
# 2026 02 05
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Error: This script must be run as root or with sudo${NC}"
    exit 1
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Ubuntu 22.04 LTS Dependency Installation${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Update package lists
echo -e "${YELLOW}[1/6] Updating package lists...${NC}"
apt update

# Upgrade existing packages
echo -e "${YELLOW}[2/6] Upgrading existing packages...${NC}"
apt upgrade -y

# Install Python 3.10 and related tools
echo -e "${YELLOW}[3/6] Installing Python 3.10 and pip...${NC}"
apt install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    python3.10-dev

# Install build tools and essential packages
echo -e "${YELLOW}[4/6] Installing build tools...${NC}"
apt install -y \
    build-essential \
    curl \
    wget \
    git \
    ca-certificates \
    gnupg \
    lsb-release

# Install additional libraries
echo -e "${YELLOW}[5/6] Installing additional dependencies...${NC}"
apt install -y \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libpq-dev \
    zlib1g-dev \
    libjpeg-dev \
    software-properties-common

# Install optional but useful tools
echo -e "${YELLOW}[6/6] Installing optional tools...${NC}"
apt install -y \
    vim \
    nano \
    htop \
    net-tools \
    jq \
    tree

# Clean up
echo -e "${YELLOW}Cleaning up...${NC}"
apt autoremove -y
apt clean

# Verify installations
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Verification${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

echo "Python version:"
python3 --version

echo ""
echo "pip version:"
pip3 --version

echo ""
echo "git version:"
git --version

echo ""
echo "curl version:"
curl --version | head -n 1

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Installation Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Next steps:"
echo -e "  1. Run ${YELLOW}./setup_ollama.sh${NC} to install Ollama"
echo -e "  2. Run ${YELLOW}./setup_environment.sh${NC} to set up Python environment"
echo ""

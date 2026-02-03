#!/bin/bash

###############################################################################
# Setup Verification Script
# 
# This script verifies that all components of the LangChain environment
# are properly installed and configured.
#
# Usage: ./test_setup.sh
###############################################################################

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="langchain-env"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}LangChain Setup Verification${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Counter for passed/failed tests
PASSED=0
FAILED=0

# Function to report test result
test_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $2"
        ((FAILED++))
    fi
}

# Test 1: Check Python installation
echo -e "${BLUE}[1/10] Checking Python installation...${NC}"
if command -v python3.10 &> /dev/null; then
    VERSION=$(python3.10 --version)
    test_result 0 "Python 3.10 installed: $VERSION"
else
    test_result 1 "Python 3.10 not found"
fi

# Test 2: Check virtual environment
echo -e "${BLUE}[2/10] Checking virtual environment...${NC}"
if [ -d "$VENV_DIR" ]; then
    test_result 0 "Virtual environment exists: $VENV_DIR"
else
    test_result 1 "Virtual environment not found: $VENV_DIR"
fi

# Test 3: Check Ollama installation
echo -e "${BLUE}[3/10] Checking Ollama installation...${NC}"
if command -v ollama &> /dev/null; then
    VERSION=$(ollama --version 2>&1 | head -n 1)
    test_result 0 "Ollama installed: $VERSION"
else
    test_result 1 "Ollama not found"
fi

# Test 4: Check Ollama service
echo -e "${BLUE}[4/10] Checking Ollama service...${NC}"
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    test_result 0 "Ollama service is running on port 11434"
else
    test_result 1 "Ollama service not responding on port 11434"
fi

# Test 5: Check for downloaded models
echo -e "${BLUE}[5/10] Checking downloaded models...${NC}"
if command -v ollama &> /dev/null; then
    MODEL_COUNT=$(ollama list 2>/dev/null | tail -n +2 | wc -l)
    if [ "$MODEL_COUNT" -gt 0 ]; then
        test_result 0 "Found $MODEL_COUNT Ollama model(s)"
        echo "   Available models:"
        ollama list | tail -n +2 | awk '{print "   - " $1}'
    else
        test_result 1 "No Ollama models downloaded"
    fi
fi

# Activate virtual environment for Python tests
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
fi

# Test 6: Check LangChain installation
echo -e "${BLUE}[6/10] Checking LangChain installation...${NC}"
if python3 -c "import langchain" 2>/dev/null; then
    VERSION=$(python3 -c "import langchain; print(langchain.__version__)" 2>/dev/null)
    test_result 0 "LangChain installed: $VERSION"
else
    test_result 1 "LangChain not installed"
fi

# Test 7: Check OpenAI integration
echo -e "${BLUE}[7/10] Checking OpenAI integration...${NC}"
if python3 -c "import langchain_openai" 2>/dev/null; then
    test_result 0 "LangChain OpenAI integration installed"
else
    test_result 1 "LangChain OpenAI integration not installed"
fi

# Test 8: Check Ollama integration
echo -e "${BLUE}[8/10] Checking Ollama integration...${NC}"
if python3 -c "from langchain_community.llms import Ollama" 2>/dev/null; then
    test_result 0 "LangChain Ollama integration installed"
else
    test_result 1 "LangChain Ollama integration not installed"
fi

# Test 9: Check environment file
echo -e "${BLUE}[9/10] Checking environment configuration...${NC}"
if [ -f "$SCRIPT_DIR/.env" ]; then
    test_result 0 ".env file exists"
    
    # Check for API key (but don't display it)
    if grep -q "OPENAI_API_KEY=sk-" "$SCRIPT_DIR/.env" 2>/dev/null; then
        echo -e "${GREEN}   ✓${NC} OpenAI API key configured"
    else
        echo -e "${YELLOW}   ⚠${NC} OpenAI API key not configured or invalid"
    fi
else
    test_result 1 ".env file not found"
fi

# Test 10: Check required Python packages
echo -e "${BLUE}[10/10] Checking required Python packages...${NC}"
REQUIRED_PACKAGES=("langchain" "langchain-openai" "langchain-community" "python-dotenv")
MISSING_PACKAGES=()

for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! pip show $(echo $package | tr '-' '_') &> /dev/null; then
        MISSING_PACKAGES+=("$package")
    fi
done

if [ ${#MISSING_PACKAGES[@]} -eq 0 ]; then
    test_result 0 "All required packages installed"
else
    test_result 1 "Missing packages: ${MISSING_PACKAGES[*]}"
fi

# Summary
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Test Summary${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed! Your environment is ready.${NC}"
    echo ""
    echo -e "You can now:"
    echo -e "  1. Activate the environment: ${YELLOW}source $VENV_DIR/bin/activate${NC}"
    echo -e "  2. Run the example agent: ${YELLOW}python run_langchain_agent.py${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}✗ Some tests failed. Please review the issues above.${NC}"
    echo ""
    echo -e "Common fixes:"
    echo -e "  - Run ${YELLOW}./install_dependencies.sh${NC} for system packages"
    echo -e "  - Run ${YELLOW}./setup_ollama.sh${NC} for Ollama setup"
    echo -e "  - Run ${YELLOW}./setup_environment.sh${NC} for Python environment"
    echo ""
    exit 1
fi

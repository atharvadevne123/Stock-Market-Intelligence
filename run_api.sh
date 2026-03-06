#!/bin/bash
"""
Stock Market Intelligence API - Setup & Run Script
"""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Directories
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_DIR="$PROJECT_DIR/api"

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Stock Market Intelligence - API Setup & Run                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if venv exists
if [ ! -d "$PROJECT_DIR/venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv "$PROJECT_DIR/venv"
fi

# Activate venv
echo -e "${BLUE}Activating virtual environment...${NC}"
source "$PROJECT_DIR/venv/bin/activate"

# Check dependencies
echo -e "${BLUE}Checking dependencies...${NC}"
pip list | grep -q "fastapi" || {
    echo -e "${YELLOW}Installing FastAPI...${NC}"
    pip install fastapi uvicorn
}

# Create API directory if it doesn't exist
if [ ! -d "$API_DIR" ]; then
    echo -e "${YELLOW}Creating api directory...${NC}"
    mkdir -p "$API_DIR"
fi

# Copy main.py to api directory if it doesn't exist
if [ ! -f "$API_DIR/main.py" ]; then
    echo -e "${YELLOW}Setting up API...${NC}"
    cp "$PROJECT_DIR/api_main.py" "$API_DIR/main.py"
fi

# Create __init__.py
touch "$API_DIR/__init__.py"

echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  ✅ Setup Complete!                                            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${BLUE}Starting API Server...${NC}\n"

# Run the API
cd "$PROJECT_DIR"
python "$API_DIR/main.py"

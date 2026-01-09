#!/bin/bash

# ProTox3-Automation One-Click Installation Script
# Version: 1.0.0
# Date: 2026-01-08

set -e

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Print welcome message
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}         ProTox3-Automation Installation Script            ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}         Version: 1.0.0                                    ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check operating system
print_info "Checking operating system..."
OS=$(uname -s)
if [[ "$OS" == "Linux" ]]; then
    print_success "Operating system: Linux"
elif [[ "$OS" == "Darwin" ]]; then
    print_success "Operating system: macOS"
else
    print_error "Unsupported operating system: $OS"
    exit 1
fi

# Check Python version
print_info "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 7 ]; then
        print_success "Python version: $PYTHON_VERSION (OK)"
    else
        print_error "Python 3.7+ is required, current version: $PYTHON_VERSION"
        exit 1
    fi
else
    print_error "Python 3 is not installed"
    exit 1
fi

# Check pip
print_info "Checking pip..."
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version | awk '{print $2}')
    print_success "pip version: $PIP_VERSION"
else
    print_error "pip3 is not installed"
    exit 1
fi

# Check Chrome/Chromium browser
print_info "Checking Chrome/Chromium browser..."
if command -v google-chrome &> /dev/null; then
    CHROME_VERSION=$(google-chrome --version 2>&1 | awk '{print $3}')
    print_success "Chrome version: $CHROME_VERSION"
elif command -v chromium-browser &> /dev/null; then
    CHROMIUM_VERSION=$(chromium-browser --version 2>&1 | awk '{print $2}')
    print_success "Chromium version: $CHROMIUM_VERSION"
elif command -v chromium &> /dev/null; then
    CHROMIUM_VERSION=$(chromium --version 2>&1 | awk '{print $2}')
    print_success "Chromium version: $CHROMIUM_VERSION"
else
    print_warning "Chrome/Chromium browser not found"
    print_warning "Please install Chrome or Chromium manually"
fi

# Create virtual environment
print_info "Creating virtual environment..."
cd "$SCRIPT_DIR"
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip -q
print_success "pip upgraded"

# Install dependencies
print_info "Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt -q
    print_success "Dependencies installed"
else
    print_warning "requirements.txt not found, installing core dependencies..."
    pip install selenium rdkit-pypi -q
    print_success "Core dependencies installed"
fi

# Create necessary directories
print_info "Creating directories..."
mkdir -p data
mkdir -p results
mkdir -p logs
print_success "Directories created"

# Create example input file if not exists
if [ ! -f "data/example_input.csv" ]; then
    print_info "Creating example input file..."
    cat > data/example_input.csv << 'EOF'
PubChem_ID,SMILES
311434,CC1=CC(=NO1)NC(=O)NC2=CC(=C(C=C2OC)OC)Cl
54576693,C1CN(CCN1CC2=CC3=C(C=C2)OC(O3)(F)F)C(=O)NC4=C(C=CN=C4)Cl
121280087,CN(C)CCN(C)C1=CC(=C(C=C1NC(=O)C=C)NC2=NC=CC(=N2)C3=CN(C4=CC=CC=C43)C5CC5)OC
EOF
    print_success "Example input file created"
fi

# Set execute permissions
print_info "Setting execute permissions..."
chmod +x setup.sh
chmod +x run_protox.sh
print_success "Execute permissions set"

# Installation complete
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC}              Installation Complete!                        ${GREEN}║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

print_success "ProTox3-Automation has been successfully installed!"
echo ""
print_info "Next steps:"
echo "  1. Prepare your input CSV file with PubChem_ID and SMILES columns"
echo "  2. Place it in the data/ directory (or use data/example_input.csv)"
echo "  3. Run: bash run_protox.sh"
echo ""
print_info "For more information, see:"
echo "  - README.md: Project overview"
echo "  - docs/QUICK_START.md: Quick start guide"
echo "  - docs/USER_GUIDE.md: Detailed user guide"
echo ""
print_warning "Note: Make sure to configure paths in config.py if needed"
echo ""

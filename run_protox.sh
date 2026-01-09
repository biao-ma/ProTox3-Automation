#!/bin/bash

# ProTox-3 Quick Start Script
# Usage: bash run_protox.sh [start] [end]
# Example: bash run_protox.sh 0 10

set -e

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Configuration - use relative paths
VENV_PATH="$SCRIPT_DIR/venv"
SCRIPT_PATH="$SCRIPT_DIR/src/protox_full_automation.py"
OUTPUT_DIR="$SCRIPT_DIR/results"
LOG_DIR="$SCRIPT_DIR/logs"

# Functions: Print colored messages
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

# Check virtual environment
print_info "Checking virtual environment..."
if [ ! -d "$VENV_PATH" ]; then
    print_warning "Virtual environment does not exist, creating..."
    python3 -m venv "$VENV_PATH"
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source "$VENV_PATH/bin/activate"
print_success "Virtual environment activated"

# Check required packages
print_info "Checking dependencies..."
pip install -q selenium rdkit 2>/dev/null || true

# Verify script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    print_error "Script not found: $SCRIPT_PATH"
    exit 1
fi

# Create output directories
mkdir -p "$OUTPUT_DIR"
mkdir -p "$LOG_DIR"

# Get command line arguments
START_IDX=${1:-0}
END_IDX=${2:-}

# Print startup information
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}     ProTox-3 Cytotoxicity Prediction Automation           ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

print_info "Configuration:"
echo "  Virtual environment: $VENV_PATH"
echo "  Script path: $SCRIPT_PATH"
echo "  Output directory: $OUTPUT_DIR"
echo ""

if [ -z "$END_IDX" ]; then
    print_info "Processing range: Starting from compound $START_IDX (all remaining compounds)"
    echo ""
    print_warning "Note: Processing all 97 compounds takes approximately 8-16 hours"
    echo ""
    read -p "Continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Cancelled"
        exit 0
    fi
    echo ""
    python3 "$SCRIPT_PATH" "$START_IDX"
else
    print_info "Processing range: From compound $START_IDX to $END_IDX (total: $((END_IDX - START_IDX)) compounds)"
    echo ""
    print_warning "Note: Processing $((END_IDX - START_IDX)) compounds takes approximately $(( (END_IDX - START_IDX) * 7 / 60 ))-$(( (END_IDX - START_IDX) * 10 / 60 )) hours"
    echo ""
    read -p "Continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Cancelled"
        exit 0
    fi
    echo ""
    python3 "$SCRIPT_PATH" "$START_IDX" "$END_IDX"
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC}                  Processing Complete!                      ${GREEN}║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Display result statistics
COMPLETED=$(ls "$OUTPUT_DIR"/CID_*.csv 2>/dev/null | wc -l)
print_success "Completed compounds: $COMPLETED"

if [ -f "$OUTPUT_DIR/cytotoxicity_summary.csv" ]; then
    SUMMARY_LINES=$(wc -l < "$OUTPUT_DIR/cytotoxicity_summary.csv")
    print_success "Summary file lines: $((SUMMARY_LINES - 1)) compounds (including header)"
    print_success "Summary file location: $OUTPUT_DIR/cytotoxicity_summary.csv"
fi

echo ""
print_info "Log file: $LOG_DIR/processing_log.txt"
echo ""

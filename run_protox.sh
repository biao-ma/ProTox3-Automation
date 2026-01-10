#!/bin/bash

# ProTox-3 Complete Automation Script
# This script handles the entire workflow:
# 1. Check/prepare input data
# 2. Convert SMILES to Canonical format
# 3. Run toxicity predictions
# 4. Extract and aggregate results
#
# Usage: bash run_protox.sh [start] [end]
# Example: bash run_protox.sh 0 10
#
# NOTE: All paths are read from config.py
# To customize paths, edit config.py instead of this script

set -e

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Helper function to read config from config.py
get_config() {
    python3 "$SCRIPT_DIR/src/get_config.py" "$1" 2>/dev/null || {
        print_error "Failed to read configuration: $1"
        exit 1
    }
}

# Read configuration from config.py
VENV_PATH="$SCRIPT_DIR/venv"
DATA_DIR=$(get_config "DATA_DIR")
RESULTS_DIR=$(get_config "RESULTS_DIR")
LOGS_DIR=$(get_config "LOGS_DIR")
INPUT_CSV=$(get_config "INPUT_FILE")
CANONICAL_CSV=$(get_config "CANONICAL_SMILES_FILE")
SUMMARY_CSV=$(get_config "CYTOTOXICITY_SUMMARY_FILE")

# Script paths
CONVERT_SCRIPT="$SCRIPT_DIR/src/convert_smiles.py"
PROTOX_SCRIPT="$SCRIPT_DIR/src/protox_full_automation.py"
EXTRACT_SCRIPT="$SCRIPT_DIR/src/extract_cytotoxicity.py"

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

print_step() {
    echo -e "${CYAN}[STEP]${NC} $1"
}

# Print banner
print_banner() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}     ProTox-3 Cytotoxicity Prediction Automation           ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}     Complete Workflow: Data → Prediction → Results        ${BLUE}║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}Configuration loaded from config.py${NC}"
    echo ""
}

# Check and activate virtual environment
setup_venv() {
    print_step "Step 1: Setting up virtual environment"
    
    if [ ! -d "$VENV_PATH" ]; then
        print_error "Virtual environment not found!"
        echo ""
        echo "Please run setup.sh first to create the virtual environment:"
        echo "  bash setup.sh"
        echo ""
        exit 1
    fi
    
    print_info "Virtual environment found"
    
    # Activate virtual environment
    print_info "Activating virtual environment..."
    source "$VENV_PATH/bin/activate"
    print_success "Virtual environment activated"
    
    # Quick dependency check (no installation)
    print_info "Checking dependencies..."
    
    # Check if critical packages are installed
    python3 -c "import selenium" 2>/dev/null || {
        print_error "Selenium not found!"
        echo "Please run setup.sh to install dependencies:"
        echo "  bash setup.sh"
        exit 1
    }
    
    python3 -c "from rdkit import Chem" 2>/dev/null || {
        print_error "RDKit not found!"
        echo "Please run setup.sh to install dependencies:"
        echo "  bash setup.sh"
        exit 1
    }
    
    print_success "All dependencies are installed"
    echo ""
}

# Check input data
check_input_data() {
    print_step "Step 2: Checking input data"
    
    print_info "Input file path: $INPUT_CSV"
    
    # Check if input.csv exists
    if [ ! -f "$INPUT_CSV" ]; then
        print_error "Input file not found: $INPUT_CSV"
        echo ""
        echo "Please prepare your input CSV file with the following format:"
        echo "  PubChem_ID,SMILES"
        echo "  311434,CC1=CC(=NO1)NC(=O)..."
        echo "  54576693,C1CN(CCN1CC2=CC3=..."
        echo ""
        echo "You can:"
        echo "  1. Create $INPUT_CSV with your data"
        echo "  2. Use the example file: cp $DATA_DIR/example_input.csv $INPUT_CSV"
        echo "  3. Modify INPUT_FILE path in config.py"
        echo ""
        exit 1
    fi
    
    print_success "Input file found: $INPUT_CSV"
    
    # Count compounds in input file
    TOTAL_COMPOUNDS=$(($(wc -l < "$INPUT_CSV") - 1))
    print_info "Total compounds in input file: $TOTAL_COMPOUNDS"
    echo ""
}

# Convert SMILES to Canonical format
convert_smiles() {
    print_step "Step 3: Converting SMILES to Canonical format"
    
    print_info "Output file: $CANONICAL_CSV"
    
    if [ -f "$CANONICAL_CSV" ]; then
        print_info "Canonical SMILES file already exists, using it"
        print_info "To regenerate, delete $CANONICAL_CSV and run again"
        echo ""
        return
    fi
    
    print_info "Running SMILES conversion..."
    python3 "$CONVERT_SCRIPT" "$INPUT_CSV" "$CANONICAL_CSV"
    
    if [ -f "$CANONICAL_CSV" ]; then
        print_success "SMILES conversion completed"
        CONVERTED_COMPOUNDS=$(($(wc -l < "$CANONICAL_CSV") - 1))
        print_info "Successfully converted: $CONVERTED_COMPOUNDS compounds"
    else
        print_error "SMILES conversion failed"
        exit 1
    fi
    echo ""
}

# Run toxicity predictions
run_predictions() {
    local START_IDX=$1
    local END_IDX=$2
    
    print_step "Step 4: Running toxicity predictions"
    
    print_info "Results will be saved to: $RESULTS_DIR"
    print_info "Processing log: $LOGS_DIR/processing_log.txt"
    
    # Determine processing range
    if [ -z "$END_IDX" ]; then
        TOTAL_TO_PROCESS=$((CONVERTED_COMPOUNDS - START_IDX))
        print_info "Processing range: From compound $START_IDX to end (total: $TOTAL_TO_PROCESS compounds)"
    else
        TOTAL_TO_PROCESS=$((END_IDX - START_IDX))
        print_info "Processing range: From compound $START_IDX to $END_IDX (total: $TOTAL_TO_PROCESS compounds)"
    fi
    
    # Estimate time
    MIN_TIME=$(( TOTAL_TO_PROCESS * 5 / 60 ))
    MAX_TIME=$(( TOTAL_TO_PROCESS * 10 / 60 ))
    
    echo ""
    print_info "Estimated processing time: $MIN_TIME - $MAX_TIME hours"
    print_info "Each compound takes approximately 5-10 minutes"
    echo ""
    print_info "Starting toxicity predictions..."
    print_info "You can monitor progress in: $LOGS_DIR/processing_log.txt"
    echo ""
    
    # Run prediction script
    if [ -z "$END_IDX" ]; then
        python3 "$PROTOX_SCRIPT" "$START_IDX"
    else
        python3 "$PROTOX_SCRIPT" "$START_IDX" "$END_IDX"
    fi
    
    print_success "Toxicity predictions completed"
    echo ""
}

# Extract and aggregate results
extract_results() {
    print_step "Step 5: Extracting and aggregating results"
    
    # Check if there are any result files
    RESULT_COUNT=$(ls "$RESULTS_DIR"/CID_*.csv 2>/dev/null | wc -l)
    
    if [ "$RESULT_COUNT" -eq 0 ]; then
        print_warning "No result files found in $RESULTS_DIR"
        print_info "Skipping result extraction"
        echo ""
        return
    fi
    
    print_info "Found $RESULT_COUNT result files"
    print_info "Extracting Cytotoxicity data..."
    
    python3 "$EXTRACT_SCRIPT"
    
    if [ -f "$SUMMARY_CSV" ]; then
        print_success "Results extracted and aggregated"
        SUMMARY_COUNT=$(($(wc -l < "$SUMMARY_CSV") - 1))
        print_info "Total compounds in summary: $SUMMARY_COUNT"
        print_info "Summary file: $SUMMARY_CSV"
    else
        print_warning "Summary file not created"
    fi
    echo ""
}

# Display final results
display_results() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${NC}                  Processing Complete!                      ${GREEN}║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    print_success "Workflow completed successfully!"
    echo ""
    
    # Display statistics
    if [ -f "$SUMMARY_CSV" ]; then
        print_info "Results Summary:"
        echo "  📁 Individual reports: $RESULTS_DIR/CID_*.csv"
        echo "  📊 Aggregated summary: $SUMMARY_CSV"
        echo "  📝 Processing log: $LOGS_DIR/processing_log.txt"
        echo ""
        
        # Display cytotoxicity statistics
        if command -v awk &> /dev/null; then
            ACTIVE_COUNT=$(awk -F',' 'NR>1 && $5=="Active" {count++} END {print count+0}' "$SUMMARY_CSV")
            INACTIVE_COUNT=$(awk -F',' 'NR>1 && $5=="Inactive" {count++} END {print count+0}' "$SUMMARY_CSV")
            TOTAL_COUNT=$(($(wc -l < "$SUMMARY_CSV") - 1))
            
            print_info "Cytotoxicity Statistics:"
            echo "  Total compounds: $TOTAL_COUNT"
            echo "  Active (cytotoxic): $ACTIVE_COUNT"
            echo "  Inactive (non-cytotoxic): $INACTIVE_COUNT"
            echo ""
        fi
        
        print_info "View results:"
        echo "  cat $SUMMARY_CSV"
        echo "  head -20 $SUMMARY_CSV"
        echo ""
    fi
    
    print_info "Next steps:"
    echo "  • Review the results in $SUMMARY_CSV"
    echo "  • Check individual reports in $RESULTS_DIR/"
    echo "  • Analyze the data for your research"
    echo ""
    
    print_info "To customize paths, edit config.py"
    echo ""
}

# Main workflow
main() {
    # Get command line arguments
    START_IDX=${1:-0}
    END_IDX=${2:-}
    
    # Print banner
    print_banner
    
    # Step 1: Setup virtual environment (check only, no installation)
    setup_venv
    
    # Step 2: Check input data
    check_input_data
    
    # Step 3: Convert SMILES
    convert_smiles
    
    # Step 4: Run predictions
    run_predictions "$START_IDX" "$END_IDX"
    
    # Step 5: Extract results
    extract_results
    
    # Display final results
    display_results
}

# Run main workflow
main "$@"

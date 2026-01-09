#!/usr/bin/env python3
"""
Configuration Reader for Shell Scripts
Reads config.py and outputs specific configuration values
"""

import sys
import os

# Add parent directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 get_config.py <config_key>", file=sys.stderr)
        print("Available keys:", file=sys.stderr)
        print("  BASE_DIR", file=sys.stderr)
        print("  DATA_DIR", file=sys.stderr)
        print("  RESULTS_DIR", file=sys.stderr)
        print("  LOGS_DIR", file=sys.stderr)
        print("  INPUT_FILE", file=sys.stderr)
        print("  CANONICAL_SMILES_FILE", file=sys.stderr)
        print("  CYTOTOXICITY_SUMMARY_FILE", file=sys.stderr)
        print("  PROCESSING_LOG_FILE", file=sys.stderr)
        sys.exit(1)
    
    key = sys.argv[1]
    
    # Get the configuration value
    if hasattr(config, key):
        value = getattr(config, key)
        print(value)
    else:
        print(f"Error: Configuration key '{key}' not found", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
ProTox3-Automation Configuration File

This is the SINGLE SOURCE OF TRUTH for all configuration.
All Python scripts and shell scripts read from this file.

To customize paths or settings:
1. Edit this file
2. Save changes
3. Run your scripts - they will automatically use the new settings

No need to modify any other files!
"""

import os

# Base directory - automatically set to the project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data directories
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# Input/Output files
INPUT_FILE = os.path.join(DATA_DIR, 'input.csv')
CANONICAL_SMILES_FILE = os.path.join(DATA_DIR, 'canonical_smiles.csv')
CYTOTOXICITY_SUMMARY_FILE = os.path.join(RESULTS_DIR, 'cytotoxicity_summary.csv')
PROCESSING_LOG_FILE = os.path.join(LOGS_DIR, 'processing_log.txt')

# ProTox-3 website configuration
PROTOX_BASE_URL = 'http://tox.charite.de/protox3'
PROTOX_INPUT_URL = f'{PROTOX_BASE_URL}/index.php?site=compound_input'
PROTOX_RESULTS_URL = f'{PROTOX_BASE_URL}/index.php?site=compound_search_similarity'

# Processing settings
MAX_WAIT_TIME = 900  # Maximum wait time for prediction (seconds) - 15 minutes
BATCH_SIZE = 10      # Number of compounds to process in one batch
RETRY_TIMES = 3      # Number of retry attempts on failure
                     # Example: RETRY_TIMES = 3 means:
                     #   - 1st attempt fails → retry
                     #   - 2nd attempt fails → retry
                     #   - 3rd attempt fails → mark as failed
                     # Increase for unstable connections, decrease for stable ones

# Browser settings
HEADLESS_MODE = True  # Set to False to see browser window
BROWSER_TIMEOUT = 30  # Browser operation timeout (seconds)

# Debug settings
DEBUG_MODE = False  # Set to True to enable debug screenshots and verbose logging
DEBUG_SCREENSHOT_DIR = os.path.join(RESULTS_DIR, 'debug_screenshots')  # Directory for debug screenshots

# Create directories if they don't exist
for directory in [DATA_DIR, RESULTS_DIR, LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Create debug directory if debug mode is enabled
if DEBUG_MODE:
    os.makedirs(DEBUG_SCREENSHOT_DIR, exist_ok=True)

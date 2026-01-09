# Configuration Guide

This document explains how to configure ProTox3-Automation for your environment.

## Configuration File

All configurable settings are centralized in `config.py` at the project root.

### Location

```
ProTox3-Automation/
├── config.py          # Main configuration file
├── ...
```

### Default Configuration

```python
#!/usr/bin/env python3
"""
ProTox3-Automation Configuration File
All configurable paths and settings
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

# Processing settings
MAX_WAIT_TIME = 900  # Maximum wait time for prediction (seconds) - 15 minutes
BATCH_SIZE = 10      # Number of compounds to process in one batch
RETRY_TIMES = 3      # Number of retry attempts on failure

# Browser settings
HEADLESS_MODE = True  # Set to False to see browser window
BROWSER_TIMEOUT = 30  # Browser operation timeout (seconds)
```

---

## Customization

### 1. Change Input File Location

If your input CSV file is in a different location:

```python
# Option 1: Use absolute path
INPUT_FILE = '/path/to/your/input.csv'

# Option 2: Use relative path from project root
INPUT_FILE = os.path.join(BASE_DIR, 'my_data', 'compounds.csv')
```

### 2. Change Output Directory

To save results to a different directory:

```python
# Option 1: Use absolute path
RESULTS_DIR = '/path/to/your/results'

# Option 2: Use relative path from project root
RESULTS_DIR = os.path.join(BASE_DIR, 'my_results')
```

### 3. Adjust Processing Timeout

If compounds take longer to process:

```python
# Increase timeout to 30 minutes
MAX_WAIT_TIME = 1800  # 30 minutes in seconds

# Or 1 hour
MAX_WAIT_TIME = 3600  # 1 hour in seconds
```

### 4. Change Batch Size

To process compounds in different batch sizes:

```python
# Smaller batches (more frequent checkpoints)
BATCH_SIZE = 5

# Larger batches (fewer checkpoints)
BATCH_SIZE = 20
```

### 5. Enable Browser Window (for debugging)

To see what the browser is doing:

```python
# Show browser window
HEADLESS_MODE = False
```

### 6. Use HTTPS Instead of HTTP

If the ProTox-3 website certificate is fixed:

```python
# Use HTTPS
PROTOX_BASE_URL = 'https://tox.charite.de/protox3'
PROTOX_INPUT_URL = f'{PROTOX_BASE_URL}/index.php?site=compound_input'
```

---

## Environment-Specific Configuration

### Development Environment

For development and testing:

```python
# config.py (development)
HEADLESS_MODE = False  # Show browser
MAX_WAIT_TIME = 300    # Shorter timeout for testing
BATCH_SIZE = 3         # Small batches
```

### Production Environment

For production use:

```python
# config.py (production)
HEADLESS_MODE = True   # Hide browser
MAX_WAIT_TIME = 900    # Standard timeout
BATCH_SIZE = 10        # Standard batch size
```

---

## Path Configuration

### Automatic Path Resolution

The configuration uses automatic path resolution based on the project directory:

```python
# BASE_DIR is automatically set to the project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# All other paths are relative to BASE_DIR
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
```

This means:
- ✅ No hardcoded paths
- ✅ Works on any system
- ✅ Works in any directory
- ✅ No manual path configuration needed

### Custom Paths

If you need to use custom paths:

```python
# Example: Use a shared network drive for results
RESULTS_DIR = '/mnt/shared/protox_results'

# Example: Use a different data source
INPUT_FILE = '/data/compounds/batch_001.csv'
```

---

## Command-Line Overrides

Some scripts support command-line arguments to override config settings:

### convert_smiles.py

```bash
# Use default paths from config.py
python3 src/convert_smiles.py

# Override with custom paths
python3 src/convert_smiles.py /path/to/input.csv /path/to/output.csv
```

### protox_full_automation.py

```bash
# Process all compounds (uses config.py paths)
python3 src/protox_full_automation.py

# Process specific range
python3 src/protox_full_automation.py 0 10
```

---

## Validation

After modifying `config.py`, validate your configuration:

```bash
# Test configuration
python3 -c "import config; print('Configuration loaded successfully')"

# Check paths
python3 -c "import config; print(f'Data dir: {config.DATA_DIR}'); print(f'Results dir: {config.RESULTS_DIR}')"
```

---

## Troubleshooting

### Problem: "No such file or directory"

**Solution**: Check that the paths in `config.py` are correct:

```python
# Verify paths exist
import os
print(f"Data dir exists: {os.path.exists(config.DATA_DIR)}")
print(f"Input file exists: {os.path.exists(config.INPUT_FILE)}")
```

### Problem: "Permission denied"

**Solution**: Ensure you have write permissions:

```bash
# Check permissions
ls -la results/
ls -la logs/

# Fix permissions if needed
chmod 755 results/
chmod 755 logs/
```

### Problem: Configuration not taking effect

**Solution**: Restart the script after modifying `config.py`:

```bash
# Kill any running processes
pkill -f protox_full_automation.py

# Restart
python3 src/protox_full_automation.py
```

---

## Best Practices

### 1. Keep config.py in Version Control

```bash
# Include config.py in git
git add config.py
git commit -m "Update configuration"
```

### 2. Use Environment Variables for Sensitive Data

```python
# config.py
import os

# Use environment variable if available
API_KEY = os.environ.get('PROTOX_API_KEY', 'default_key')
```

### 3. Document Your Changes

```python
# config.py
# Modified by: John Doe
# Date: 2026-01-08
# Reason: Increased timeout for large compounds
MAX_WAIT_TIME = 1800  # 30 minutes
```

### 4. Test After Changes

```bash
# Always test after modifying config
python3 src/convert_smiles.py
python3 src/protox_full_automation.py 0 1  # Test with one compound
```

---

## Example Configurations

### Example 1: High-Throughput Processing

```python
# config.py
MAX_WAIT_TIME = 600    # Shorter timeout
BATCH_SIZE = 20        # Larger batches
HEADLESS_MODE = True   # No GUI
RETRY_TIMES = 1        # Fewer retries
```

### Example 2: Careful Processing

```python
# config.py
MAX_WAIT_TIME = 1800   # Longer timeout
BATCH_SIZE = 5         # Smaller batches
HEADLESS_MODE = False  # Show browser
RETRY_TIMES = 5        # More retries
```

### Example 3: Development/Testing

```python
# config.py
MAX_WAIT_TIME = 300    # Short timeout
BATCH_SIZE = 2         # Very small batches
HEADLESS_MODE = False  # Show browser
INPUT_FILE = os.path.join(BASE_DIR, 'data', 'test_input.csv')  # Test data
```

---

## Additional Resources

- [Quick Start Guide](QUICK_START.md)
- [User Guide](USER_GUIDE.md)
- [Troubleshooting](TROUBLESHOOTING.md)

---

**Last Updated**: 2026-01-08

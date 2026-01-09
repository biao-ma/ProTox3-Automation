# Configuration Refactoring

## 📝 Overview

This document describes the configuration refactoring that centralizes all path and settings management in `config.py`, eliminating duplicate configuration across scripts.

---

## 🎯 Problem Statement

### Before Refactoring

Configuration was duplicated in multiple places:

**config.py**:
```python
DATA_DIR = os.path.join(BASE_DIR, 'data')
INPUT_FILE = os.path.join(DATA_DIR, 'input.csv')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
# ... more settings
```

**run_protox.sh**:
```bash
DATA_DIR="$SCRIPT_DIR/data"
INPUT_CSV="$DATA_DIR/input.csv"
RESULTS_DIR="$SCRIPT_DIR/results"
# ... duplicate settings
```

**Problems**:
- ❌ Configuration duplicated in 2 places
- ❌ Need to modify both files to change paths
- ❌ Risk of inconsistency
- ❌ Harder to maintain

---

## ✅ Solution

### After Refactoring

**Single Source of Truth**: All configuration in `config.py`

**config.py** (unchanged):
```python
# All paths and settings defined here
DATA_DIR = os.path.join(BASE_DIR, 'data')
INPUT_FILE = os.path.join(DATA_DIR, 'input.csv')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
# ...
```

**src/get_config.py** (new helper script):
```python
# Reads config.py and outputs values for shell scripts
import config
print(getattr(config, sys.argv[1]))
```

**run_protox.sh** (reads from config.py):
```bash
# Read configuration from config.py
DATA_DIR=$(get_config "DATA_DIR")
INPUT_CSV=$(get_config "INPUT_FILE")
RESULTS_DIR=$(get_config "RESULTS_DIR")
# ...
```

**Benefits**:
- ✅ Single source of truth
- ✅ Only modify config.py to change paths
- ✅ No risk of inconsistency
- ✅ Easier to maintain

---

## 🔧 Implementation Details

### 1. Created Helper Script: `src/get_config.py`

**Purpose**: Bridge between Python config and Shell scripts

**Usage**:
```bash
# Get a configuration value
python3 src/get_config.py DATA_DIR
# Output: /path/to/ProTox3-Automation/data

# Get another value
python3 src/get_config.py INPUT_FILE
# Output: /path/to/ProTox3-Automation/data/input.csv
```

**Available Keys**:
- `BASE_DIR` - Project root directory
- `DATA_DIR` - Data directory
- `RESULTS_DIR` - Results directory
- `LOGS_DIR` - Logs directory
- `INPUT_FILE` - Input CSV file path
- `CANONICAL_SMILES_FILE` - Canonical SMILES file path
- `CYTOTOXICITY_SUMMARY_FILE` - Summary CSV file path
- `PROCESSING_LOG_FILE` - Processing log file path

### 2. Modified `run_protox.sh`

**Added helper function**:
```bash
# Helper function to read config from config.py
get_config() {
    python3 "$SCRIPT_DIR/src/get_config.py" "$1" 2>/dev/null || {
        print_error "Failed to read configuration: $1"
        exit 1
    }
}
```

**Read all paths from config.py**:
```bash
# Read configuration from config.py
DATA_DIR=$(get_config "DATA_DIR")
RESULTS_DIR=$(get_config "RESULTS_DIR")
LOGS_DIR=$(get_config "LOGS_DIR")
INPUT_CSV=$(get_config "INPUT_FILE")
CANONICAL_CSV=$(get_config "CANONICAL_SMILES_FILE")
SUMMARY_CSV=$(get_config "CYTOTOXICITY_SUMMARY_FILE")
```

### 3. Updated Banner

Added indication that configuration is loaded from config.py:

```
╔════════════════════════════════════════════════════════════╗
║     ProTox-3 Cytotoxicity Prediction Automation           ║
║     Complete Workflow: Data → Prediction → Results        ║
╚════════════════════════════════════════════════════════════╝
Configuration loaded from config.py
```

---

## 📖 Usage Guide

### For Users

**To customize paths**, simply edit `config.py`:

```python
# config.py

# Example: Change data directory
DATA_DIR = os.path.join(BASE_DIR, 'my_data')

# Example: Change input file name
INPUT_FILE = os.path.join(DATA_DIR, 'my_compounds.csv')

# Example: Change results directory
RESULTS_DIR = os.path.join(BASE_DIR, 'my_results')
```

**That's it!** All scripts will automatically use the new paths.

### No Need to Modify

- ❌ Don't modify `run_protox.sh`
- ❌ Don't modify `src/get_config.py`
- ✅ Only modify `config.py`

---

## 🔄 Migration Guide

### For Existing Users

If you've already cloned the repository:

```bash
# 1. Update to latest version
cd /path/to/ProTox3-Automation
git pull origin master

# 2. Review config.py (optional)
cat config.py

# 3. Customize if needed (optional)
nano config.py

# 4. Use as normal
bash run_protox.sh
```

### For New Users

No changes needed - just use as documented:

```bash
git clone https://github.com/biao-ma/ProTox3-Automation.git
cd ProTox3-Automation
bash setup.sh
bash run_protox.sh
```

---

## 📊 Comparison

| Aspect | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Config locations** | 2 places | 1 place | ✅ Centralized |
| **To change paths** | Edit 2 files | Edit 1 file | ✅ Simpler |
| **Risk of inconsistency** | High | None | ✅ Safer |
| **Maintenance** | Harder | Easier | ✅ Better |
| **User experience** | Confusing | Clear | ✅ Improved |

---

## 🎨 Design Philosophy

### Single Source of Truth (SSOT)

> "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system."

**Benefits**:
1. **Consistency**: No conflicting values
2. **Simplicity**: One place to change
3. **Maintainability**: Easier to update
4. **Reliability**: Less prone to errors

### Separation of Concerns

| Component | Responsibility |
|-----------|----------------|
| **config.py** | Define all configuration |
| **get_config.py** | Bridge Python ↔ Shell |
| **run_protox.sh** | Execute workflow |
| **Python scripts** | Process data |

---

## 🧪 Testing

### Test Configuration Reading

```bash
# Test get_config.py
cd ProTox3-Automation
python3 src/get_config.py DATA_DIR
python3 src/get_config.py INPUT_FILE
python3 src/get_config.py RESULTS_DIR
```

### Test run_protox.sh Integration

```bash
# Test that run_protox.sh reads config correctly
bash run_protox.sh
# Should show: "Configuration loaded from config.py"
```

### Test Custom Configuration

```bash
# 1. Backup original config
cp config.py config.py.backup

# 2. Modify config
cat >> config.py << 'EOF'
# Custom test configuration
DATA_DIR = os.path.join(BASE_DIR, 'test_data')
EOF

# 3. Test
python3 src/get_config.py DATA_DIR
# Should output: /path/to/ProTox3-Automation/test_data

# 4. Restore original
mv config.py.backup config.py
```

---

## 🐛 Troubleshooting

### Issue: "Failed to read configuration"

**Error**:
```
[ERROR] Failed to read configuration: DATA_DIR
```

**Possible causes**:
1. `config.py` is missing or corrupted
2. `src/get_config.py` is missing
3. Python import error

**Solution**:
```bash
# Check if files exist
ls -l config.py src/get_config.py

# Test get_config.py directly
python3 src/get_config.py DATA_DIR

# If still failing, re-clone repository
git pull origin master
```

### Issue: Configuration key not found

**Error**:
```
Error: Configuration key 'INVALID_KEY' not found
```

**Solution**:
Use only valid configuration keys (see list above).

### Issue: Paths not updating

**Problem**: Modified `config.py` but paths haven't changed

**Solution**:
```bash
# 1. Check if config.py was saved
cat config.py | grep DATA_DIR

# 2. Test get_config.py
python3 src/get_config.py DATA_DIR

# 3. Restart the script
bash run_protox.sh
```

---

## 📚 Related Documentation

- [config.py](config.py) - Main configuration file
- [src/get_config.py](src/get_config.py) - Configuration reader
- [CONFIGURATION.md](docs/CONFIGURATION.md) - Configuration guide
- [OPTIMIZATION_NOTES.md](OPTIMIZATION_NOTES.md) - Other optimizations

---

## 🎉 Summary

### What Changed

| File | Change | Impact |
|------|--------|--------|
| **config.py** | No change | Still the single source of truth |
| **src/get_config.py** | New file | Enables shell scripts to read config |
| **run_protox.sh** | Refactored | Now reads from config.py |

### Benefits

1. ✅ **Single source of truth** - Only edit config.py
2. ✅ **No duplication** - Configuration defined once
3. ✅ **Easier maintenance** - One place to update
4. ✅ **Better consistency** - No conflicting values
5. ✅ **Clearer design** - Separation of concerns

### User Impact

**Before**:
```bash
# To change paths, edit both files
nano config.py
nano run_protox.sh
```

**After**:
```bash
# To change paths, edit only config.py
nano config.py
```

**Result**: Simpler, clearer, more maintainable!

---

**Last Updated**: 2026-01-09  
**Version**: 1.2.0  
**Status**: ✅ Refactored

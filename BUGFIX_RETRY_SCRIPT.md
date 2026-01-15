# Bug Fix: retry_failed.py Script Logic Issue

## 🐛 Problem Description

### Issue
When running `retry_failed.py` to retry failed compounds, the script was processing **all compounds** from the original input file instead of only the **failed compounds**.

### Observed Behavior

```bash
python3 src/retry_failed.py
# Identifies 9 failed compounds ✅
# Creates temp_retry_input.csv with only 9 compounds ✅
# Runs protox_full_automation.py ✅
# But processes all 97 compounds from original file ❌
```

### Log Evidence

```
Found 9 failed compounds:
  1. PubChem_ID: 6215
  2. PubChem_ID: 159324
  ...
  9. PubChem_ID: 135398743

✓ Failed compounds list saved to: .../temp_retry_input.csv

Running: python3 .../protox_full_automation.py
Input file: .../temp_retry_input.csv  ← Intended input

[ProTox-3 Automation Script Started]
Configuration:
  Input file: .../output2_canonical_smiles.csv  ← Actually used (wrong!)
Total compounds in file: 97  ← Should be 9!
```

---

## 🔍 Root Cause Analysis

### Problem 1: Hard-coded Input File

**File**: `src/protox_full_automation.py`

The script read the input file path from `config.py`:

```python
# At module level
CANONICAL_SMILES_FILE = config.CANONICAL_SMILES_FILE

# In main()
with open(CANONICAL_SMILES_FILE, 'r', encoding='utf-8') as f:
    # Read compounds...
```

**Issue**: No way to override the input file from command line.

### Problem 2: Ineffective Workaround

**File**: `src/retry_failed.py`

The retry script tried to temporarily modify `config.py`:

```python
# Temporarily replace the input file in config
original_input = config.CANONICAL_SMILES_FILE
config.CANONICAL_SMILES_FILE = temp_input  # ← Doesn't work!

try:
    result = subprocess.run([sys.executable, script_path], check=False)
finally:
    config.CANONICAL_SMILES_FILE = original_input
```

**Why it failed**:
- `protox_full_automation.py` imports `config` at module load time
- Changing `config.CANONICAL_SMILES_FILE` in the parent process doesn't affect the child process
- The subprocess loads `config.py` fresh and gets the original value

---

## ✅ Solution

### Change 1: Add --input Parameter

**File**: `src/protox_full_automation.py`

Added command-line argument to specify custom input file:

```python
def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='ProTox-3 Automation Script')
    parser.add_argument('start', type=int, nargs='?', default=0, 
                       help='Start index (default: 0)')
    parser.add_argument('end', type=int, nargs='?', default=None, 
                       help='End index (default: all)')
    parser.add_argument('--input', type=str, default=None,  # ← NEW
                       help='Custom input file path (default: from config.py)')
    args = parser.parse_args()
    
    # Use custom input file if provided, otherwise use config
    input_file = args.input if args.input else CANONICAL_SMILES_FILE  # ← NEW
    
    # ... rest of the code uses input_file instead of CANONICAL_SMILES_FILE
```

**Benefits**:
- ✅ Can override input file from command line
- ✅ Backward compatible (defaults to config.py if not specified)
- ✅ Works correctly with subprocess calls

### Change 2: Use --input in retry_failed.py

**File**: `src/retry_failed.py`

Modified to pass the temporary file via command-line argument:

```python
# Before (didn't work)
config.CANONICAL_SMILES_FILE = temp_input
result = subprocess.run([sys.executable, script_path], check=False)

# After (works correctly)
result = subprocess.run(
    [sys.executable, script_path, '--input', temp_input],  # ← Pass via CLI
    check=False
)
```

**Benefits**:
- ✅ Correctly passes custom input file to subprocess
- ✅ No need to modify config module
- ✅ Clean and explicit

---

## 📖 Usage Examples

### Normal Usage (No Change)

```bash
# Uses input file from config.py
python3 src/protox_full_automation.py

# Process specific range
python3 src/protox_full_automation.py 0 10
```

### With Custom Input File (New Feature)

```bash
# Use a different input file
python3 src/protox_full_automation.py --input /path/to/custom_input.csv

# With range
python3 src/protox_full_automation.py 0 10 --input /path/to/custom_input.csv
```

### Retry Failed Compounds (Fixed)

```bash
# Now correctly processes only failed compounds
python3 src/retry_failed.py

# Or automatic mode
python3 src/retry_failed.py --auto
```

---

## 🧪 Testing

### Test 1: Verify --input Parameter

```bash
# Create test file with 2 compounds
cat > /tmp/test_input.csv << 'EOF'
PubChem_ID,Canonical_SMILES
311434,COc1cc(OC)c(NC(=O)Nc2cc(C)on2)cc1Cl
54576693,COc1ccc(NC(=O)Nc2cc(C)on2)cc1OC
EOF

# Run with custom input
python3 src/protox_full_automation.py --input /tmp/test_input.csv

# Check log - should show:
#   Input file: /tmp/test_input.csv
#   Total compounds in file: 2  ← Correct!
```

### Test 2: Verify retry_failed.py

```bash
# Run retry script
python3 src/retry_failed.py

# Check that it processes only failed compounds
# Log should show:
#   Found N failed compounds
#   Running: python3 ... --input .../temp_retry_input.csv
#   Input file: .../temp_retry_input.csv  ← Correct!
#   Total compounds in file: N  ← Matches failed count!
```

### Test 3: Backward Compatibility

```bash
# Old usage still works
python3 src/protox_full_automation.py

# Should use config.py input file
# Log should show:
#   Input file: /path/from/config.py/canonical_smiles.csv
```

---

## 📊 Impact Analysis

### Before Fix

| Scenario | Expected | Actual | Status |
|----------|----------|--------|--------|
| Normal run | Process all compounds | Process all compounds | ✅ OK |
| Retry 9 failed | Process 9 compounds | Process 97 compounds | ❌ **Wrong** |
| Custom input | Not supported | Not supported | ⚠️ Limited |

### After Fix

| Scenario | Expected | Actual | Status |
|----------|----------|--------|--------|
| Normal run | Process all compounds | Process all compounds | ✅ OK |
| Retry 9 failed | Process 9 compounds | Process 9 compounds | ✅ **Fixed** |
| Custom input | Process custom file | Process custom file | ✅ **New Feature** |

---

## 🎯 Key Improvements

### 1. Correct Retry Behavior

**Before**:
```
retry_failed.py identifies 9 failed
  ↓
Creates temp file with 9 compounds
  ↓
Runs protox_full_automation.py
  ↓
Processes all 97 compounds (wrong!)
  ↓
Wastes ~8-16 hours
```

**After**:
```
retry_failed.py identifies 9 failed
  ↓
Creates temp file with 9 compounds
  ↓
Runs protox_full_automation.py --input temp_file
  ↓
Processes only 9 compounds (correct!)
  ↓
Takes ~45-90 minutes
```

### 2. New Flexibility

Users can now process custom compound lists:

```bash
# Extract specific compounds
grep "PubChem_ID: 123\|456\|789" data/input.csv > custom.csv

# Process only those
python3 src/protox_full_automation.py --input custom.csv
```

### 3. Better Debugging

Can test with small subsets:

```bash
# Create test file with 1-2 compounds
head -3 data/canonical_smiles.csv > test.csv

# Quick test run
python3 src/protox_full_automation.py --input test.csv
```

---

## 🔧 Technical Details

### Why Modifying config.py Didn't Work

**Python module loading**:
1. Parent process: `import config` → loads config.py
2. Parent process: `config.CANONICAL_SMILES_FILE = new_value` → modifies in-memory
3. Parent process: `subprocess.run([python3, script.py])` → starts new process
4. Child process: `import config` → **loads config.py fresh from disk**
5. Child process: Gets original value, not modified value

**Solution**: Pass data via command-line arguments, not module variables.

### Why --input Works

**Command-line arguments**:
1. Parent process: `subprocess.run([python3, script.py, '--input', path])`
2. Child process: `argparse` reads `sys.argv`
3. Child process: Gets `--input` value directly
4. No dependency on module state

---

## 📚 Related Documentation

- [RETRY_MECHANISM.md](RETRY_MECHANISM.md) - Complete retry mechanism guide
- [src/protox_full_automation.py](src/protox_full_automation.py) - Main automation script
- [src/retry_failed.py](src/retry_failed.py) - Failure recovery script
- [config.py](config.py) - Configuration file

---

## 🎉 Summary

### What Was Fixed

| Component | Change | Impact |
|-----------|--------|--------|
| **protox_full_automation.py** | Added `--input` parameter | Can specify custom input file |
| **retry_failed.py** | Use `--input` to pass temp file | Correctly processes only failed compounds |
| **Documentation** | Added this bug fix document | Clear explanation of issue and fix |

### Benefits

1. ✅ **Correct Behavior** - retry_failed.py now works as intended
2. ✅ **Time Savings** - Only reprocess failed compounds, not all
3. ✅ **New Feature** - Can use custom input files
4. ✅ **Better Testing** - Easy to test with small compound sets
5. ✅ **Backward Compatible** - Old usage still works

### User Impact

**Before**:
```bash
python3 src/retry_failed.py
# Wastes hours reprocessing all compounds
```

**After**:
```bash
python3 src/retry_failed.py
# Efficiently reprocesses only failed compounds
```

**Result**: Efficient, correct failure recovery! 🎉

---

**Bug Fixed**: 2026-01-15  
**Version**: 1.4.1  
**Status**: ✅ Resolved

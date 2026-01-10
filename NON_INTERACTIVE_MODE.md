# Non-Interactive Mode and Debug Settings

## 📝 Overview

This document describes the improvements made to enable unattended execution and conditional debug output.

---

## 🎯 Improvements

### 1. Removed Interactive Confirmations

**Problem**: The script required user input (y/n) at two points, preventing unattended execution.

**Solution**: Removed all interactive confirmations to enable background and automated runs.

### 2. Conditional Debug Screenshots

**Problem**: Debug screenshots were always saved, cluttering the results directory.

**Solution**: Added `DEBUG_MODE` configuration to control screenshot saving.

---

## 🔧 Changes Made

### 1. run_protox.sh - Removed Interactive Prompts

#### Change 1: SMILES Conversion Confirmation

**Before**:
```bash
if [ -f "$CANONICAL_CSV" ]; then
    print_warning "Canonical SMILES file already exists"
    read -p "Do you want to regenerate it? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Using existing canonical SMILES file"
        return
    fi
fi
```

**After**:
```bash
if [ -f "$CANONICAL_CSV" ]; then
    print_info "Canonical SMILES file already exists, using it"
    print_info "To regenerate, delete $CANONICAL_CSV and run again"
    return
fi
```

**Benefit**: Script automatically uses existing file without asking.

#### Change 2: Prediction Start Confirmation

**Before**:
```bash
print_warning "Estimated processing time: $MIN_TIME - $MAX_TIME hours"
print_warning "Each compound takes approximately 5-10 minutes"

read -p "Continue with toxicity prediction? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Prediction cancelled"
    exit 0
fi
```

**After**:
```bash
print_info "Estimated processing time: $MIN_TIME - $MAX_TIME hours"
print_info "Each compound takes approximately 5-10 minutes"
print_info "Starting toxicity predictions..."
```

**Benefit**: Script starts immediately without waiting for user confirmation.

### 2. config.py - Added Debug Mode

**New Configuration**:
```python
# Debug settings
DEBUG_MODE = False  # Set to True to enable debug screenshots and verbose logging
DEBUG_SCREENSHOT_DIR = os.path.join(RESULTS_DIR, 'debug_screenshots')  # Directory for debug screenshots

# Create debug directory if debug mode is enabled
if DEBUG_MODE:
    os.makedirs(DEBUG_SCREENSHOT_DIR, exist_ok=True)
```

**Benefits**:
- Debug features only active when needed
- Cleaner results directory in production
- Easy to enable for troubleshooting

### 3. protox_full_automation.py - Conditional Screenshots

**Before**:
```python
# Save screenshot for debugging
try:
    screenshot_path = os.path.join(OUTPUT_DIR, f"debug_{pubchem_id}_page.png")
    driver.save_screenshot(screenshot_path)
    log_message(f"  Screenshot saved: {screenshot_path}")
except:
    pass
```

**After**:
```python
# Save screenshot for debugging (only if DEBUG_MODE is enabled)
if config.DEBUG_MODE:
    try:
        screenshot_path = os.path.join(config.DEBUG_SCREENSHOT_DIR, f"debug_{pubchem_id}_page.png")
        driver.save_screenshot(screenshot_path)
        log_message(f"  Screenshot saved: {screenshot_path}")
    except Exception as e:
        log_message(f"  Warning: Failed to save screenshot: {e}")
```

**Benefits**:
- Screenshots only saved when debugging
- Separate directory for debug files
- Better error handling

---

## 📖 Usage Guide

### Normal Mode (Default)

**No changes needed** - just run as usual:

```bash
bash run_protox.sh
```

**Behavior**:
- ✅ No interactive prompts
- ✅ Automatic execution
- ✅ No debug screenshots
- ✅ Clean results directory

### Debug Mode

**Enable debugging** in `config.py`:

```python
# config.py
DEBUG_MODE = True  # Enable debug mode
```

**Then run**:

```bash
bash run_protox.sh
```

**Behavior**:
- ✅ No interactive prompts
- ✅ Automatic execution
- ✅ Debug screenshots saved to `results/debug_screenshots/`
- ✅ More verbose logging

### Background Execution

Now you can run in the background without issues:

```bash
# Run in background
nohup bash run_protox.sh > protox.log 2>&1 &

# Monitor progress
tail -f protox.log
tail -f logs/processing_log.txt

# Check if still running
ps aux | grep run_protox
```

### Batch Processing

Process in batches without manual intervention:

```bash
# Process batch 1
bash run_protox.sh 0 25 &

# Process batch 2
bash run_protox.sh 25 50 &

# Process batch 3
bash run_protox.sh 50 75 &

# Process batch 4
bash run_protox.sh 75 97 &

# Monitor all
tail -f logs/processing_log.txt
```

### Scheduled Execution

Use cron for scheduled runs:

```bash
# Edit crontab
crontab -e

# Add entry (run daily at 2 AM)
0 2 * * * cd /path/to/ProTox3-Automation && bash run_protox.sh >> /path/to/cron.log 2>&1
```

---

## 🔄 Manual Control Options

### Regenerate Canonical SMILES

If you want to regenerate the canonical SMILES file:

```bash
# Delete existing file
rm data/canonical_smiles.csv

# Run script - it will regenerate automatically
bash run_protox.sh
```

### Skip Prediction

If you only want to convert SMILES without running predictions:

```bash
# Run conversion only
python3 src/convert_smiles.py data/input.csv data/canonical_smiles.csv
```

### Force Debug Mode

Enable debug mode temporarily without editing config.py:

```bash
# Set environment variable (if implemented)
DEBUG_MODE=1 bash run_protox.sh

# Or edit config.py temporarily
sed -i 's/DEBUG_MODE = False/DEBUG_MODE = True/' config.py
bash run_protox.sh
sed -i 's/DEBUG_MODE = True/DEBUG_MODE = False/' config.py
```

---

## 📊 Comparison

### Interactive vs Non-Interactive

| Aspect | Before (Interactive) | After (Non-Interactive) | Improvement |
|--------|---------------------|------------------------|-------------|
| **User input required** | 2 prompts | 0 prompts | ✅ Automated |
| **Background execution** | Not possible | Fully supported | ✅ Better |
| **Batch processing** | Manual | Automatic | ✅ Efficient |
| **Scheduled runs** | Not possible | Supported | ✅ Flexible |
| **Unattended operation** | No | Yes | ✅ Convenient |

### Debug Mode

| Aspect | Always On | Conditional (New) | Improvement |
|--------|-----------|-------------------|-------------|
| **Screenshot saving** | Always | Only when needed | ✅ Cleaner |
| **Results directory** | Cluttered | Clean | ✅ Organized |
| **Disk usage** | High | Low | ✅ Efficient |
| **Debug location** | Mixed | Separate dir | ✅ Better |
| **Production use** | Messy | Clean | ✅ Professional |

---

## 🎨 Design Philosophy

### Principle 1: Automation First

> "Scripts should run without human intervention by default."

**Benefits**:
- Enables background execution
- Supports scheduled runs
- Reduces manual effort
- Prevents interruptions

### Principle 2: Debug When Needed

> "Debug features should be opt-in, not always-on."

**Benefits**:
- Cleaner output in production
- Lower disk usage
- Faster execution
- Professional appearance

### Principle 3: Explicit Control

> "Users should have clear ways to control behavior."

**Benefits**:
- Predictable behavior
- Easy troubleshooting
- Flexible usage
- Better documentation

---

## 🧪 Testing

### Test Non-Interactive Mode

```bash
# Test that script runs without prompts
timeout 60 bash run_protox.sh 0 1
# Should complete without asking for input
```

### Test Debug Mode Off (Default)

```bash
# Ensure DEBUG_MODE is False
grep "DEBUG_MODE = False" config.py

# Run script
bash run_protox.sh 0 1

# Check that no debug screenshots were created
ls results/debug_*.png 2>/dev/null
# Should show: No such file or directory
```

### Test Debug Mode On

```bash
# Enable debug mode
sed -i 's/DEBUG_MODE = False/DEBUG_MODE = True/' config.py

# Run script
bash run_protox.sh 0 1

# Check that debug screenshots were created
ls results/debug_screenshots/debug_*.png
# Should show screenshot files

# Restore debug mode
sed -i 's/DEBUG_MODE = True/DEBUG_MODE = False/' config.py
```

### Test Background Execution

```bash
# Run in background
nohup bash run_protox.sh 0 1 > test.log 2>&1 &

# Wait for completion
wait

# Check log
cat test.log
# Should show complete execution without errors
```

---

## 🐛 Troubleshooting

### Issue: Script Still Asks for Input

**Possible causes**:
1. Using old version of run_protox.sh
2. Cached script in memory

**Solution**:
```bash
# Update to latest version
git pull origin master

# Verify changes
grep -n "read -p" run_protox.sh
# Should return no results

# Run again
bash run_protox.sh
```

### Issue: Debug Screenshots Not Saving

**Possible causes**:
1. DEBUG_MODE is False
2. Permission issues

**Solution**:
```bash
# Check DEBUG_MODE
grep "DEBUG_MODE" config.py

# Enable if needed
sed -i 's/DEBUG_MODE = False/DEBUG_MODE = True/' config.py

# Check directory permissions
ls -ld results/debug_screenshots/

# Create directory if needed
mkdir -p results/debug_screenshots
chmod 755 results/debug_screenshots
```

### Issue: Want to Regenerate Files

**Solution**:
```bash
# Delete files you want to regenerate
rm data/canonical_smiles.csv
rm results/CID_*.csv

# Run script - it will regenerate automatically
bash run_protox.sh
```

---

## 📚 Related Documentation

- [config.py](config.py) - Configuration file with DEBUG_MODE
- [run_protox.sh](run_protox.sh) - Main workflow script
- [src/protox_full_automation.py](src/protox_full_automation.py) - Automation script
- [OPTIMIZATION_NOTES.md](OPTIMIZATION_NOTES.md) - Other optimizations
- [CONFIG_REFACTORING.md](CONFIG_REFACTORING.md) - Configuration improvements

---

## 🎉 Summary

### What Changed

| Component | Change | Impact |
|-----------|--------|--------|
| **run_protox.sh** | Removed 2 interactive prompts | Enables unattended execution |
| **config.py** | Added DEBUG_MODE setting | Controls debug features |
| **protox_full_automation.py** | Conditional screenshot saving | Cleaner results directory |

### Benefits

1. ✅ **Fully automated** - No user input required
2. ✅ **Background friendly** - Can run with nohup or screen
3. ✅ **Batch processing** - Process multiple ranges in parallel
4. ✅ **Scheduled runs** - Works with cron jobs
5. ✅ **Clean output** - Debug files only when needed
6. ✅ **Better organized** - Debug files in separate directory
7. ✅ **Flexible control** - Easy to enable/disable debug mode

### User Impact

**Before**:
```bash
bash run_protox.sh
# Regenerate canonical SMILES? (y/n) ← Waits for input
# Continue with prediction? (y/n) ← Waits for input
# Creates debug_*.png in results/ ← Clutters directory
```

**After**:
```bash
bash run_protox.sh
# Runs automatically without prompts ✅
# No debug files unless DEBUG_MODE=True ✅
# Can run in background ✅
```

**Result**: Fully automated, production-ready workflow!

---

**Last Updated**: 2026-01-09  
**Version**: 1.3.0  
**Status**: ✅ Non-Interactive

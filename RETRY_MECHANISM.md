# Retry Mechanism and Failure Recovery

## 📝 Overview

This document describes the automatic retry mechanism and failure recovery features that handle timeout errors and processing failures.

---

## 🎯 Features

### 1. Automatic Retry on Failure

**Problem**: Some compounds may fail due to temporary issues (network timeout, server overload, etc.)

**Solution**: Automatically retry failed compounds up to a configurable number of times.

### 2. Failure Recovery

**Problem**: After processing all compounds, some may still fail after all retry attempts.

**Solution**: Identify failed compounds and provide easy reprocessing.

---

## 🔧 Retry Mechanism

### Configuration

**In config.py**:
```python
RETRY_TIMES = 3  # Number of retry attempts on failure (default: 3)
```

**Customization**:
```python
# Example: Increase retries for unstable connections
RETRY_TIMES = 5

# Example: Disable retries (not recommended)
RETRY_TIMES = 1
```

### How It Works

When processing a compound:

```
Attempt 1: Process compound
  ↓
  Failed? → Wait 10 seconds → Attempt 2
  ↓
  Failed? → Wait 10 seconds → Attempt 3
  ↓
  Failed? → Mark as failed, continue to next compound
  ↓
Success? → Save result, continue to next compound
```

### Log Output

**Successful on first attempt**:
```
[1/97] Processing compound 311434
✓ Compound 311434 processed successfully
```

**Successful on retry**:
```
[2/97] Processing compound 16129701
  ⚠ Attempt 1 failed, retrying...
  Retry attempt 1/2
✓ Compound 16129701 processed successfully
```

**Failed after all retries**:
```
[3/97] Processing compound 54576693
  ⚠ Attempt 1 failed, retrying...
  Retry attempt 1/2
  ⚠ Attempt 2 failed, retrying...
  Retry attempt 2/2
✗ Compound 54576693 processing failed after 3 attempts
```

---

## 🔄 Failure Recovery

### Identify Failed Compounds

**Run the analysis script**:
```bash
python3 src/retry_failed.py
```

**Output**:
```
======================================================================
Failed Compounds Analysis
======================================================================

Reading input file: /path/to/data/canonical_smiles.csv
  Total compounds in input: 97

Analyzing log file: /path/to/logs/processing_log.txt
  Successful from log: 92
  Failed from log: 5

Checking results directory: /path/to/results
  Compounds with result files: 92

======================================================================
Found 5 failed compounds:
======================================================================

  1. PubChem_ID: 16129701
  2. PubChem_ID: 54576693
  3. PubChem_ID: 71584930
  4. PubChem_ID: 9839311
  5. PubChem_ID: 121280087

✓ Failed compounds list saved to: /path/to/data/failed_compounds.csv

Options:
  1. Retry all failed compounds now
  2. Save list and retry manually later
  3. Exit without retrying

Enter your choice (1/2/3):
```

### Automatic Retry

**Option 1: Interactive mode**
```bash
python3 src/retry_failed.py
# Choose option 1 when prompted
```

**Option 2: Automatic mode**
```bash
python3 src/retry_failed.py --auto
# Automatically retries without prompting
```

### Manual Retry

**Option 1: Use the failed compounds list**
```bash
# The script saves failed compounds to data/failed_compounds.csv
# You can manually review and process them

# Copy to input file
cp data/failed_compounds.csv data/input.csv

# Run the workflow
bash run_protox.sh
```

**Option 2: Process specific compounds**
```bash
# Edit failed_compounds.csv to select specific compounds
nano data/failed_compounds.csv

# Copy to input file
cp data/failed_compounds.csv data/input.csv

# Run conversion and prediction
python3 src/convert_smiles.py data/input.csv data/canonical_smiles.csv
python3 src/protox_full_automation.py
```

---

## 📊 Analysis Logic

### How Failed Compounds Are Identified

The script uses multiple sources to identify failures:

1. **Log File Analysis**
   - Searches for "✓ Compound X processed successfully"
   - Searches for "✗ Compound X processing failed"

2. **Result Files Check**
   - Lists all `CID_*.csv` files in results directory
   - Extracts PubChem_IDs from filenames

3. **Cross-Reference**
   - Compound is considered failed if:
     - No result file exists, OR
     - Marked as failed in log AND not marked as successful

### Example Scenarios

| Scenario | Log Status | Result File | Identified As |
|----------|-----------|-------------|---------------|
| Normal success | ✓ Success | Exists | Success |
| Failed all retries | ✗ Failed | Missing | **Failed** |
| Partial log | Not mentioned | Missing | **Failed** |
| Retry success | ✗ Failed, then ✓ Success | Exists | Success |
| Interrupted | Not mentioned | Exists | Success |

---

## 🎨 Best Practices

### 1. Monitor Long Runs

For long processing runs:

```bash
# Run in background
nohup bash run_protox.sh > protox.log 2>&1 &

# Monitor progress
tail -f logs/processing_log.txt

# Check for failures
grep "failed after" logs/processing_log.txt
```

### 2. Adjust Retry Settings

**For stable connections**:
```python
# config.py
RETRY_TIMES = 2  # Fewer retries needed
MAX_WAIT_TIME = 600  # 10 minutes timeout
```

**For unstable connections**:
```python
# config.py
RETRY_TIMES = 5  # More retries
MAX_WAIT_TIME = 1200  # 20 minutes timeout
```

### 3. Batch Processing with Recovery

**Process in batches**:
```bash
# Batch 1
bash run_protox.sh 0 25

# Check for failures
python3 src/retry_failed.py

# Batch 2
bash run_protox.sh 25 50

# Check for failures
python3 src/retry_failed.py

# And so on...
```

### 4. Scheduled Retry

**Use cron for automatic retry**:
```bash
# Edit crontab
crontab -e

# Add retry job (runs daily at 3 AM)
0 3 * * * cd /path/to/ProTox3-Automation && python3 src/retry_failed.py --auto >> /path/to/retry.log 2>&1
```

---

## 🧪 Testing

### Test Retry Mechanism

**Simulate a failure** (temporarily reduce timeout):
```python
# Edit config.py
MAX_WAIT_TIME = 10  # Very short timeout to force failure

# Run on one compound
python3 src/protox_full_automation.py 0 1

# Check log for retry attempts
grep "Retry attempt" logs/processing_log.txt

# Restore timeout
# Edit config.py back to MAX_WAIT_TIME = 900
```

### Test Failure Recovery

**Create test scenario**:
```bash
# Process some compounds
python3 src/protox_full_automation.py 0 5

# Manually delete one result file
rm results/CID_311434.csv

# Run failure analysis
python3 src/retry_failed.py

# Should identify CID_311434 as failed
```

---

## 📈 Statistics and Reporting

### View Retry Statistics

**From log file**:
```bash
# Count retry attempts
grep "Retry attempt" logs/processing_log.txt | wc -l

# Count failed compounds
grep "processing failed after" logs/processing_log.txt | wc -l

# List failed compounds
grep "processing failed after" logs/processing_log.txt | \
  sed 's/.*Compound \([0-9]*\).*/\1/'
```

### Generate Report

**Create a summary**:
```bash
# Total compounds
total=$(grep "Total compounds in file:" logs/processing_log.txt | \
  tail -1 | awk '{print $NF}')

# Successful
success=$(grep "Successful:" logs/processing_log.txt | \
  tail -1 | awk '{print $NF}')

# Failed
failed=$(grep "Failed:" logs/processing_log.txt | \
  tail -1 | awk '{print $NF}')

# Display
echo "Processing Summary:"
echo "  Total: $total"
echo "  Success: $success"
echo "  Failed: $failed"
echo "  Success Rate: $(( success * 100 / total ))%"
```

---

## 🐛 Troubleshooting

### Issue: All Compounds Failing

**Possible causes**:
1. ProTox-3 website is down
2. Network connection issues
3. WebDriver problems

**Solution**:
```bash
# Check website accessibility
curl -I https://tox.charite.de/protox3/

# Test with a single compound manually
python3 src/protox_full_automation.py 0 1

# Enable debug mode
# Edit config.py: DEBUG_MODE = True

# Check debug screenshots
ls results/debug_screenshots/
```

### Issue: Retry Script Not Finding Failures

**Possible causes**:
1. Log file in different location
2. Results directory path incorrect

**Solution**:
```bash
# Check paths in config.py
python3 src/get_config.py PROCESSING_LOG_FILE
python3 src/get_config.py RESULTS_DIR

# Verify files exist
ls -l logs/processing_log.txt
ls -l results/CID_*.csv | head
```

### Issue: Too Many Retries Slowing Down

**Problem**: With `RETRY_TIMES = 5`, each failure takes 50+ minutes

**Solution**:
```python
# Reduce retries for first pass
RETRY_TIMES = 2

# Then use retry_failed.py for remaining failures
# This is more efficient than many retries per compound
```

---

## 📚 Related Documentation

- [config.py](config.py) - Configuration including RETRY_TIMES
- [src/protox_full_automation.py](src/protox_full_automation.py) - Main script with retry logic
- [src/retry_failed.py](src/retry_failed.py) - Failure recovery script
- [NON_INTERACTIVE_MODE.md](NON_INTERACTIVE_MODE.md) - Background execution
- [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - General troubleshooting

---

## 🎉 Summary

### What Was Added

| Feature | Description | Benefit |
|---------|-------------|---------|
| **Automatic Retry** | Retry failed compounds up to N times | Handles temporary failures |
| **Configurable Retries** | Set RETRY_TIMES in config.py | Flexible for different scenarios |
| **Failure Analysis** | Identify failed compounds from log and results | Know what needs reprocessing |
| **Easy Recovery** | One command to retry all failures | Simple failure recovery |
| **Detailed Logging** | Log each retry attempt | Better debugging |

### Benefits

1. ✅ **Resilient Processing** - Handles temporary failures automatically
2. ✅ **Configurable** - Adjust retry behavior for your needs
3. ✅ **Easy Recovery** - Simple workflow for handling persistent failures
4. ✅ **Transparent** - Clear logging of all retry attempts
5. ✅ **Efficient** - Don't waste time on manual retries
6. ✅ **Complete** - Ensure all compounds are processed

### Workflow

**Normal Processing**:
```
bash run_protox.sh
  ↓
Automatic retries handle temporary failures
  ↓
Most compounds succeed
```

**Failure Recovery**:
```
python3 src/retry_failed.py
  ↓
Identifies remaining failures
  ↓
Option to retry automatically
  ↓
All compounds processed
```

**Result**: Robust, resilient, production-ready workflow!

---

**Last Updated**: 2026-01-10  
**Version**: 1.4.0  
**Status**: ✅ Retry Mechanism Implemented

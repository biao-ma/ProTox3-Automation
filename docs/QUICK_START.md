# Quick Start Guide

Get started with ProTox3-Automation in just a few steps!

## 🚀 Super Quick Start (3 Steps)

### Step 1: Clone and Install

```bash
git clone https://github.com/biao-ma/ProTox3-Automation.git
cd ProTox3-Automation
bash setup.sh
```

### Step 2: Prepare Your Data

Create or copy your input CSV file to `data/input.csv`:

```csv
PubChem_ID,SMILES
311434,CC1=CC(=NO1)NC(=O)NC2=CC(=C(C=C2OC)OC)Cl
54576693,C1CN(CCN1CC2=CC3=C(C=C2)OC(O3)(F)F)C(=O)NC4=C(C=CN=C4)Cl
121280087,CN(C)CCN(C)C1=CC(=C(C=C1NC(=O)C=C)NC2=NC=CC(=N2)C3=CN(C4=CC=CC=C43)C5CC5)OC
```

**Or use the example data:**

```bash
cp data/example_input.csv data/input.csv
```

### Step 3: Run the Complete Workflow

```bash
bash run_protox.sh
```

That's it! The script will automatically:
1. ✅ Check and setup the environment
2. ✅ Convert SMILES to Canonical format
3. ✅ Run toxicity predictions
4. ✅ Extract and aggregate results

---

## 📋 What the Script Does

The `run_protox.sh` script handles the entire workflow:

```
┌─────────────────────────────────────────────────────────┐
│  Step 1: Setup Virtual Environment                      │
│  • Check/create venv                                    │
│  • Install dependencies                                 │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  Step 2: Check Input Data                               │
│  • Verify input.csv exists                              │
│  • Count compounds                                      │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  Step 3: Convert SMILES                                 │
│  • Run convert_smiles.py                                │
│  • Generate canonical_smiles.csv                        │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  Step 4: Run Toxicity Predictions                       │
│  • Process each compound via ProTox-3                   │
│  • Save individual reports (CID_*.csv)                  │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  Step 5: Extract and Aggregate Results                  │
│  • Extract Cytotoxicity data                            │
│  • Create summary file                                  │
└─────────────────────────────────────────────────────────┘
                         ↓
                    ✅ Done!
```

---

## 🎯 Usage Examples

### Process All Compounds

```bash
bash run_protox.sh
```

This will process all compounds in your input file.

### Process Specific Range

```bash
# Process compounds 0-10
bash run_protox.sh 0 10

# Process compounds 10-20
bash run_protox.sh 10 20

# Process compounds 20 to end
bash run_protox.sh 20
```

### Run in Background

```bash
# Run in background and save output to log
nohup bash run_protox.sh > workflow.log 2>&1 &

# Monitor progress
tail -f workflow.log
tail -f logs/processing_log.txt
```

---

## ⏱️ Time Estimates

| Compounds | Processing Time |
|-----------|-----------------|
| 1 compound | 5-10 minutes |
| 10 compounds | 1-2 hours |
| 50 compounds | 4-8 hours |
| 100 compounds | 8-16 hours |

**Note**: Each compound takes approximately 5-10 minutes to process.

---

## 📊 Output Files

After running the workflow, you'll find:

### 1. Individual Compound Reports

Location: `results/CID_{PubChem_ID}.csv`

Example: `results/CID_311434.csv`

```csv
Classification,Target,Shorthand,Prediction,Probability
Organ toxicity,Hepatotoxicity,dili,Active,0.62
Organ toxicity,Neurotoxicity,neuro,Active,0.61
...
Toxicity end points,Cytotoxicity,cyto,Inactive,0.62
...
```

### 2. Aggregated Summary

Location: `results/cytotoxicity_summary.csv`

```csv
PubChem_ID,Classification,Target,Shorthand,Prediction,Probability
311434,Toxicity end points,Cytotoxicity,cyto,Inactive,0.62
54576693,Toxicity end points,Cytotoxicity,cyto,Active,0.71
121280087,Toxicity end points,Cytotoxicity,cyto,Inactive,0.58
```

### 3. Processing Log

Location: `logs/processing_log.txt`

Contains detailed logs of the entire process.

---

## 🔍 Monitoring Progress

### During Processing

```bash
# Watch the main log
tail -f logs/processing_log.txt

# Check how many compounds are done
ls results/CID_*.csv | wc -l

# View the latest result
ls -t results/CID_*.csv | head -1 | xargs cat
```

### After Processing

```bash
# View summary
cat results/cytotoxicity_summary.csv

# Count results
wc -l results/cytotoxicity_summary.csv

# View statistics
head -20 results/cytotoxicity_summary.csv
```

---

## 🛠️ Troubleshooting

### Issue: "Input file not found"

**Solution**: Create your input file:

```bash
# Option 1: Use example data
cp data/example_input.csv data/input.csv

# Option 2: Create your own
nano data/input.csv
```

### Issue: "SMILES conversion failed"

**Solution**: Check your SMILES format:

```bash
# View the input file
cat data/input.csv

# Ensure it has the correct format:
# PubChem_ID,SMILES
# 311434,CC1=CC(=NO1)...
```

### Issue: "Permission denied"

**Solution**: Ensure the script is executable:

```bash
chmod +x run_protox.sh
chmod +x setup.sh
```

### Issue: "Virtual environment not found"

**Solution**: Run setup first:

```bash
bash setup.sh
```

---

## 💡 Tips

### 1. Test with Small Dataset First

```bash
# Create a test file with 3 compounds
head -4 data/input.csv > data/test_input.csv

# Process test file
cp data/test_input.csv data/input.csv
bash run_protox.sh
```

### 2. Process in Batches

For large datasets, process in batches:

```bash
# Batch 1: 0-25
bash run_protox.sh 0 25

# Batch 2: 25-50
bash run_protox.sh 25 50

# Batch 3: 50-75
bash run_protox.sh 50 75

# Batch 4: 75-100
bash run_protox.sh 75 100
```

### 3. Resume After Interruption

The script checks for existing files:
- If `canonical_smiles.csv` exists, it asks if you want to regenerate
- Individual compound reports are not overwritten
- You can resume by specifying the start index

```bash
# If interrupted at compound 30, resume from there
bash run_protox.sh 30
```

### 4. Monitor System Resources

```bash
# Check CPU and memory usage
top

# Check disk space
df -h

# Check process
ps aux | grep python
```

---

## 📚 Next Steps

After getting your results:

1. **Analyze the data**
   ```bash
   # View summary
   cat results/cytotoxicity_summary.csv
   
   # Count active vs inactive
   grep "Active" results/cytotoxicity_summary.csv | wc -l
   grep "Inactive" results/cytotoxicity_summary.csv | wc -l
   ```

2. **Export for further analysis**
   - Import into Excel/LibreOffice
   - Use Python/R for statistical analysis
   - Create visualizations

3. **Review individual reports**
   ```bash
   # View a specific compound
   cat results/CID_311434.csv
   
   # Check all predictions for a compound
   head -50 results/CID_311434.csv
   ```

---

## 🆘 Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Review the [Configuration Guide](CONFIGURATION.md)
3. Check the [Processing Log](../logs/processing_log.txt)
4. Open an issue on [GitHub](https://github.com/biao-ma/ProTox3-Automation/issues)

---

## 📖 Additional Documentation

- [Installation Guide](INSTALLATION.md) - Detailed installation instructions
- [User Guide](USER_GUIDE.md) - Complete user manual
- [Configuration Guide](CONFIGURATION.md) - Customization options
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and solutions

---

**Happy predicting!** 🎉

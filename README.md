# ProTox3-Automation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![ProTox-3](https://img.shields.io/badge/ProTox-3.0-green.svg)](https://tox.charite.de/protox3/)

**Languages**: [English](README.md) | [中文](README.zh-CN.md) | [日本語](README.ja.md)

**ProTox3-Automation** is a comprehensive automation toolkit for batch processing toxicity predictions of chemical compounds, with a focus on extracting **Cytotoxicity** prediction results.

## ✨ Core Features

- 🔄 **SMILES Conversion** - Automatically convert SMILES to Canonical format
- 🤖 **Batch Prediction** - Automated access to ProTox-3 website for toxicity predictions
- 📊 **Data Extraction** - Extract Cytotoxicity data from prediction results
- 📈 **Results Aggregation** - Consolidate all results into a single CSV file
- 🚀 **Efficient Processing** - Support for batch processing and background execution

## 🎯 Use Cases

- Toxicity assessment in drug development
- Safety screening of chemical compounds
- Toxicity prediction in academic research
- Large-scale toxicity analysis of compound libraries

## 📋 System Requirements

- Python 3.7+
- Chrome/Chromium browser
- Stable internet connection
- At least 1GB available disk space

## 🚀 Quick Start

### One-Click Installation (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/biao-ma/ProTox3-Automation.git
cd ProTox3-Automation

# 2. One-time setup (installs all dependencies)
bash setup.sh

# 3. Prepare your input data
cp data/example_input.csv data/input.csv
# Edit data/input.csv with your compounds

# 4. Run the complete workflow (fast start, no installation)
bash run_protox.sh
```

**Note**: `setup.sh` only needs to be run once. Subsequent runs of `run_protox.sh` will start immediately without reinstalling dependencies (~5 seconds vs ~2 minutes).

### Manual Installation

```bash
# 1. Clone the repository
git clone https://github.com/biao-ma/ProTox3-Automation.git
cd ProTox3-Automation

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Prepare data
# Place your CSV file in the data/ directory with PubChem_ID and SMILES columns

# 5. Run the script
python3 src/protox_full_automation.py
```

## 📊 Usage Examples

### Process All Compounds

```bash
python3 src/protox_full_automation.py
```

### Process Specific Range of Compounds

```bash
# Process compounds 0-10
python3 src/protox_full_automation.py 0 10

# Process compounds 10-20
python3 src/protox_full_automation.py 10 20
```

### Run in Background

```bash
nohup python3 src/protox_full_automation.py > protox.log 2>&1 &
```

## 📁 Project Structure

```
ProTox3-Automation/
├── README.md                      # Project documentation (English)
├── README.zh-CN.md               # Chinese documentation
├── README.ja.md                  # Japanese documentation
├── LICENSE                        # License
├── requirements.txt               # Python dependencies
├── setup.sh                       # One-click installation script
├── run_protox.sh                  # Quick start script
├── data/                          # Data directory
│   └── example_input.csv         # Example input file
├── src/                           # Source code directory
│   ├── protox_full_automation.py # Main automation script
│   ├── extract_cytotoxicity.py   # Results aggregation script
│   └── convert_smiles.py         # SMILES conversion script
├── results/                       # Output directory
│   ├── CID_*.csv                 # Individual compound reports
│   └── cytotoxicity_summary.csv  # Final aggregated file
└── docs/                          # Documentation directory
    ├── QUICK_START.md            # Quick start guide
    ├── INSTALLATION.md           # Detailed installation guide
    ├── USER_GUIDE.md             # User guide
    └── TROUBLESHOOTING.md        # Troubleshooting guide
```

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Single compound | 5-10 minutes |
| 10 compounds | 1-2 hours |
| 100 compounds | 8-16 hours |

## 📊 Output Format

### Individual Compound Report (CID_*.csv)

```csv
Classification,Target,Shorthand,Prediction,Probability
Organ toxicity,Hepatotoxicity,dili,Active,0.62
Organ toxicity,Neurotoxicity,neuro,Active,0.61
...
Toxicity end points,Cytotoxicity,cyto,Inactive,0.62
...
```

### Aggregated File (cytotoxicity_summary.csv)

```csv
PubChem_ID,Classification,Target,Shorthand,Prediction,Probability
311434,Toxicity end points,Cytotoxicity,cyto,Inactive,0.62
54576693,Toxicity end points,Cytotoxicity,cyto,Active,0.71
...
```

## 🔧 Configuration Options

Customize the following options in `config.py`:

```python
# ProTox-3 website URL
PROTOX_URL = 'https://tox.charite.de/protox3/index.php?site=compound_input'

# Input file path
INPUT_FILE = 'data/input.csv'

# Output directory
OUTPUT_DIR = 'results/'

# Timeout setting (seconds)
MAX_WAIT_TIME = 900  # 15 minutes
```

## 📚 Documentation

- [Quick Start Guide](docs/QUICK_START.md)
- [Detailed Installation Guide](docs/INSTALLATION.md)
- [User Guide](docs/USER_GUIDE.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [API Documentation](docs/API.md)

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to participate.

### How to Contribute

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## ⚠️ Disclaimer

- This tool is for research and educational purposes only
- Please comply with ProTox-3 website terms of use
- Data should not be used for commercial purposes
- Prediction results are for reference only and should not be used as the sole basis for decision-making

## 🙏 Acknowledgments

- [ProTox-3](https://tox.charite.de/protox3/) - Providing toxicity prediction services
- [RDKit](https://www.rdkit.org/) - Cheminformatics toolkit
- [Selenium](https://www.selenium.dev/) - Browser automation tool

## 📞 Contact

- Issue Reports: [GitHub Issues](https://github.com/biao-ma/ProTox3-Automation/issues)
- Feature Requests: [GitHub Discussions](https://github.com/biao-ma/ProTox3-Automation/discussions)

## 🌟 Star History

If this project helps you, please give us a ⭐️!

---

**Last Updated**: 2026-01-08  
**Version**: 1.0.0

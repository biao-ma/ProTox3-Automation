# RDKit Installation Guide

RDKit is a critical dependency for SMILES conversion. This guide covers installation on different systems and Python versions.

## 🐍 Python Version Compatibility

| Python Version | rdkit-pypi | rdkit (conda) | Recommendation |
|----------------|------------|---------------|----------------|
| 3.7 - 3.11 | ✅ Yes | ✅ Yes | Use rdkit-pypi |
| 3.12 | ⚠️ Limited | ✅ Yes | Use conda |
| 3.13+ | ❌ No | ⚠️ Testing | Use conda or Python 3.11 |

---

## 📦 Installation Methods

### Method 1: pip (Recommended for Python 3.7-3.11)

```bash
# Activate virtual environment first
source venv/bin/activate

# Install rdkit-pypi
pip install rdkit-pypi
```

### Method 2: conda (Recommended for Python 3.12+)

```bash
# Install conda if not already installed
# Download from: https://docs.conda.io/en/latest/miniconda.html

# Create conda environment
conda create -n protox python=3.11
conda activate protox

# Install rdkit
conda install -c conda-forge rdkit

# Install other dependencies
pip install selenium requests beautifulsoup4
```

### Method 3: System Package Manager (Linux)

#### Ubuntu/Debian

```bash
# Install system package
sudo apt-get update
sudo apt-get install python3-rdkit

# Or use pip in virtual environment
python3 -m venv venv
source venv/bin/activate
pip install rdkit-pypi
```

#### Fedora/RHEL

```bash
sudo dnf install python3-rdkit
```

### Method 4: Build from Source (Advanced)

```bash
# Install dependencies
sudo apt-get install build-essential cmake python3-dev

# Clone and build
git clone https://github.com/rdkit/rdkit.git
cd rdkit
mkdir build && cd build
cmake ..
make
make install
```

---

## 🔧 Troubleshooting

### Issue 1: "No matching distribution found for rdkit-pypi"

**Cause**: Python version too new (3.13+) or too old (<3.7)

**Solution 1**: Use conda

```bash
conda create -n protox python=3.11
conda activate protox
conda install -c conda-forge rdkit
```

**Solution 2**: Downgrade Python

```bash
# Install Python 3.11
sudo apt-get install python3.11 python3.11-venv

# Create venv with Python 3.11
python3.11 -m venv venv
source venv/bin/activate
pip install rdkit-pypi
```

### Issue 2: "ImportError: No module named 'rdkit'"

**Cause**: RDKit not installed or not in Python path

**Solution**: Verify installation

```bash
# Check if rdkit is installed
pip list | grep rdkit

# Test import
python -c "from rdkit import Chem; print('RDKit OK')"

# If not found, reinstall
pip uninstall rdkit rdkit-pypi
pip install rdkit-pypi
```

### Issue 3: "ImportError: libRDKit*.so: cannot open shared object file"

**Cause**: Missing system libraries

**Solution**: Install system dependencies

```bash
# Ubuntu/Debian
sudo apt-get install libboost-all-dev

# Fedora/RHEL
sudo dnf install boost-devel
```

### Issue 4: Conda environment conflicts

**Cause**: Mixing pip and conda packages

**Solution**: Use conda for everything

```bash
# Create fresh conda environment
conda create -n protox_fresh python=3.11
conda activate protox_fresh

# Install all dependencies via conda
conda install -c conda-forge rdkit selenium requests beautifulsoup4 pandas numpy
```

---

## ✅ Verification

After installation, verify RDKit works:

```bash
# Activate environment
source venv/bin/activate  # or: conda activate protox

# Test RDKit
python << EOF
from rdkit import Chem

# Test SMILES conversion
smiles = "CC1=CC(=NO1)NC(=O)NC2=CC(=C(C=C2OC)OC)Cl"
mol = Chem.MolFromSmiles(smiles)
if mol:
    canonical = Chem.MolToSmiles(mol, canonical=True)
    print(f"✓ RDKit is working!")
    print(f"  Input: {smiles}")
    print(f"  Canonical: {canonical}")
else:
    print("✗ RDKit failed to parse SMILES")
EOF
```

Expected output:
```
✓ RDKit is working!
  Input: CC1=CC(=NO1)NC(=O)NC2=CC(=C(C=C2OC)OC)Cl
  Canonical: COc1cc(OC)c(NC(=O)Nc2cc(C)on2)cc1Cl
```

---

## 🐳 Docker Alternative

If installation is problematic, use Docker:

```dockerfile
# Dockerfile
FROM continuumio/miniconda3

# Install rdkit via conda
RUN conda install -c conda-forge rdkit selenium

# Copy project files
COPY . /app
WORKDIR /app

# Install other dependencies
RUN pip install -r requirements.txt

# Run
CMD ["bash", "run_protox.sh"]
```

Build and run:

```bash
docker build -t protox3-automation .
docker run -v $(pwd)/data:/app/data -v $(pwd)/results:/app/results protox3-automation
```

---

## 📋 Recommended Setup

### For Most Users (Python 3.7-3.11)

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Upgrade pip
pip install --upgrade pip

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify
python -c "from rdkit import Chem; print('RDKit OK')"
```

### For Python 3.12+ Users

```bash
# 1. Install conda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# 2. Create environment
conda create -n protox python=3.11
conda activate protox

# 3. Install rdkit
conda install -c conda-forge rdkit

# 4. Install other dependencies
pip install selenium requests beautifulsoup4

# 5. Verify
python -c "from rdkit import Chem; print('RDKit OK')"
```

### For WSL/Windows Users

```bash
# Use conda (more reliable on Windows)
# 1. Install Miniconda for Windows
# Download from: https://docs.conda.io/en/latest/miniconda.html

# 2. Open Anaconda Prompt
conda create -n protox python=3.11
conda activate protox

# 3. Install dependencies
conda install -c conda-forge rdkit
pip install selenium requests beautifulsoup4

# 4. Navigate to project
cd /path/to/ProTox3-Automation

# 5. Run
bash run_protox.sh
```

---

## 🔗 Additional Resources

- [RDKit Documentation](https://www.rdkit.org/docs/index.html)
- [RDKit Installation Guide](https://www.rdkit.org/docs/Install.html)
- [Conda Documentation](https://docs.conda.io/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

---

## 💡 Tips

1. **Use Python 3.11** - Best compatibility with all dependencies
2. **Use conda for RDKit** - More reliable than pip on some systems
3. **Keep environments separate** - Don't mix system and venv packages
4. **Update regularly** - `pip install --upgrade rdkit-pypi`
5. **Check compatibility** - Verify Python version before installing

---

**Last Updated**: 2026-01-09

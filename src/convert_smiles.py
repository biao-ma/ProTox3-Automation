#!/usr/bin/env python3
"""
Convert SMILES to Canonical SMILES using RDKit
Function: Read PubChem_ID and SMILES from CSV, convert to Canonical SMILES, save to new CSV

Usage:
    python3 convert_smiles.py [input_file] [output_file]
    
Examples:
    python3 convert_smiles.py
    python3 convert_smiles.py data/input.csv data/canonical_smiles.csv
"""

import csv
import sys
from pathlib import Path
from rdkit import Chem

# Add parent directory to path to import config
sys.path.insert(0, str(Path(__file__).parent.parent))
import config

def convert_to_canonical_smiles(smiles):
    """Convert SMILES to Canonical SMILES"""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        canonical_smiles = Chem.MolToSmiles(mol, canonical=True)
        return canonical_smiles
    except Exception as e:
        print(f"  ✗ Error converting SMILES: {e}")
        return None

def main():
    """Main function"""
    # Get input and output file paths from command line or use defaults
    if len(sys.argv) >= 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        input_file = config.INPUT_FILE
        output_file = config.CANONICAL_SMILES_FILE
    
    print("=" * 60)
    print("Converting SMILES to Canonical SMILES")
    print("=" * 60)
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print("")
    
    # Check if input file exists
    if not Path(input_file).exists():
        print(f"✗ Input file not found: {input_file}")
        print("\nPlease ensure your input CSV file contains:")
        print("  - PubChem_ID column")
        print("  - SMILES column")
        return
    
    # Read input CSV
    compounds = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            compounds.append(row)
    
    print(f"Total compounds in input file: {len(compounds)}")
    print("")
    
    # Convert SMILES to Canonical SMILES
    results = []
    success_count = 0
    fail_count = 0
    
    for idx, compound in enumerate(compounds, 1):
        pubchem_id = compound.get('PubChem_ID', '')
        smiles = compound.get('SMILES', '')
        
        print(f"[{idx}/{len(compounds)}] Processing PubChem_ID: {pubchem_id}")
        
        if not smiles:
            print(f"  ✗ SMILES is empty")
            fail_count += 1
            continue
        
        canonical_smiles = convert_to_canonical_smiles(smiles)
        
        if canonical_smiles:
            results.append({
                'PubChem_ID': pubchem_id,
                'Original_SMILES': smiles,
                'Canonical_SMILES': canonical_smiles
            })
            print(f"  ✓ Converted successfully")
            success_count += 1
        else:
            print(f"  ✗ Conversion failed")
            fail_count += 1
    
    print("")
    print(f"Conversion complete:")
    print(f"  Successful: {success_count}")
    print(f"  Failed: {fail_count}")
    print("")
    
    # Save results to output CSV
    if results:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['PubChem_ID', 'Original_SMILES', 'Canonical_SMILES'])
            writer.writeheader()
            writer.writerows(results)
        
        print(f"✓ Results saved to: {output_file}")
        print("")
    else:
        print("✗ No results to save")
    
    print("=" * 60)

if __name__ == "__main__":
    main()

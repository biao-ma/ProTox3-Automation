#!/usr/bin/env python3
"""
Extract Cytotoxicity Data from ProTox-3 Results
Function: Extract Cytotoxicity rows from all CID_*.csv files and aggregate into a summary file

Usage:
    python3 extract_cytotoxicity.py
"""

import csv
import os
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.insert(0, str(Path(__file__).parent.parent))
import config

# Configuration from config.py
RESULT_DIR = config.RESULTS_DIR
OUTPUT_FILE = config.CYTOTOXICITY_SUMMARY_FILE

def extract_cytotoxicity():
    """Extract Cytotoxicity data from all CID_*.csv files"""
    
    print("=" * 60)
    print("Extracting Cytotoxicity Data")
    print("=" * 60)
    print(f"Results directory: {RESULT_DIR}")
    print(f"Output file: {OUTPUT_FILE}")
    print("")
    
    # Check if results directory exists
    if not os.path.exists(RESULT_DIR):
        print(f"✗ Results directory not found: {RESULT_DIR}")
        return
    
    # Find all CID_*.csv files
    cid_files = []
    for filename in os.listdir(RESULT_DIR):
        if filename.startswith('CID_') and filename.endswith('.csv'):
            cid_files.append(filename)
    
    if not cid_files:
        print("✗ No CID_*.csv files found in results directory")
        return
    
    print(f"Found {len(cid_files)} CID files")
    print("")
    
    # Extract Cytotoxicity data
    cytotoxicity_data = []
    
    for filename in sorted(cid_files):
        filepath = os.path.join(RESULT_DIR, filename)
        pubchem_id = filename.replace('CID_', '').replace('.csv', '')
        
        print(f"Processing: {filename}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    # Check if this row contains Cytotoxicity data
                    if len(row) > 0 and 'Cytotoxicity' in ' '.join(row):
                        # Insert PubChem_ID as the first column
                        row_with_id = [pubchem_id] + row
                        cytotoxicity_data.append(row_with_id)
                        print(f"  ✓ Found Cytotoxicity data: {row}")
                        break
        except Exception as e:
            print(f"  ✗ Error reading file: {e}")
    
    print("")
    print(f"Total Cytotoxicity records extracted: {len(cytotoxicity_data)}")
    print("")
    
    # Save to summary file
    if cytotoxicity_data:
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            header = ['PubChem_ID', 'Classification', 'Target', 'Shorthand', 'Prediction', 'Probability']
            writer.writerow(header)
            
            # Write data
            for row in cytotoxicity_data:
                writer.writerow(row)
        
        print(f"✓ Summary file saved: {OUTPUT_FILE}")
        print("")
        
        # Display statistics
        active_count = sum(1 for row in cytotoxicity_data if 'Active' in row)
        inactive_count = sum(1 for row in cytotoxicity_data if 'Inactive' in row)
        
        print("Statistics:")
        print(f"  Total compounds: {len(cytotoxicity_data)}")
        print(f"  Active (cytotoxic): {active_count}")
        print(f"  Inactive (non-cytotoxic): {inactive_count}")
        print("")
    else:
        print("✗ No Cytotoxicity data found")
    
    print("=" * 60)
    print("Extraction Complete")
    print("=" * 60)

if __name__ == "__main__":
    extract_cytotoxicity()

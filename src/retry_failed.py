#!/usr/bin/env python3
"""
Retry Failed Compounds Script

This script analyzes the processing log and results directory to identify
compounds that failed to process, then creates a list for reprocessing.

Usage:
    python3 retry_failed.py [--auto]
    
Options:
    --auto    Automatically retry failed compounds without confirmation
    
Examples:
    python3 retry_failed.py           # Analyze and show failed compounds
    python3 retry_failed.py --auto    # Automatically retry failed compounds
"""

import os
import sys
import csv
import re
import argparse
from pathlib import Path

# Add parent directory to path to import config
sys.path.insert(0, str(Path(__file__).parent.parent))
import config

def parse_log_file(log_file):
    """Parse processing log to find failed compounds"""
    failed_compounds = set()
    successful_compounds = set()
    
    if not os.path.exists(log_file):
        print(f"Warning: Log file not found: {log_file}")
        return failed_compounds, successful_compounds
    
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Match successful processing
            success_match = re.search(r'✓ Compound (\d+) processed successfully', line)
            if success_match:
                pubchem_id = success_match.group(1)
                successful_compounds.add(pubchem_id)
            
            # Match failed processing
            fail_match = re.search(r'✗ Compound (\d+) processing failed', line)
            if fail_match:
                pubchem_id = fail_match.group(1)
                failed_compounds.add(pubchem_id)
    
    # Remove successful ones from failed set (in case of retries in same log)
    failed_compounds = failed_compounds - successful_compounds
    
    return failed_compounds, successful_compounds

def check_result_files(results_dir):
    """Check which compounds have result files"""
    compounds_with_results = set()
    
    if not os.path.exists(results_dir):
        print(f"Warning: Results directory not found: {results_dir}")
        return compounds_with_results
    
    # Find all CID_*.csv files
    for filename in os.listdir(results_dir):
        if filename.startswith('CID_') and filename.endswith('.csv'):
            # Extract PubChem_ID from filename
            pubchem_id = filename[4:-4]  # Remove 'CID_' and '.csv'
            compounds_with_results.add(pubchem_id)
    
    return compounds_with_results

def get_all_compounds(input_file):
    """Get all compounds from input file"""
    all_compounds = {}
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        return all_compounds
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pubchem_id = row['PubChem_ID']
            canonical_smiles = row['Canonical_SMILES']
            all_compounds[pubchem_id] = canonical_smiles
    
    return all_compounds

def identify_failed_compounds():
    """Identify compounds that need to be retried"""
    print("=" * 70)
    print("Failed Compounds Analysis")
    print("=" * 70)
    print()
    
    # Get all compounds
    print(f"Reading input file: {config.CANONICAL_SMILES_FILE}")
    all_compounds = get_all_compounds(config.CANONICAL_SMILES_FILE)
    total_compounds = len(all_compounds)
    print(f"  Total compounds in input: {total_compounds}")
    print()
    
    # Parse log file
    print(f"Analyzing log file: {config.PROCESSING_LOG_FILE}")
    failed_from_log, successful_from_log = parse_log_file(config.PROCESSING_LOG_FILE)
    print(f"  Successful from log: {len(successful_from_log)}")
    print(f"  Failed from log: {len(failed_from_log)}")
    print()
    
    # Check result files
    print(f"Checking results directory: {config.RESULTS_DIR}")
    compounds_with_results = check_result_files(config.RESULTS_DIR)
    print(f"  Compounds with result files: {len(compounds_with_results)}")
    print()
    
    # Identify truly failed compounds
    # Failed = (in input file) AND (no result file OR marked as failed in log)
    truly_failed = set()
    
    for pubchem_id in all_compounds.keys():
        has_result = pubchem_id in compounds_with_results
        marked_failed = pubchem_id in failed_from_log
        marked_success = pubchem_id in successful_from_log
        
        # Failed if: no result file, or marked as failed but not marked as success
        if not has_result or (marked_failed and not marked_success):
            truly_failed.add(pubchem_id)
    
    return truly_failed, all_compounds

def save_failed_list(failed_compounds, all_compounds, output_file):
    """Save failed compounds to a CSV file"""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['PubChem_ID', 'Canonical_SMILES'])
        
        for pubchem_id in sorted(failed_compounds, key=lambda x: int(x)):
            canonical_smiles = all_compounds[pubchem_id]
            writer.writerow([pubchem_id, canonical_smiles])
    
    print(f"✓ Failed compounds list saved to: {output_file}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Retry Failed Compounds')
    parser.add_argument('--auto', action='store_true',
                       help='Automatically retry failed compounds')
    args = parser.parse_args()
    
    # Identify failed compounds
    failed_compounds, all_compounds = identify_failed_compounds()
    
    if not failed_compounds:
        print("=" * 70)
        print("✓ No failed compounds found!")
        print("=" * 70)
        print()
        print("All compounds have been successfully processed.")
        return
    
    # Display failed compounds
    print("=" * 70)
    print(f"Found {len(failed_compounds)} failed compounds:")
    print("=" * 70)
    print()
    
    # Show first 20 failed compounds
    failed_list = sorted(failed_compounds, key=lambda x: int(x))
    display_count = min(20, len(failed_list))
    
    for i, pubchem_id in enumerate(failed_list[:display_count], 1):
        print(f"  {i}. PubChem_ID: {pubchem_id}")
    
    if len(failed_list) > display_count:
        print(f"  ... and {len(failed_list) - display_count} more")
    
    print()
    
    # Save failed compounds list
    failed_list_file = os.path.join(config.DATA_DIR, 'failed_compounds.csv')
    save_failed_list(failed_compounds, all_compounds, failed_list_file)
    print()
    
    # Offer to retry
    if args.auto:
        retry = True
        print("Auto mode: Retrying failed compounds...")
    else:
        print("Options:")
        print("  1. Retry all failed compounds now")
        print("  2. Save list and retry manually later")
        print("  3. Exit without retrying")
        print()
        
        choice = input("Enter your choice (1/2/3): ").strip()
        retry = (choice == '1')
    
    if retry:
        print()
        print("=" * 70)
        print("Retrying Failed Compounds")
        print("=" * 70)
        print()
        
        # Import and run the main automation script
        import subprocess
        
        # Create a temporary input file with only failed compounds
        temp_input = os.path.join(config.DATA_DIR, 'temp_retry_input.csv')
        save_failed_list(failed_compounds, all_compounds, temp_input)
        
        # Run protox_full_automation.py with the failed compounds
        script_path = os.path.join(os.path.dirname(__file__), 'protox_full_automation.py')
        
        print(f"Running: python3 {script_path} --input {temp_input}")
        print(f"Input file: {temp_input}")
        print()
        
        try:
            # Run the automation script with custom input file
            result = subprocess.run(
                [sys.executable, script_path, '--input', temp_input],
                check=False
            )
            
            if result.returncode == 0:
                print()
                print("=" * 70)
                print("✓ Retry completed successfully")
                print("=" * 70)
            else:
                print()
                print("=" * 70)
                print("⚠ Retry completed with some errors")
                print("=" * 70)
        finally:
            # Clean up temporary file
            if os.path.exists(temp_input):
                os.remove(temp_input)
                print(f"Temporary file removed: {temp_input}")
    else:
        print()
        print("=" * 70)
        print("To retry failed compounds later, run:")
        print(f"  python3 {__file__} --auto")
        print()
        print("Or manually process the failed compounds:")
        print(f"  1. Copy {failed_list_file} to {config.CANONICAL_SMILES_FILE}")
        print(f"  2. Run: bash run_protox.sh")
        print("=" * 70)

if __name__ == "__main__":
    main()

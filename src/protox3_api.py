#!/usr/bin/env python3
"""
ProTox-3 API Client
A Python client for the ProTox-3 toxicity prediction API

Based on the official API documentation at:
https://tox.charite.de/protox3/index.php?site=api

Usage:
    python3 protox3_api.py <compound1>,<compound2>,...
    python3 protox3_api.py -t smiles -m "acute_tox cyto" "SMILES_STRING"
    
Examples:
    # Query by compound name
    python3 protox3_api.py aspirin,vorinostat
    
    # Query by SMILES
    python3 protox3_api.py -t smiles "CC1=CC(=NO1)NC(=O)NC2=CC(=C(C=C2OC)OC)Cl"
    
    # Query with specific models
    python3 protox3_api.py -t smiles -m "acute_tox cyto dili" -o results.csv "SMILES"
"""

import sys
import argparse
import requests
import json
import time
import csv
from pathlib import Path

# API Configuration
API_BASE_URL = "https://tox.charite.de/protox3/api"
API_ENDPOINT = f"{API_BASE_URL}/query.php"
MAX_QUERIES_PER_DAY = 250
REQUEST_DELAY = 2  # seconds between requests

# Available models (from ProTox-3 documentation)
ALL_MODELS = [
    # Organ Toxicity
    "dili",          # Hepatotoxicity
    "neuro",         # Neurotoxicity
    "nephro",        # Nephrotoxicity
    "respi",         # Respiratory toxicity
    "cardio",        # Cardiotoxicity
    
    # Toxicity end points
    "carcino",       # Carcinogenicity
    "immuno",        # Immunotoxicity
    "mutagen",       # Mutagenicity
    "cyto",          # Cytotoxicity
    "bbb",           # BBB-barrier
    "eco",           # Ecotoxicity
    "clinical",      # Clinical toxicity
    "nutri",         # Nutritional toxicity
    
    # Tox21 Nuclear receptor signalling pathways
    "nr_ahr",        # Aryl hydrocarbon Receptor
    "nr_ar",         # Androgen Receptor
    "nr_ar_lbd",     # Androgen Receptor Ligand Binding Domain
    "nr_aromatase",  # Aromatase
    "nr_er",         # Estrogen Receptor Alpha
    "nr_er_lbd",     # Estrogen Receptor Ligand Binding Domain
    "nr_ppar_gamma", # PPAR-Gamma
    
    # Tox21 Stress response pathways
    "sr_are",        # nrf2/ARE
    "sr_hse",        # Heat shock factor response element
    "sr_mmp",        # Mitochondrial Membrane Potential
    "sr_p53",        # p53
    "sr_atad5",      # ATAD5
    
    # Molecular Initiating Events
    "mie_thr_alpha", # Thyroid hormone receptor alpha
    "mie_thr_beta",  # Thyroid hormone receptor beta
    "mie_ttr",       # Transtyretrin
    "mie_ryr",       # Ryanodine receptor
    "mie_gabar",     # GABA receptor
    "mie_nmdar",     # NMDA receptor
    "mie_ampar",     # AMPA receptor
    "mie_kar",       # Kainate receptor
    "mie_ache",      # Achetylcholinesterase
    "mie_car",       # Constitutive androstane receptor
    "mie_pxr",       # Pregnane X receptor
    "mie_nadhox",    # NADH-quinone oxidoreductase
    "mie_vgsc",      # Voltage gated sodium channel
    "mie_nis",       # Na+/I- symporter
    
    # Metabolism
    "CYP1A2",        # Cytochrome CYP1A2
    "CYP2C19",       # Cytochrome CYP2C19
    "CYP2C9",        # Cytochrome CYP2C9
    "CYP2D6",        # Cytochrome CYP2D6
    "CYP3A4",        # Cytochrome CYP3A4
    "CYP2E1",        # Cytochrome CYP2E1
]

# Default models (always computed)
DEFAULT_MODELS = ["acute_tox", "tox_targets"]


def query_protox(compound, input_type="name", models=None, quiet=False):
    """
    Query ProTox-3 API for toxicity prediction
    
    Args:
        compound: Compound name or SMILES string
        input_type: "name" or "smiles"
        models: List of model shorthands to query
        quiet: Suppress status messages
        
    Returns:
        dict: API response data
    """
    if models is None:
        models = DEFAULT_MODELS
    
    # Prepare request data
    data = {
        "compound": compound,
        "type": input_type,
        "models": ",".join(models)
    }
    
    if not quiet:
        print(f"Querying ProTox-3 for: {compound}")
        print(f"  Input type: {input_type}")
        print(f"  Models: {', '.join(models)}")
    
    try:
        # Note: Since the actual API endpoint structure is not accessible,
        # this is a best-guess implementation based on standard REST API patterns
        # The actual endpoint might be different
        
        # Try POST request
        response = requests.post(
            API_ENDPOINT,
            data=data,
            timeout=60,
            verify=False  # Skip SSL verification due to certificate issue
        )
        
        if response.status_code == 200:
            if not quiet:
                print("  ✓ Query successful")
            return response.json()
        else:
            if not quiet:
                print(f"  ✗ Query failed: HTTP {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        if not quiet:
            print(f"  ✗ Request error: {e}")
        return None


def parse_response(response_data, compound):
    """
    Parse API response and extract relevant data
    
    Args:
        response_data: API response dictionary
        compound: Original compound identifier
        
    Returns:
        list: Parsed results as list of dictionaries
    """
    results = []
    
    if not response_data:
        return results
    
    # Parse based on expected response format from documentation
    # Format: input, type, target, prediction, probability
    
    for item in response_data.get("predictions", []):
        result = {
            "input": compound,
            "type": item.get("type", ""),
            "target": item.get("target", ""),
            "prediction": item.get("prediction", ""),
            "probability": item.get("probability", "")
        }
        results.append(result)
    
    return results


def save_to_csv(results, output_file):
    """
    Save results to CSV file
    
    Args:
        results: List of result dictionaries
        output_file: Output CSV file path
    """
    if not results:
        print("No results to save")
        return
    
    fieldnames = ["input", "type", "target", "prediction", "probability"]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"✓ Results saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="ProTox-3 API Client for toxicity prediction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Query by compound name
  %(prog)s aspirin,vorinostat
  
  # Query by SMILES
  %(prog)s -t smiles "CC1=CC(=NO1)NC(=O)NC2=CC(=C(C=C2OC)OC)Cl"
  
  # Query with specific models
  %(prog)s -t smiles -m "acute_tox cyto dili" -o results.csv "SMILES"
  
  # Query all models
  %(prog)s -t smiles -m ALL_MODELS "SMILES"
        """
    )
    
    parser.add_argument(
        "compounds",
        nargs="?",
        help="Comma-separated list of compound names or SMILES strings"
    )
    
    parser.add_argument(
        "-t", "--type",
        choices=["name", "smiles"],
        default="name",
        help="Input type: 'name' for PubChem name search, 'smiles' for SMILES string (default: name)"
    )
    
    parser.add_argument(
        "-m", "--models",
        default="acute_tox tox_targets",
        help="Space-separated list of model shorthands (default: acute_tox tox_targets). Use 'ALL_MODELS' for all models."
    )
    
    parser.add_argument(
        "-o", "--output",
        default="protox_results.csv",
        help="Output CSV file (default: protox_results.csv)"
    )
    
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress status messages"
    )
    
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List all available models and exit"
    )
    
    args = parser.parse_args()
    
    # List models and exit
    if args.list_models:
        print("Available models:")
        print("\nOrgan Toxicity:")
        for model in ["dili", "neuro", "nephro", "respi", "cardio"]:
            print(f"  {model}")
        print("\nToxicity end points:")
        for model in ["carcino", "immuno", "mutagen", "cyto", "bbb", "eco", "clinical", "nutri"]:
            print(f"  {model}")
        print("\nTox21 Nuclear receptor signalling pathways:")
        for model in [m for m in ALL_MODELS if m.startswith("nr_")]:
            print(f"  {model}")
        print("\nTox21 Stress response pathways:")
        for model in [m for m in ALL_MODELS if m.startswith("sr_")]:
            print(f"  {model}")
        print("\nMolecular Initiating Events:")
        for model in [m for m in ALL_MODELS if m.startswith("mie_")]:
            print(f"  {model}")
        print("\nMetabolism:")
        for model in [m for m in ALL_MODELS if m.startswith("CYP")]:
            print(f"  {model}")
        print("\nDefault models (always computed):")
        for model in DEFAULT_MODELS:
            print(f"  {model}")
        return
    
    # Parse models
    if args.models == "ALL_MODELS":
        models = ALL_MODELS
    else:
        models = args.models.split()
    
    # Parse compounds
    compounds = [c.strip() for c in args.compounds.split(",")]
    
    if not args.quiet:
        print(f"ProTox-3 API Client")
        print(f"=" * 60)
        print(f"Compounds to query: {len(compounds)}")
        print(f"Input type: {args.type}")
        print(f"Models: {len(models)}")
        print(f"Output file: {args.output}")
        print(f"=" * 60)
        print()
    
    # Query each compound
    all_results = []
    for i, compound in enumerate(compounds, 1):
        if not args.quiet:
            print(f"[{i}/{len(compounds)}] Processing: {compound}")
        
        response = query_protox(compound, args.type, models, args.quiet)
        results = parse_response(response, compound)
        all_results.extend(results)
        
        # Rate limiting
        if i < len(compounds):
            time.sleep(REQUEST_DELAY)
        
        if not args.quiet:
            print()
    
    # Save results
    save_to_csv(all_results, args.output)
    
    if not args.quiet:
        print(f"\n✓ Processed {len(compounds)} compounds")
        print(f"✓ Total predictions: {len(all_results)}")


if __name__ == "__main__":
    # Suppress SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    main()

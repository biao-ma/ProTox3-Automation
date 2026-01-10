#!/usr/bin/env python3
"""
ProTox-3 Full Automation Script
Function: Batch process compound toxicity predictions, extract Cytotoxicity data, aggregate results

Usage:
    python3 protox_full_automation.py [start_index] [end_index]
    
Examples:
    python3 protox_full_automation.py          # Process all compounds
    python3 protox_full_automation.py 0 10    # Process compounds 0-10
    python3 protox_full_automation.py 10 20   # Process compounds 10-20
"""

import csv
import time
import os
import sys
import argparse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Add parent directory to path to import config
sys.path.insert(0, str(Path(__file__).parent.parent))
import config

# Configuration from config.py
PROTOX_URL = config.PROTOX_INPUT_URL
CANONICAL_SMILES_FILE = config.CANONICAL_SMILES_FILE
OUTPUT_DIR = config.RESULTS_DIR
LOG_FILE = config.PROCESSING_LOG_FILE
MAX_WAIT_TIME = config.MAX_WAIT_TIME

def log_message(message):
    """Log message to log file and console"""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry + '\n')

def create_driver():
    """Create Chrome WebDriver with SSL certificate handling"""
    chrome_options = Options()
    
    if config.HEADLESS_MODE:
        chrome_options.add_argument('--headless=new')  # Use new headless mode
    
    # Basic options
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    # SSL certificate handling
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument('--allow-insecure-localhost')
    chrome_options.add_argument('--allow-running-insecure-content')
    
    # Anti-detection
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Additional stability options
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--disable-features=IsolateOrigins,site-per-process')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # Set page load strategy
    chrome_options.page_load_strategy = 'normal'
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        log_message("✓ WebDriver created successfully")
        return driver
    except Exception as e:
        log_message(f"✗ Failed to create WebDriver: {e}")
        import traceback
        traceback.print_exc()
        return None

def extract_cytotoxicity_data(driver):
    """Extract Cytotoxicity data from the page"""
    try:
        script = """
        const tables = document.querySelectorAll('table');
        let cytotoxicityData = null;
        
        tables.forEach(table => {
            const rows = table.querySelectorAll('tr');
            rows.forEach(row => {
                const text = row.textContent;
                if (text.includes('Cytotoxicity')) {
                    const cells = row.querySelectorAll('td');
                    if (cells.length > 0) {
                        const rowData = [];
                        cells.forEach(cell => {
                            rowData.push(cell.textContent.trim());
                        });
                        cytotoxicityData = rowData;
                    }
                }
            });
        });
        
        return cytotoxicityData;
        """
        
        result = driver.execute_script(script)
        return result
    except Exception as e:
        log_message(f"✗ Failed to extract Cytotoxicity data: {e}")
        return None

def process_compound(driver, pubchem_id, canonical_smiles):
    """Process a single compound"""
    try:
        log_message(f"Processing compound: PubChem_ID={pubchem_id}")
        
        # Navigate to ProTox-3 input page
        log_message(f"  Navigating to {PROTOX_URL}")
        try:
            driver.get(PROTOX_URL)
            time.sleep(5)  # Increased wait time for SSL certificate handling
        except Exception as e:
            log_message(f"  ✗ Navigation failed: {e}")
            log_message("  Trying to handle SSL certificate warning...")
            try:
                # Try to click through SSL warning if present
                driver.execute_script("window.stop();")
                time.sleep(2)
                driver.get(PROTOX_URL)
                time.sleep(5)
            except:
                pass
        
        # Check if page loaded successfully
        log_message(f"  Current URL: {driver.current_url}")
        log_message(f"  Page title: {driver.title}")
        
        # Save screenshot for debugging (only if DEBUG_MODE is enabled)
        if config.DEBUG_MODE:
            try:
                screenshot_path = os.path.join(config.DEBUG_SCREENSHOT_DIR, f"debug_{pubchem_id}_page.png")
                driver.save_screenshot(screenshot_path)
                log_message(f"  Screenshot saved: {screenshot_path}")
            except Exception as e:
                log_message(f"  Warning: Failed to save screenshot: {e}")
        
        # Find and fill SMILES input field
        log_message("  Filling SMILES input field...")
        try:
            # Use ID instead of NAME - the field has id="smiles_field"
            smiles_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "smiles_field"))
            )
        except TimeoutException:
            log_message("  ✗ Timeout waiting for SMILES input field")
            log_message("  Checking page source for debugging...")
            page_source = driver.page_source[:500]  # First 500 chars
            log_message(f"  Page source preview: {page_source}")
            raise
        smiles_input.clear()
        smiles_input.send_keys(canonical_smiles)
        log_message("  ✓ SMILES input filled")
        
        # Click SMILES button (submit button next to SMILES field)
        log_message("  Clicking SMILES button...")
        # The SMILES button is a submit button with type="submit" after the smiles_field
        smiles_button = driver.find_element(By.XPATH, "//input[@id='smiles_field']/following-sibling::input[@type='submit']")
        smiles_button.click()
        time.sleep(2)
        log_message("  ✓ SMILES button clicked")
        
        # Click All button
        log_message("  Clicking All button...")
        all_button = driver.find_element(By.ID, "button_all")
        all_button.click()
        time.sleep(1)
        log_message("  ✓ All button clicked")
        
        # Click Start Tox-Prediction button
        log_message("  Clicking Start Tox-Prediction button...")
        start_button = driver.find_element(By.ID, "start_pred")
        start_button.click()
        log_message("  ✓ Start button clicked, waiting for results...")
        
        # Wait for results page (up to MAX_WAIT_TIME seconds)
        wait_time = 0
        max_wait = MAX_WAIT_TIME
        while wait_time < max_wait:
            time.sleep(30)
            wait_time += 30
            log_message(f"  Waiting... ({wait_time}/{max_wait} seconds)")
            
            # Check if results are ready
            try:
                if "Toxicity Model Report" in driver.page_source:
                    log_message("  ✓ Results page loaded")
                    break
            except:
                pass
        
        if wait_time >= max_wait:
            log_message(f"  ✗ Timeout waiting for results (>{max_wait}s)")
            return False
        
        # Extract Cytotoxicity data
        log_message("  Extracting Cytotoxicity data...")
        cyto_data = extract_cytotoxicity_data(driver)
        
        if cyto_data and len(cyto_data) >= 5:
            log_message(f"  ✓ Cytotoxicity data extracted: {cyto_data}")
            
            # Save individual compound report
            output_file = os.path.join(OUTPUT_DIR, f"CID_{pubchem_id}.csv")
            
            # Extract all toxicity data from the page
            script = """
            const tables = document.querySelectorAll('table');
            const allData = [];
            
            tables.forEach(table => {
                const rows = table.querySelectorAll('tr');
                rows.forEach((row, index) => {
                    const cells = row.querySelectorAll('td, th');
                    if (cells.length > 0) {
                        const rowData = [];
                        cells.forEach(cell => {
                            rowData.push(cell.textContent.trim());
                        });
                        allData.push(rowData);
                    }
                });
            });
            
            return allData;
            """
            
            all_data = driver.execute_script(script)
            
            # Save to CSV
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for row in all_data:
                    if row:  # Skip empty rows
                        writer.writerow(row)
            
            log_message(f"  ✓ Saved report to: {output_file}")
            return True
        else:
            log_message("  ✗ Failed to extract Cytotoxicity data")
            return False
            
    except Exception as e:
        log_message(f"  ✗ Error processing compound {pubchem_id}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='ProTox-3 Automation Script')
    parser.add_argument('start', type=int, nargs='?', default=0, 
                       help='Start index (default: 0)')
    parser.add_argument('end', type=int, nargs='?', default=None, 
                       help='End index (default: all)')
    args = parser.parse_args()
    
    start_idx = args.start
    end_idx = args.end
    
    log_message("=" * 60)
    log_message("ProTox-3 Automation Script Started")
    log_message("=" * 60)
    log_message(f"Configuration:")
    log_message(f"  Input file: {CANONICAL_SMILES_FILE}")
    log_message(f"  Output directory: {OUTPUT_DIR}")
    log_message(f"  Log file: {LOG_FILE}")
    log_message(f"  Start index: {start_idx}")
    log_message(f"  End index: {end_idx if end_idx else 'all'}")
    log_message("")
    
    # Check if input file exists
    if not os.path.exists(CANONICAL_SMILES_FILE):
        log_message(f"✗ Input file not found: {CANONICAL_SMILES_FILE}")
        log_message("Please run convert_smiles.py first to generate canonical SMILES")
        return
    
    # Read compounds from CSV
    compounds = []
    with open(CANONICAL_SMILES_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            compounds.append(row)
    
    total_compounds = len(compounds)
    log_message(f"Total compounds in file: {total_compounds}")
    
    # Determine processing range
    if end_idx is None:
        end_idx = total_compounds
    
    compounds_to_process = compounds[start_idx:end_idx]
    log_message(f"Processing compounds {start_idx} to {end_idx} ({len(compounds_to_process)} compounds)")
    log_message("")
    
    # Create WebDriver
    driver = create_driver()
    if not driver:
        log_message("✗ Failed to create WebDriver, exiting...")
        return
    
    # Process each compound
    success_count = 0
    fail_count = 0
    
    try:
        for idx, compound in enumerate(compounds_to_process, start=start_idx):
            pubchem_id = compound['PubChem_ID']
            canonical_smiles = compound['Canonical_SMILES']
            
            log_message(f"\n[{idx+1}/{end_idx}] Processing compound {pubchem_id}")
            
            success = process_compound(driver, pubchem_id, canonical_smiles)
            
            if success:
                success_count += 1
                log_message(f"✓ Compound {pubchem_id} processed successfully")
            else:
                fail_count += 1
                log_message(f"✗ Compound {pubchem_id} processing failed")
            
            log_message("")
            
    finally:
        driver.quit()
        log_message("WebDriver closed")
    
    # Summary
    log_message("=" * 60)
    log_message("Processing Complete")
    log_message("=" * 60)
    log_message(f"Total processed: {success_count + fail_count}")
    log_message(f"Successful: {success_count}")
    log_message(f"Failed: {fail_count}")
    log_message("")
    log_message("Next step: Run extract_cytotoxicity.py to aggregate results")
    log_message("=" * 60)

if __name__ == "__main__":
    main()

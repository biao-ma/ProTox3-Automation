#!/usr/bin/env python3
"""
ProTox-3完整自动化脚本
功能：批量处理化合物毒性预测，提取Cytotoxicity数据，汇总结果

使用方法：
    python3 protox_full_automation.py [start_index] [end_index]
    
示例：
    python3 protox_full_automation.py          # 处理所有化合物
    python3 protox_full_automation.py 0 10    # 处理第0-10个化合物
    python3 protox_full_automation.py 10 20   # 处理第10-20个化合物
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

# 配置
PROTOX_URL = 'https://tox.charite.de/protox3/index.php?site=compound_input'
CANONICAL_SMILES_FILE = '/home/ubuntu/canonical_smiles.csv'
OUTPUT_DIR = '/home/ubuntu/protox_results'
LOG_FILE = os.path.join(OUTPUT_DIR, 'processing_log.txt')

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)

def log_message(message):
    """记录消息到日志文件和控制台"""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry + '\n')

def create_driver():
    """创建Chrome WebDriver"""
    chrome_options = Options()
    # 不使用无头模式，以便更好地与网站交互
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument('--allow-insecure-localhost')
    chrome_options.add_argument('--disable-web-resources')
    chrome_options.add_argument('--disable-features=IsolateOrigins,site-per-process')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        log_message("✓ WebDriver已创建")
        return driver
    except Exception as e:
        log_message(f"✗ 创建WebDriver失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def extract_cytotoxicity_data(driver):
    """从页面中提取Cytotoxicity数据"""
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
        log_message(f"✗ 提取数据失败: {e}")
        return None

def extract_full_report(driver):
    """从页面中提取完整的Toxicity Model Report表格"""
    try:
        script = """
        const tables = document.querySelectorAll('table');
        let reportData = [];
        
        tables.forEach(table => {
            const rows = table.querySelectorAll('tr');
            let isReportTable = false;
            
            rows.forEach(row => {
                const text = row.textContent;
                // 检查是否是Toxicity Model Report表格
                if (text.includes('Classification') && text.includes('Prediction')) {
                    isReportTable = true;
                }
                
                if (isReportTable) {
                    const cells = row.querySelectorAll('td');
                    if (cells.length > 0) {
                        const rowData = [];
                        cells.forEach(cell => {
                            rowData.push(cell.textContent.trim());
                        });
                        if (rowData.length > 0) {
                            reportData.push(rowData);
                        }
                    }
                }
            });
        });
        
        return reportData;
        """
        
        result = driver.execute_script(script)
        return result if result else []
    except Exception as e:
        log_message(f"✗ 提取完整报告失败: {e}")
        return []

def save_report_to_csv(pubchem_id, report_data):
    """将报告数据保存为CSV文件"""
    try:
        output_file = os.path.join(OUTPUT_DIR, f'CID_{pubchem_id}.csv')
        
        if report_data and len(report_data) > 0:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # 写入表头
                writer.writerow(['Classification', 'Target', 'Shorthand', 'Prediction', 'Probability'])
                # 写入数据行
                for row in report_data:
                    if len(row) >= 5:
                        writer.writerow(row[:5])
            
            log_message(f"  ✓ 已保存报告到: {output_file}")
            return True
        else:
            log_message(f"  ✗ 报告数据为空")
            return False
    except Exception as e:
        log_message(f"  ✗ 保存报告失败: {e}")
        return False

def process_compound(driver, pubchem_id, canonical_smiles):
    """处理单个化合物的毒性预测"""
    try:
        log_message(f"\n处理化合物: {pubchem_id}")
        
        # 访问网站
        driver.get(PROTOX_URL)
        log_message(f"  ✓ 已访问网站")
        
        # 等待SMILES输入框加载
        time.sleep(2)
        try:
            smiles_input = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, 'smiles_field'))
            )
        except TimeoutException:
            log_message(f"  ✗ 找不到SMILES输入框")
            return False
        
        log_message(f"  ✓ 找到SMILES输入框")
        
        # 清空输入框并输入SMILES
        smiles_input.clear()
        smiles_input.send_keys(canonical_smiles)
        log_message(f"  ✓ 已输入Canonical SMILES")
        
        # 点击SMILES按钮验证
        time.sleep(1)
        try:
            smiles_button = driver.find_element(By.XPATH, "//input[@type='submit'][@value='smiles']")
            smiles_button.click()
            log_message(f"  ✓ 已点击SMILES按钮")
        except NoSuchElementException:
            log_message(f"  ✗ 找不到SMILES按钮")
            return False
        
        # 等待结构显示和页面更新
        time.sleep(3)
        
        # 点击All按钮选择所有模型
        try:
            all_button = driver.find_element(By.ID, 'button_all')
            all_button.click()
            log_message(f"  ✓ 已点击All按钮")
        except NoSuchElementException:
            log_message(f"  ✗ 找不到All按钮")
            return False
        
        # 等待复选框更新
        time.sleep(1)
        
        # 点击Start Tox-Prediction按钮
        try:
            start_button = driver.find_element(By.ID, 'start_pred')
            start_button.click()
            log_message(f"  ✓ 已点击Start Tox-Prediction按钮")
        except NoSuchElementException:
            log_message(f"  ✗ 找不到Start Tox-Prediction按钮")
            return False
        
        # 等待预测完成（最多15分钟）
        log_message(f"  ⏳ 等待预测结果（最多15分钟）...")
        start_time = time.time()
        max_wait = 900  # 15分钟
        check_interval = 3  # 每3秒检查一次
        
        while time.time() - start_time < max_wait:
            try:
                # 检查是否有Cytotoxicity数据可以提取
                cyto_data = extract_cytotoxicity_data(driver)
                if cyto_data and len(cyto_data) >= 4:
                    log_message(f"  ✓ 预测完成")
                    
                    # 提取完整报告
                    report_data = extract_full_report(driver)
                    
                    # 保存报告
                    if save_report_to_csv(pubchem_id, report_data):
                        return True
                    else:
                        return False
            except Exception as e:
                pass
            
            # 数据还未出现，继续等待
            elapsed = int(time.time() - start_time)
            if elapsed % 30 == 0:  # 每30秒输出一次进度
                log_message(f"  ⏳ 已等待 {elapsed} 秒...")
            
            time.sleep(check_interval)
        
        log_message(f"  ✗ 预测超时（超过15分钟）")
        return False
        
    except Exception as e:
        log_message(f"  ✗ 处理失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def read_canonical_smiles():
    """读取Canonical SMILES数据"""
    compounds = []
    try:
        with open(CANONICAL_SMILES_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                compounds.append({
                    'pubchem_id': row['PubChem_ID'],
                    'canonical_smiles': row['Canonical_SMILES']
                })
        log_message(f"✓ 已读取 {len(compounds)} 个化合物的数据")
        return compounds
    except Exception as e:
        log_message(f"✗ 读取数据失败: {e}")
        return []

def extract_cytotoxicity_summary():
    """从所有CID_*.csv文件中提取Cytotoxicity数据并汇总"""
    log_message("\n开始汇总Cytotoxicity数据...")
    
    cid_files = sorted(Path(OUTPUT_DIR).glob('CID_*.csv'))
    results = []
    
    for file_path in cid_files:
        pubchem_id = file_path.stem.replace('CID_', '')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Target') == 'Cytotoxicity':
                        result = {
                            'PubChem_ID': pubchem_id,
                            'Classification': row.get('Classification', ''),
                            'Target': row.get('Target', ''),
                            'Shorthand': row.get('Shorthand', ''),
                            'Prediction': row.get('Prediction', ''),
                            'Probability': row.get('Probability', '')
                        }
                        results.append(result)
                        break
        except Exception as e:
            log_message(f"✗ 处理文件 {file_path} 失败: {e}")
    
    # 保存汇总结果
    if results:
        output_file = os.path.join(OUTPUT_DIR, 'cytotoxicity_summary.csv')
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['PubChem_ID', 'Classification', 'Target', 'Shorthand', 'Prediction', 'Probability'])
            writer.writeheader()
            writer.writerows(results)
        
        log_message(f"✓ 已汇总 {len(results)} 个化合物的Cytotoxicity数据")
        log_message(f"✓ 汇总结果已保存到: {output_file}")
        return output_file
    else:
        log_message(f"✗ 未能提取任何Cytotoxicity数据")
        return None

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='ProTox-3批量处理脚本')
    parser.add_argument('start_index', nargs='?', type=int, default=0, help='起始索引（默认：0）')
    parser.add_argument('end_index', nargs='?', type=int, default=None, help='结束索引（默认：所有）')
    args = parser.parse_args()
    
    log_message("="*60)
    log_message("ProTox-3批量处理脚本启动")
    log_message("="*60)
    
    # 读取化合物数据
    compounds = read_canonical_smiles()
    if not compounds:
        log_message("✗ 无法读取化合物数据，退出")
        return
    
    # 确定处理范围
    start_idx = args.start_index
    end_idx = args.end_index if args.end_index is not None else len(compounds)
    
    log_message(f"处理范围: {start_idx} - {end_idx} (共 {end_idx - start_idx} 个化合物)")
    
    # 创建WebDriver
    driver = None
    try:
        driver = create_driver()
        if not driver:
            log_message("✗ 无法创建WebDriver，退出")
            return
        
        # 处理化合物
        successful = 0
        failed = 0
        
        for i in range(start_idx, min(end_idx, len(compounds))):
            compound = compounds[i]
            
            if process_compound(driver, compound['pubchem_id'], compound['canonical_smiles']):
                successful += 1
            else:
                failed += 1
            
            # 每处理3个化合物后暂停一下
            if (i - start_idx + 1) % 3 == 0:
                log_message(f"⏳ 暂停15秒...")
                time.sleep(15)
        
        log_message("\n" + "="*60)
        log_message(f"处理完成！成功: {successful}, 失败: {failed}")
        log_message("="*60)
        
        # 汇总结果
        summary_file = extract_cytotoxicity_summary()
        if summary_file:
            log_message(f"✓ 最终结果文件: {summary_file}")
        
    finally:
        if driver:
            driver.quit()
            log_message("✓ WebDriver已关闭")

if __name__ == '__main__':
    main()

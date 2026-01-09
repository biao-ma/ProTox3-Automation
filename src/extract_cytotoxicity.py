#!/usr/bin/env python3
"""
从所有CID_*.csv文件中提取Cytotoxicity行并汇总到一个新的CSV文件
"""

import csv
import os
import sys
from pathlib import Path

def extract_cytotoxicity_from_file(file_path):
    """从单个CSV文件中提取Cytotoxicity行"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('Target') == 'Cytotoxicity':
                    return row
    except Exception as e:
        print(f"读取文件 {file_path} 失败: {e}")
    
    return None

def main():
    # 结果目录
    result_dir = '/home/ubuntu/protox_results'
    
    # 查找所有CID_*.csv文件
    cid_files = sorted(Path(result_dir).glob('CID_*.csv'))
    
    if not cid_files:
        print(f"在 {result_dir} 中找不到任何CID_*.csv文件")
        return
    
    print(f"找到 {len(cid_files)} 个CID_*.csv文件")
    
    # 提取所有Cytotoxicity数据
    results = []
    for file_path in cid_files:
        # 从文件名中提取PubChem_ID
        pubchem_id = file_path.stem.replace('CID_', '')
        
        # 提取Cytotoxicity行
        cyto_row = extract_cytotoxicity_from_file(file_path)
        
        if cyto_row:
            result = {
                'PubChem_ID': pubchem_id,
                'Classification': cyto_row.get('Classification', ''),
                'Target': cyto_row.get('Target', ''),
                'Shorthand': cyto_row.get('Shorthand', ''),
                'Prediction': cyto_row.get('Prediction', ''),
                'Probability': cyto_row.get('Probability', '')
            }
            results.append(result)
            print(f"✓ {pubchem_id}: {cyto_row.get('Prediction', 'N/A')} ({cyto_row.get('Probability', 'N/A')})")
        else:
            print(f"✗ {pubchem_id}: 未找到Cytotoxicity行")
    
    # 保存汇总结果
    if results:
        output_file = os.path.join(result_dir, 'cytotoxicity_summary.csv')
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['PubChem_ID', 'Classification', 'Target', 'Shorthand', 'Prediction', 'Probability'])
            writer.writeheader()
            writer.writerows(results)
        
        print(f"\n{'='*60}")
        print(f"✓ 成功提取 {len(results)} 个化合物的Cytotoxicity数据")
        print(f"✓ 汇总结果已保存到: {output_file}")
        print(f"{'='*60}")
    else:
        print(f"\n✗ 未能提取任何Cytotoxicity数据")

if __name__ == '__main__':
    main()

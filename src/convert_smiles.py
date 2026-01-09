#!/usr/bin/env python3
"""
转换SMILES为Canonical SMILES格式
"""

import csv
import sys
from rdkit import Chem

def convert_to_canonical_smiles(smiles):
    """将SMILES转换为Canonical SMILES"""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is not None:
            canonical_smiles = Chem.MolToSmiles(mol)
            return canonical_smiles
        else:
            return None
    except Exception as e:
        print(f"Error converting SMILES: {smiles}, Error: {e}", file=sys.stderr)
        return None

def main():
    input_file = '/home/ubuntu/upload/pubchem_smiles.csv'
    output_file = '/home/ubuntu/canonical_smiles.csv'
    
    # 读取输入文件并转换
    data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pubchem_id = row['PubChem_ID']
            smiles = row['SMILES']
            canonical_smiles = convert_to_canonical_smiles(smiles)
            
            if canonical_smiles:
                data.append({
                    'PubChem_ID': pubchem_id,
                    'Original_SMILES': smiles,
                    'Canonical_SMILES': canonical_smiles
                })
                print(f"✓ {pubchem_id}: {canonical_smiles}")
            else:
                print(f"✗ {pubchem_id}: Failed to convert", file=sys.stderr)
    
    # 写入输出文件
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['PubChem_ID', 'Original_SMILES', 'Canonical_SMILES'])
        writer.writeheader()
        writer.writerows(data)
    
    print(f"\n✓ 成功转换 {len(data)} 个化合物")
    print(f"✓ 结果已保存到: {output_file}")

if __name__ == '__main__':
    main()

# 文件清单和说明

## 📁 项目文件结构

```
/home/ubuntu/
├── venv/                              # Python虚拟环境
├── upload/
│   └── pubchem_smiles.csv            # 原始数据（PubChem_ID + SMILES）
├── canonical_smiles.csv              # 转换后的Canonical SMILES数据 ✓
├── protox_results/                   # 输出目录
│   ├── CID_311434.csv               # 单个化合物的完整报告
│   ├── CID_54576693.csv
│   ├── ...
│   ├── cytotoxicity_summary.csv     # 最终汇总文件
│   └── processing_log.txt           # 处理日志
├── protox_full_automation.py         # 主自动化脚本 ✓
├── extract_cytotoxicity.py           # 结果汇总脚本 ✓
├── run_protox.sh                     # 快速启动脚本 ✓
├── PROTOX_AUTOMATION_GUIDE.md        # 详细使用指南 ✓
├── QUICK_START.md                    # 快速开始指南 ✓
└── FILES_MANIFEST.md                 # 本文件 ✓
```

---

## 📄 文件详细说明

### 输入数据文件

#### 1. `/home/ubuntu/upload/pubchem_smiles.csv`
- **来源**: 用户上传
- **内容**: 原始数据，包含PubChem_ID和SMILES
- **格式**: CSV
- **行数**: 98行（1个表头 + 97个化合物）
- **列**: PubChem_ID, SMILES
- **状态**: ✓ 已处理

#### 2. `/home/ubuntu/canonical_smiles.csv`
- **来源**: 由`convert_smiles.py`生成
- **内容**: PubChem_ID、原始SMILES和Canonical SMILES
- **格式**: CSV
- **行数**: 98行（1个表头 + 97个化合物）
- **列**: PubChem_ID, Original_SMILES, Canonical_SMILES
- **状态**: ✓ 已生成

---

### 脚本文件

#### 1. `/home/ubuntu/protox_full_automation.py`
- **功能**: 主自动化脚本，处理所有化合物的毒性预测
- **语言**: Python 3
- **依赖**: selenium, rdkit
- **用法**:
  ```bash
  python3 protox_full_automation.py [start] [end]
  ```
- **输出**: 
  - `CID_*.csv` 文件（每个化合物一个）
  - `cytotoxicity_summary.csv`（汇总文件）
  - `processing_log.txt`（日志文件）

#### 2. `/home/ubuntu/extract_cytotoxicity.py`
- **功能**: 从所有CID_*.csv文件中提取Cytotoxicity行并汇总
- **语言**: Python 3
- **依赖**: 无（仅使用标准库）
- **用法**:
  ```bash
  python3 extract_cytotoxicity.py
  ```
- **输出**: `cytotoxicity_summary.csv`

#### 3. `/home/ubuntu/run_protox.sh`
- **功能**: 快速启动脚本，提供交互式界面
- **语言**: Bash
- **用法**:
  ```bash
  bash run_protox.sh [start] [end]
  ```
- **特点**: 
  - 自动激活虚拟环境
  - 自动安装依赖
  - 提供彩色输出
  - 确认框提示

---

### 文档文件

#### 1. `/home/ubuntu/PROTOX_AUTOMATION_GUIDE.md`
- **内容**: 详细的使用指南
- **章节**:
  - 项目概述
  - 环境准备
  - 使用方法
  - 输出文件说明
  - 重要提示
  - 故障排除
  - 高级用法
  - 结果验证
  - 常见问题解答

#### 2. `/home/ubuntu/QUICK_START.md`
- **内容**: 快速开始指南
- **特点**: 简洁明了，适合快速上手
- **章节**:
  - 文件清单
  - 快速开始（3步）
  - 时间估计
  - 输出文件
  - 监控进度
  - 中途停止和继续
  - 后台运行
  - 常见问题

#### 3. `/home/ubuntu/FILES_MANIFEST.md`
- **内容**: 本文件，文件清单和说明

---

### 输出文件

#### 1. `/home/ubuntu/protox_results/CID_*.csv`
- **格式**: CSV
- **命名**: `CID_{PubChem_ID}.csv`
- **示例**: `CID_311434.csv`
- **内容**: 单个化合物的完整毒性预测报告
- **列**: Classification, Target, Shorthand, Prediction, Probability
- **行数**: 取决于预测的模型数（通常40-50行）
- **生成**: 由`protox_full_automation.py`生成

#### 2. `/home/ubuntu/protox_results/cytotoxicity_summary.csv`
- **格式**: CSV
- **内容**: 所有化合物的Cytotoxicity预测结果汇总
- **列**: PubChem_ID, Classification, Target, Shorthand, Prediction, Probability
- **行数**: 1个表头 + 97个化合物
- **生成**: 由`protox_full_automation.py`自动生成，或由`extract_cytotoxicity.py`手动生成

#### 3. `/home/ubuntu/protox_results/processing_log.txt`
- **格式**: 纯文本
- **内容**: 详细的处理日志
- **信息**: 时间戳、操作状态、错误信息等
- **生成**: 由`protox_full_automation.py`生成

---

## 🔄 工作流程

```
1. 原始数据
   └─ /home/ubuntu/upload/pubchem_smiles.csv

2. SMILES转换 ✓ 已完成
   └─ /home/ubuntu/canonical_smiles.csv

3. 批量毒性预测 ⏳ 待执行
   ├─ 运行: python3 protox_full_automation.py
   └─ 输出: 
      ├─ /home/ubuntu/protox_results/CID_*.csv
      ├─ /home/ubuntu/protox_results/processing_log.txt
      └─ /home/ubuntu/protox_results/cytotoxicity_summary.csv

4. 结果汇总 ✓ 自动完成
   └─ /home/ubuntu/protox_results/cytotoxicity_summary.csv
```

---

## 📊 数据格式说明

### Canonical SMILES CSV格式
```csv
PubChem_ID,Original_SMILES,Canonical_SMILES
311434,CC1=CC(=NO1)NC(=O)NC2=CC(=C(C=C2OC)OC)Cl,COc1cc(OC)c(NC(=O)Nc2cc(C)on2)cc1Cl
54576693,...,...
```

### 单个化合物报告CSV格式
```csv
Classification,Target,Shorthand,Prediction,Probability
Organ toxicity,Hepatotoxicity,dili,Active,0.62
Organ toxicity,Neurotoxicity,neuro,Active,0.61
...
Toxicity end points,Cytotoxicity,cyto,Inactive,0.62
...
```

### 汇总文件CSV格式
```csv
PubChem_ID,Classification,Target,Shorthand,Prediction,Probability
311434,Toxicity end points,Cytotoxicity,cyto,Inactive,0.62
54576693,Toxicity end points,Cytotoxicity,cyto,Active,0.71
...
```

---

## 🔐 文件权限

| 文件 | 权限 | 说明 |
|------|------|------|
| `protox_full_automation.py` | 644 | 可读可执行 |
| `extract_cytotoxicity.py` | 644 | 可读可执行 |
| `run_protox.sh` | 755 | 可执行脚本 |
| `*.csv` | 644 | 可读 |
| `*.md` | 644 | 可读 |

---

## 💾 存储空间估计

| 项目 | 大小 | 说明 |
|------|------|------|
| 原始数据 | ~50 KB | pubchem_smiles.csv |
| Canonical SMILES | ~100 KB | canonical_smiles.csv |
| 单个CID文件 | ~5-10 KB | 平均每个化合物 |
| 全部CID文件 | ~500 KB - 1 MB | 97个化合物 |
| 汇总文件 | ~20 KB | cytotoxicity_summary.csv |
| 日志文件 | ~100-500 KB | processing_log.txt |
| **总计** | **~1-2 MB** | 完整项目 |

---

## 🔄 版本控制

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0 | 2026-01-08 | 初始版本 |

---

## ✅ 检查清单

在运行脚本前，请确保：

- [ ] 虚拟环境已创建：`/home/ubuntu/venv/`
- [ ] Canonical SMILES文件已生成：`/home/ubuntu/canonical_smiles.csv`
- [ ] 输出目录已创建：`/home/ubuntu/protox_results/`
- [ ] 主脚本存在：`/home/ubuntu/protox_full_automation.py`
- [ ] 启动脚本存在：`/home/ubuntu/run_protox.sh`
- [ ] 网络连接正常
- [ ] Chrome/Chromium已安装

---

## 📞 获取帮助

1. **快速问题**: 查看 `QUICK_START.md`
2. **详细问题**: 查看 `PROTOX_AUTOMATION_GUIDE.md`
3. **脚本问题**: 查看 `processing_log.txt`
4. **数据问题**: 检查 `canonical_smiles.csv`

---

**最后更新**: 2026-01-08
**维护者**: Manus AI

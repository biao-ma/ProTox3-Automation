# ProTox3-Automation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![ProTox-3](https://img.shields.io/badge/ProTox-3.0-green.svg)](https://tox.charite.de/protox3/)

**语言**: [English](README.md) | [中文](README.zh-CN.md) | [日本語](README.ja.md)

**ProTox3-Automation** 是一个完整的自动化工具套件，用于批量处理化合物的毒性预测，特别是提取**细胞毒性（Cytotoxicity）**预测结果。

## ✨ 核心功能

- 🔄 **SMILES转换** - 自动将SMILES转换为Canonical格式
- 🤖 **批量预测** - 自动化访问ProTox-3网站进行毒性预测
- 📊 **数据提取** - 从预测结果中提取Cytotoxicity数据
- 📈 **结果汇总** - 将所有结果汇总到单一CSV文件
- 🚀 **高效处理** - 支持分批处理和后台运行

## 🎯 适用场景

- 药物研发中的毒性评估
- 化学品安全性筛选
- 学术研究中的毒性预测
- 大规模化合物库的毒性分析

## 📋 系统要求

- Python 3.7+
- Chrome/Chromium浏览器
- 稳定的网络连接
- 至少1GB可用磁盘空间

## 🚀 快速开始

### 一键安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/biao-ma/ProTox3-Automation.git
cd ProTox3-Automation

# 运行安装脚本
bash setup.sh

# 开始使用
bash run_protox.sh
```

### 手动安装

```bash
# 1. 克隆仓库
git clone https://github.com/biao-ma/ProTox3-Automation.git
cd ProTox3-Automation

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 准备数据
# 将您的CSV文件放入 data/ 目录，文件应包含 PubChem_ID 和 SMILES 列

# 5. 运行脚本
python3 src/protox_full_automation.py
```

## 📊 使用示例

### 处理所有化合物

```bash
python3 src/protox_full_automation.py
```

### 处理指定范围的化合物

```bash
# 处理第0-10个化合物
python3 src/protox_full_automation.py 0 10

# 处理第10-20个化合物
python3 src/protox_full_automation.py 10 20
```

### 后台运行

```bash
nohup python3 src/protox_full_automation.py > protox.log 2>&1 &
```

## 📁 项目结构

```
ProTox3-Automation/
├── README.md                      # 项目说明
├── LICENSE                        # 许可证
├── requirements.txt               # Python依赖
├── setup.sh                       # 一键安装脚本
├── run_protox.sh                  # 快速启动脚本
├── data/                          # 数据目录
│   └── example_input.csv         # 示例输入文件
├── src/                           # 源代码目录
│   ├── protox_full_automation.py # 主自动化脚本
│   ├── extract_cytotoxicity.py   # 结果汇总脚本
│   └── convert_smiles.py         # SMILES转换脚本
├── results/                       # 输出目录
│   ├── CID_*.csv                 # 单个化合物报告
│   └── cytotoxicity_summary.csv  # 最终汇总文件
└── docs/                          # 文档目录
    ├── QUICK_START.md            # 快速开始指南
    ├── INSTALLATION.md           # 详细安装指南
    ├── USER_GUIDE.md             # 用户指南
    └── TROUBLESHOOTING.md        # 故障排除
```

## ⏱️ 时间估计

| 任务 | 时间 |
|------|------|
| 单个化合物 | 5-10分钟 |
| 10个化合物 | 1-2小时 |
| 100个化合物 | 8-16小时 |

## 📊 输出格式

### 单个化合物报告 (CID_*.csv)

```csv
Classification,Target,Shorthand,Prediction,Probability
Organ toxicity,Hepatotoxicity,dili,Active,0.62
Organ toxicity,Neurotoxicity,neuro,Active,0.61
...
Toxicity end points,Cytotoxicity,cyto,Inactive,0.62
...
```

### 汇总文件 (cytotoxicity_summary.csv)

```csv
PubChem_ID,Classification,Target,Shorthand,Prediction,Probability
311434,Toxicity end points,Cytotoxicity,cyto,Inactive,0.62
54576693,Toxicity end points,Cytotoxicity,cyto,Active,0.71
...
```

## 🔧 配置选项

在 `config.py` 中可以自定义以下选项：

```python
# ProTox-3网站URL
PROTOX_URL = 'https://tox.charite.de/protox3/index.php?site=compound_input'

# 输入文件路径
INPUT_FILE = 'data/input.csv'

# 输出目录
OUTPUT_DIR = 'results/'

# 超时设置（秒）
MAX_WAIT_TIME = 900  # 15分钟
```

## 📚 文档

- [快速开始指南](docs/QUICK_START.md)
- [详细安装指南](docs/INSTALLATION.md)
- [用户指南](docs/USER_GUIDE.md)
- [故障排除](docs/TROUBLESHOOTING.md)
- [API文档](docs/API.md)

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与项目。

### 贡献方式

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## ⚠️ 免责声明

- 本工具仅供研究和学习用途
- 请遵守 ProTox-3 网站的使用条款
- 数据不得用于商业目的
- 预测结果仅供参考，不应作为最终决策依据

## 🙏 致谢

- [ProTox-3](https://tox.charite.de/protox3/) - 提供毒性预测服务
- [RDKit](https://www.rdkit.org/) - 化学信息学工具包
- [Selenium](https://www.selenium.dev/) - 浏览器自动化工具

## 📞 联系方式

- 问题反馈：[GitHub Issues](https://github.com/biao-ma/ProTox3-Automation/issues)
- 功能建议：[GitHub Discussions](https://github.com/biao-ma/ProTox3-Automation/discussions)

## 🌟 Star History

如果这个项目对您有帮助，请给我们一个 ⭐️！

---

**最后更新**: 2026-01-08  
**版本**: 1.0.0

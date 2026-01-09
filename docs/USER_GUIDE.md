# ProTox-3 细胞毒性预测自动化脚本使用指南

## 项目概述

本脚本用于自动化批量处理化合物的毒性预测，特别是提取**细胞毒性（Cytotoxicity）**预测结果。

### 工作流程

1. **SMILES转换** ✓ 已完成
   - 从CSV文件读取PubChem_ID和SMILES
   - 使用RDKit转换为Canonical SMILES格式
   - 结果保存在 `/home/ubuntu/canonical_smiles.csv`

2. **批量毒性预测** ⏳ 待执行
   - 访问ProTox-3网站
   - 输入Canonical SMILES
   - 选择所有预测模型
   - 等待预测结果
   - 保存完整报告为 `CID_{PubChem_ID}.csv`

3. **结果汇总** ⏳ 待执行
   - 从所有CID_*.csv文件中提取Cytotoxicity行
   - 汇总到 `cytotoxicity_summary.csv`

---

## 环境准备

### 1. 安装依赖

```bash
# 创建虚拟环境（如果还未创建）
python3 -m venv ~/venv

# 激活虚拟环境
source ~/venv/bin/activate

# 安装必要的包
pip install selenium rdkit -q
```

### 2. 验证环境

```bash
# 检查Python版本
python3 --version

# 检查Selenium是否已安装
python3 -c "import selenium; print(f'Selenium版本: {selenium.__version__}')"

# 检查RDKit是否已安装
python3 -c "from rdkit import Chem; print('RDKit已安装')"
```

---

## 使用方法

### 基本用法

#### 方式1：处理所有化合物

```bash
cd /home/ubuntu
source venv/bin/activate
python3 protox_full_automation.py
```

#### 方式2：处理指定范围的化合物

```bash
# 处理第0-10个化合物
python3 protox_full_automation.py 0 10

# 处理第10-20个化合物
python3 protox_full_automation.py 10 20

# 处理第50个到第100个化合物
python3 protox_full_automation.py 50 100
```

### 执行示例

```bash
# 启动脚本
$ python3 protox_full_automation.py 0 5

# 预期输出
[2026-01-08 10:30:45] ============================================================
[2026-01-08 10:30:45] ProTox-3批量处理脚本启动
[2026-01-08 10:30:45] ============================================================
[2026-01-08 10:30:45] ✓ 已读取 97 个化合物的数据
[2026-01-08 10:30:45] ✓ WebDriver已创建
[2026-01-08 10:30:45] 处理范围: 0 - 5 (共 5 个化合物)
[2026-01-08 10:30:46] 
[2026-01-08 10:30:46] 处理化合物: 311434
[2026-01-08 10:30:46]   ✓ 已访问网站
[2026-01-08 10:30:48]   ✓ 找到SMILES输入框
[2026-01-08 10:30:48]   ✓ 已输入Canonical SMILES
...
```

---

## 输出文件说明

### 1. 单个化合物报告
- **文件名**: `CID_{PubChem_ID}.csv`
- **位置**: `/home/ubuntu/protox_results/`
- **内容**: 完整的毒性预测报告，包括所有模型的预测结果

**示例内容**:
```csv
Classification,Target,Shorthand,Prediction,Probability
Organ toxicity,Hepatotoxicity,dili,Active,0.62
Organ toxicity,Neurotoxicity,neuro,Active,0.61
...
Toxicity end points,Cytotoxicity,cyto,Inactive,0.62
...
```

### 2. 细胞毒性汇总文件
- **文件名**: `cytotoxicity_summary.csv`
- **位置**: `/home/ubuntu/protox_results/`
- **内容**: 所有化合物的Cytotoxicity预测结果汇总

**示例内容**:
```csv
PubChem_ID,Classification,Target,Shorthand,Prediction,Probability
311434,Toxicity end points,Cytotoxicity,cyto,Inactive,0.62
54576693,Toxicity end points,Cytotoxicity,cyto,Active,0.71
121280087,Toxicity end points,Cytotoxicity,cyto,Inactive,0.58
...
```

### 3. 处理日志
- **文件名**: `processing_log.txt`
- **位置**: `/home/ubuntu/protox_results/`
- **内容**: 详细的处理日志，包括所有操作和错误信息

---

## 重要提示

### ⏱️ 时间估计

- **每个化合物**: 5-10分钟（取决于网络速度和服务器响应）
- **全部97个化合物**: 8-16小时
- **建议**: 分批处理，每批10-20个化合物

### 🔄 断点续传

如果处理过程中中断，您可以：

1. **查看已完成的化合物**
   ```bash
   ls -lh /home/ubuntu/protox_results/CID_*.csv | wc -l
   ```

2. **继续处理剩余化合物**
   - 假设已处理到第20个，继续处理第20-40个：
   ```bash
   python3 protox_full_automation.py 20 40
   ```

3. **重新汇总所有结果**
   ```bash
   python3 extract_cytotoxicity.py
   ```

### 🌐 网络连接

- 脚本需要稳定的互联网连接
- 如果连接中断，脚本会自动重试
- 建议在稳定的网络环境下运行

### 🔒 SSL证书问题

脚本已配置为忽略SSL证书错误。如果仍然遇到问题：

```bash
# 方法1：更新证书
pip install --upgrade certifi

# 方法2：使用HTTP而不是HTTPS（如果可用）
# 编辑脚本中的 PROTOX_URL 变量
```

---

## 故障排除

### 问题1：WebDriver无法启动

**错误信息**: `SessionNotCreatedException: Chrome failed to start`

**解决方案**:
```bash
# 检查Chrome是否已安装
which chromium-browser

# 如果未安装，请安装Chrome/Chromium
sudo apt-get install chromium-browser

# 重新运行脚本
python3 protox_full_automation.py
```

### 问题2：网站无法访问

**错误信息**: `net::ERR_CERT_DATE_INVALID` 或 `net::ERR_TIMED_OUT`

**解决方案**:
- 检查网络连接
- 等待几分钟后重试
- 脚本会自动重试，通常可以解决

### 问题3：预测超时

**错误信息**: `预测超时（超过15分钟）`

**解决方案**:
- 这是正常的，某些复杂化合物可能需要更长时间
- 脚本会自动跳过并继续处理下一个
- 可以稍后手动重新处理该化合物

### 问题4：内存不足

**错误信息**: `MemoryError` 或 `out of memory`

**解决方案**:
- 减少批处理大小（例如每次处理5个而不是20个）
- 定期重启脚本
- 确保系统有足够的可用内存

---

## 高级用法

### 1. 后台运行脚本

```bash
# 使用nohup后台运行
nohup python3 protox_full_automation.py > protox_output.log 2>&1 &

# 查看进程
ps aux | grep protox_full_automation

# 查看实时日志
tail -f /home/ubuntu/protox_results/processing_log.txt
```

### 2. 使用screen进行会话管理

```bash
# 创建新的screen会话
screen -S protox

# 在screen中运行脚本
cd /home/ubuntu
source venv/bin/activate
python3 protox_full_automation.py

# 分离会话（按Ctrl+A然后D）
# 重新连接会话
screen -r protox

# 列出所有会话
screen -ls
```

### 3. 使用tmux进行会话管理

```bash
# 创建新的tmux会话
tmux new-session -s protox

# 在tmux中运行脚本
cd /home/ubuntu
source venv/bin/activate
python3 protox_full_automation.py

# 分离会话（按Ctrl+B然后D）
# 重新连接会话
tmux attach-session -t protox

# 列出所有会话
tmux list-sessions
```

### 4. 定期检查进度

```bash
# 创建一个检查脚本 check_progress.sh
#!/bin/bash
while true; do
    clear
    echo "=== ProTox-3处理进度 ==="
    echo "已完成的化合物数: $(ls /home/ubuntu/protox_results/CID_*.csv 2>/dev/null | wc -l)"
    echo "总化合物数: 97"
    echo ""
    echo "最近的日志:"
    tail -5 /home/ubuntu/protox_results/processing_log.txt
    echo ""
    echo "下一次检查在10秒后..."
    sleep 10
done

# 运行检查脚本
bash check_progress.sh
```

---

## 结果验证

### 1. 检查文件是否生成

```bash
# 查看已生成的CID文件
ls -lh /home/ubuntu/protox_results/CID_*.csv | head -10

# 统计已生成的文件数
ls /home/ubuntu/protox_results/CID_*.csv | wc -l
```

### 2. 验证汇总文件

```bash
# 查看汇总文件内容
head -20 /home/ubuntu/protox_results/cytotoxicity_summary.csv

# 统计汇总文件中的行数
wc -l /home/ubuntu/protox_results/cytotoxicity_summary.csv
```

### 3. 检查特定化合物的结果

```bash
# 查看特定化合物的完整报告
cat /home/ubuntu/protox_results/CID_311434.csv

# 查看特定化合物的Cytotoxicity结果
grep "Cytotoxicity" /home/ubuntu/protox_results/CID_311434.csv
```

---

## 脚本参数说明

### 主要配置变量

在脚本顶部可以修改以下配置：

```python
PROTOX_URL = 'https://tox.charite.de/protox3/index.php?site=compound_input'
# ProTox-3网站URL

CANONICAL_SMILES_FILE = '/home/ubuntu/canonical_smiles.csv'
# Canonical SMILES数据文件路径

OUTPUT_DIR = '/home/ubuntu/protox_results'
# 输出文件目录

LOG_FILE = os.path.join(OUTPUT_DIR, 'processing_log.txt')
# 日志文件路径
```

### 调整超时时间

如果遇到频繁超时，可以修改脚本中的超时时间：

```python
max_wait = 900  # 改为 1200 表示20分钟
check_interval = 3  # 改为 5 表示每5秒检查一次
```

---

## 常见问题解答

**Q: 脚本运行多久？**
A: 全部97个化合物需要8-16小时，取决于网络速度和服务器响应时间。

**Q: 可以中途停止吗？**
A: 可以。按Ctrl+C停止脚本。已完成的化合物数据会被保存，您可以稍后继续处理。

**Q: 如何检查处理进度？**
A: 查看日志文件 `/home/ubuntu/protox_results/processing_log.txt`，或者数一下 `CID_*.csv` 文件的个数。

**Q: 失败的化合物可以重新处理吗？**
A: 可以。删除对应的 `CID_*.csv` 文件，然后重新运行脚本处理该化合物。

**Q: 最终结果在哪里？**
A: 汇总结果在 `/home/ubuntu/protox_results/cytotoxicity_summary.csv`

---

## 联系支持

如有问题，请查看：
- 日志文件：`/home/ubuntu/protox_results/processing_log.txt`
- 脚本源代码：`/home/ubuntu/protox_full_automation.py`
- 提取脚本：`/home/ubuntu/extract_cytotoxicity.py`

---

## 许可证和免责声明

- 本脚本仅供研究和学习用途
- 请遵守ProTox-3网站的使用条款
- 数据仅用于科研目的，不得用于商业用途

---

**最后更新**: 2026-01-08
**版本**: 1.0

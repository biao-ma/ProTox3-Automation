# ProTox-3 自动化脚本 - 快速开始指南

## 📋 文件清单

| 文件 | 说明 |
|------|------|
| `protox_full_automation.py` | 主自动化脚本 |
| `extract_cytotoxicity.py` | 结果汇总脚本 |
| `run_protox.sh` | 快速启动脚本 |
| `canonical_smiles.csv` | Canonical SMILES数据（已生成） |
| `PROTOX_AUTOMATION_GUIDE.md` | 详细使用指南 |
| `QUICK_START.md` | 本文件 |

---

## 🚀 快速开始（3步）

### 第1步：激活虚拟环境

```bash
cd /home/ubuntu
source venv/bin/activate
```

### 第2步：运行脚本

#### 选项A：使用快速启动脚本（推荐）

```bash
# 处理所有化合物
bash run_protox.sh

# 处理第0-10个化合物
bash run_protox.sh 0 10

# 处理第10-20个化合物
bash run_protox.sh 10 20
```

#### 选项B：直接运行Python脚本

```bash
# 处理所有化合物
python3 protox_full_automation.py

# 处理第0-10个化合物
python3 protox_full_automation.py 0 10
```

### 第3步：等待完成

脚本会自动处理每个化合物，并在完成后生成结果文件。

---

## ⏱️ 时间估计

| 任务 | 时间 |
|------|------|
| 单个化合物 | 5-10分钟 |
| 10个化合物 | 1-2小时 |
| 20个化合物 | 2-3小时 |
| 全部97个化合物 | 8-16小时 |

---

## 📊 输出文件

### 单个化合物报告
- **文件**: `/home/ubuntu/protox_results/CID_311434.csv`
- **内容**: 该化合物的完整毒性预测报告

### 汇总文件
- **文件**: `/home/ubuntu/protox_results/cytotoxicity_summary.csv`
- **内容**: 所有化合物的Cytotoxicity预测结果

### 日志文件
- **文件**: `/home/ubuntu/protox_results/processing_log.txt`
- **内容**: 详细的处理日志

---

## 🔍 监控进度

### 方法1：查看日志
```bash
tail -f /home/ubuntu/protox_results/processing_log.txt
```

### 方法2：统计完成数
```bash
ls /home/ubuntu/protox_results/CID_*.csv | wc -l
```

### 方法3：查看汇总文件
```bash
wc -l /home/ubuntu/protox_results/cytotoxicity_summary.csv
```

---

## 🛑 中途停止和继续

### 停止脚本
按 `Ctrl+C` 停止脚本

### 查看已完成的化合物
```bash
ls /home/ubuntu/protox_results/CID_*.csv | head -10
```

### 继续处理剩余化合物
假设已处理到第20个，继续处理第20-40个：
```bash
python3 protox_full_automation.py 20 40
```

---

## ✅ 后台运行（推荐）

### 使用nohup
```bash
nohup python3 protox_full_automation.py > protox_output.log 2>&1 &
```

### 使用screen
```bash
# 创建screen会话
screen -S protox

# 在screen中运行脚本
python3 protox_full_automation.py

# 分离会话（Ctrl+A然后D）

# 重新连接
screen -r protox
```

### 使用tmux
```bash
# 创建tmux会话
tmux new-session -s protox

# 在tmux中运行脚本
python3 protox_full_automation.py

# 分离会话（Ctrl+B然后D）

# 重新连接
tmux attach-session -t protox
```

---

## 🔧 常见问题

### Q: 脚本无法启动
**A:** 检查虚拟环境是否已激活：
```bash
source /home/ubuntu/venv/bin/activate
```

### Q: 出现SSL证书错误
**A:** 脚本已配置为忽略SSL错误，通常可以自动解决。

### Q: 预测超时
**A:** 这是正常的，某些复杂化合物可能需要更长时间。脚本会自动跳过并继续。

### Q: 如何重新处理某个化合物
**A:** 删除对应的CID_*.csv文件，然后重新运行脚本：
```bash
rm /home/ubuntu/protox_results/CID_311434.csv
python3 protox_full_automation.py 0 1
```

---

## 📈 最终结果验证

### 查看汇总文件内容
```bash
head -20 /home/ubuntu/protox_results/cytotoxicity_summary.csv
```

### 查看特定化合物的结果
```bash
grep "311434" /home/ubuntu/protox_results/cytotoxicity_summary.csv
```

### 统计Active和Inactive的数量
```bash
grep "Active" /home/ubuntu/protox_results/cytotoxicity_summary.csv | wc -l
grep "Inactive" /home/ubuntu/protox_results/cytotoxicity_summary.csv | wc -l
```

---

## 📚 更多信息

详细使用指南请参考：`PROTOX_AUTOMATION_GUIDE.md`

---

**提示**: 建议先用小批量测试（如10个化合物），验证流程正常后再处理全部化合物。

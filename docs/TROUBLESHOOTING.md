# 故障排除指南

本文档包含常见问题及其解决方案。

## 目录

- [安装问题](#安装问题)
- [运行时问题](#运行时问题)
- [浏览器问题](#浏览器问题)
- [数据问题](#数据问题)
- [性能问题](#性能问题)

---

## 安装问题

### Q1: Python版本不兼容

**问题**: 提示需要Python 3.7+

**解决方案**:
```bash
# 检查当前版本
python3 --version

# Ubuntu安装Python 3.9
sudo apt install python3.9 python3.9-venv -y

# macOS
brew install python@3.9
```

### Q2: pip安装依赖失败

**问题**: "ERROR: Could not install packages"

**解决方案**:
```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 逐个安装依赖
pip install selenium
pip install rdkit-pypi  # 如果rdkit安装失败
```

### Q3: RDKit安装失败

**问题**: "Building wheel for rdkit failed"

**解决方案**:
```bash
# 方法1: 使用conda（推荐）
conda install -c conda-forge rdkit

# 方法2: 使用预编译版本
pip install rdkit-pypi

# 方法3: 使用系统包管理器
# Ubuntu
sudo apt install python3-rdkit

# macOS
brew install rdkit
```

---

## 运行时问题

### Q4: 找不到输入文件

**问题**: "FileNotFoundError: input.csv not found"

**解决方案**:
```bash
# 检查文件路径
ls data/

# 确保文件名正确
# 默认查找: data/input.csv

# 或指定文件路径
python3 src/protox_full_automation.py --input data/your_file.csv
```

### Q5: SMILES转换失败

**问题**: "Invalid SMILES string"

**解决方案**:
- 检查SMILES格式是否正确
- 确保没有特殊字符
- 尝试清理数据：
```python
# 移除空格和换行符
smiles = smiles.strip()
```

### Q6: 脚本运行中断

**问题**: 脚本突然停止

**解决方案**:
```bash
# 使用nohup后台运行
nohup python3 src/protox_full_automation.py > output.log 2>&1 &

# 或使用screen
screen -S protox
python3 src/protox_full_automation.py
# Ctrl+A, D 分离会话

# 重新连接
screen -r protox
```

---

## 浏览器问题

### Q7: ChromeDriver版本不匹配

**问题**: "This version of ChromeDriver only supports Chrome version XX"

**解决方案**:
```bash
# 方法1: 自动管理驱动（推荐）
pip install webdriver-manager

# 在代码中使用
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

# 方法2: 手动下载匹配版本
# 1. 查看Chrome版本: chrome://version/
# 2. 下载对应驱动: https://chromedriver.chromium.org/
```

### Q8: 浏览器无法启动

**问题**: "WebDriverException: unknown error: Chrome failed to start"

**解决方案**:
```bash
# 检查Chrome是否安装
google-chrome --version
# 或
chromium-browser --version

# 添加无头模式选项
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
```

### Q9: SSL证书错误

**问题**: "SSL: CERTIFICATE_VERIFY_FAILED"

**解决方案**:
```python
# 在代码中添加
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

# 或使用HTTP而不是HTTPS
PROTOX_URL = 'http://tox.charite.de/protox3/...'
```

---

## 数据问题

### Q10: CSV格式错误

**问题**: "KeyError: 'PubChem_ID' or 'SMILES'"

**解决方案**:
```bash
# 确保CSV包含必需的列
# 正确格式:
PubChem_ID,SMILES
311434,CC1=CC(=NO1)NC(=O)...

# 检查列名
head -1 data/input.csv
```

### Q11: 编码问题

**问题**: "UnicodeDecodeError"

**解决方案**:
```python
# 指定编码
pd.read_csv('input.csv', encoding='utf-8')

# 或
with open('input.csv', 'r', encoding='utf-8') as f:
    ...
```

### Q12: 结果文件为空

**问题**: 生成的CSV文件为空

**解决方案**:
- 检查网络连接
- 增加等待时间
- 查看日志文件：
```bash
tail -f logs/processing.log
```

---

## 性能问题

### Q13: 处理速度慢

**问题**: 每个化合物需要很长时间

**解决方案**:
- 这是正常的，ProTox-3服务器需要时间计算
- 每个化合物通常需要5-10分钟
- 可以分批处理：
```bash
# 分批处理
python3 src/protox_full_automation.py 0 10   # 第一批
python3 src/protox_full_automation.py 10 20  # 第二批
```

### Q14: 内存占用高

**问题**: 系统内存不足

**解决方案**:
```bash
# 减少并发数
# 在代码中设置较小的batch_size

# 关闭无用的Chrome标签
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')
```

### Q15: 磁盘空间不足

**问题**: "No space left on device"

**解决方案**:
```bash
# 检查磁盘空间
df -h

# 清理旧的结果文件
rm -rf results/old_*

# 压缩日志文件
gzip logs/*.log
```

---

## 网络问题

### Q16: 连接超时

**问题**: "Connection timeout"

**解决方案**:
```python
# 增加超时时间
MAX_WAIT_TIME = 1800  # 30分钟

# 添加重试机制
for retry in range(3):
    try:
        # 执行操作
        break
    except TimeoutException:
        if retry == 2:
            raise
        time.sleep(60)
```

### Q17: 代理问题

**问题**: 需要通过代理访问

**解决方案**:
```python
# 设置代理
options.add_argument('--proxy-server=http://proxy:8080')

# 或设置环境变量
export http_proxy="http://proxy:8080"
export https_proxy="https://proxy:8080"
```

---

## 其他问题

### Q18: 权限错误

**问题**: "Permission denied"

**解决方案**:
```bash
# 添加执行权限
chmod +x setup.sh
chmod +x run_protox.sh

# 或使用sudo（不推荐）
sudo python3 src/protox_full_automation.py
```

### Q19: 日志文件过大

**问题**: 日志文件占用太多空间

**解决方案**:
```bash
# 清理旧日志
rm logs/*.log

# 或压缩
gzip logs/*.log

# 设置日志轮转
# 在代码中使用logging.handlers.RotatingFileHandler
```

### Q20: 找不到结果文件

**问题**: 处理完成但找不到输出

**解决方案**:
```bash
# 检查输出目录
ls -la results/

# 检查日志
tail -100 logs/processing.log

# 验证处理是否完成
grep "完成" logs/processing.log
```

---

## 调试技巧

### 启用详细日志

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 检查浏览器状态

```python
# 不使用无头模式，观察浏览器操作
# 注释掉这行
# options.add_argument('--headless')
```

### 保存截图

```python
# 在关键步骤保存截图
driver.save_screenshot('debug_screenshot.png')
```

---

## 获取帮助

如果以上方法都无法解决问题：

1. **查看日志文件**
   ```bash
   cat logs/processing.log
   ```

2. **搜索已知问题**
   - [GitHub Issues](https://github.com/YOUR_USERNAME/ProTox3-Automation/issues)

3. **创建新Issue**
   - 提供详细的错误信息
   - 包含系统信息
   - 附上相关日志

4. **联系维护者**
   - 通过GitHub Discussions
   - 提供完整的复现步骤

---

## 常用命令

```bash
# 检查Python版本
python3 --version

# 检查依赖
pip list

# 查看进程
ps aux | grep python

# 查看日志
tail -f logs/processing.log

# 清理环境
rm -rf venv/ results/ logs/

# 重新安装
bash setup.sh
```

---

**最后更新**: 2026-01-08

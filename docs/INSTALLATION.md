# 详细安装指南

本指南将帮助您在不同操作系统上安装和配置 ProTox3-Automation。

## 目录

- [系统要求](#系统要求)
- [Linux安装](#linux安装)
- [macOS安装](#macos安装)
- [Windows安装](#windows安装)
- [验证安装](#验证安装)
- [故障排除](#故障排除)

---

## 系统要求

### 最低配置

- **操作系统**: Linux, macOS, Windows 10+
- **Python**: 3.7 或更高版本
- **内存**: 至少 2GB RAM
- **磁盘空间**: 至少 1GB 可用空间
- **网络**: 稳定的互联网连接

### 推荐配置

- **操作系统**: Ubuntu 20.04+ / macOS 11+ / Windows 10+
- **Python**: 3.9 或更高版本
- **内存**: 4GB+ RAM
- **磁盘空间**: 5GB+ 可用空间
- **浏览器**: Chrome 或 Chromium 最新版本

---

## Linux安装

### Ubuntu/Debian

#### 1. 安装系统依赖

```bash
# 更新包列表
sudo apt update

# 安装Python和pip
sudo apt install python3 python3-pip python3-venv -y

# 安装Chrome浏览器
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f -y

# 或者安装Chromium
sudo apt install chromium-browser -y
```

#### 2. 克隆项目

```bash
git clone https://github.com/YOUR_USERNAME/ProTox3-Automation.git
cd ProTox3-Automation
```

#### 3. 运行安装脚本

```bash
bash setup.sh
```

### CentOS/RHEL

#### 1. 安装系统依赖

```bash
# 安装Python
sudo yum install python3 python3-pip -y

# 安装Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo yum localinstall google-chrome-stable_current_x86_64.rpm -y
```

#### 2. 继续按照Ubuntu步骤2-3操作

---

## macOS安装

### 使用Homebrew（推荐）

#### 1. 安装Homebrew（如果未安装）

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. 安装依赖

```bash
# 安装Python
brew install python3

# 安装Chrome
brew install --cask google-chrome
```

#### 3. 克隆项目

```bash
git clone https://github.com/YOUR_USERNAME/ProTox3-Automation.git
cd ProTox3-Automation
```

#### 4. 运行安装脚本

```bash
bash setup.sh
```

---

## Windows安装

### 使用WSL（推荐）

#### 1. 安装WSL2

```powershell
# 在PowerShell（管理员）中运行
wsl --install
```

#### 2. 安装Ubuntu

```powershell
wsl --install -d Ubuntu-22.04
```

#### 3. 在WSL中按照Linux安装步骤操作

### 原生Windows安装

#### 1. 安装Python

1. 访问 [Python官网](https://www.python.org/downloads/)
2. 下载Python 3.9+安装程序
3. 运行安装程序，**勾选 "Add Python to PATH"**
4. 完成安装

#### 2. 安装Chrome

1. 访问 [Chrome官网](https://www.google.com/chrome/)
2. 下载并安装Chrome浏览器

#### 3. 安装Git

1. 访问 [Git官网](https://git-scm.com/download/win)
2. 下载并安装Git

#### 4. 克隆项目

```cmd
git clone https://github.com/YOUR_USERNAME/ProTox3-Automation.git
cd ProTox3-Automation
```

#### 5. 创建虚拟环境

```cmd
python -m venv venv
venv\Scripts\activate
```

#### 6. 安装依赖

```cmd
pip install -r requirements.txt
```

---

## 验证安装

### 检查Python

```bash
python3 --version
# 应输出: Python 3.7.x 或更高
```

### 检查pip

```bash
pip3 --version
# 应输出: pip 21.x.x 或更高
```

### 检查依赖包

```bash
# 激活虚拟环境
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 检查Selenium
python -c "import selenium; print('Selenium:', selenium.__version__)"

# 检查RDKit
python -c "from rdkit import Chem; print('RDKit: OK')"
```

### 运行测试

```bash
# 处理示例数据
python3 src/protox_full_automation.py --test
```

---

## 故障排除

### 问题1: Python版本过低

**症状**: 提示 "Python 3.7+ required"

**解决方案**:
```bash
# 更新Python到最新版本
# Ubuntu
sudo apt install python3.9 -y

# macOS
brew install python@3.9

# Windows
# 从官网下载最新版本安装
```

### 问题2: pip安装失败

**症状**: "No module named 'pip'"

**解决方案**:
```bash
# Linux/macOS
python3 -m ensurepip --upgrade

# Windows
python -m ensurepip --upgrade
```

### 问题3: RDKit安装失败

**症状**: "ERROR: Could not build wheels for rdkit"

**解决方案**:
```bash
# 使用conda安装（推荐）
conda install -c conda-forge rdkit

# 或使用预编译版本
pip install rdkit-pypi
```

### 问题4: Chrome驱动问题

**症状**: "ChromeDriver not found"

**解决方案**:
```bash
# 自动安装ChromeDriver
pip install webdriver-manager

# 或手动下载
# 访问 https://chromedriver.chromium.org/
# 下载对应Chrome版本的驱动
```

### 问题5: 权限错误

**症状**: "Permission denied"

**解决方案**:
```bash
# 给脚本添加执行权限
chmod +x setup.sh
chmod +x run_protox.sh
```

### 问题6: 网络连接问题

**症状**: "Connection timeout"

**解决方案**:
- 检查网络连接
- 使用代理（如需要）
- 增加超时时间设置

---

## 高级配置

### 使用代理

如果需要通过代理访问网络：

```bash
# 设置环境变量
export http_proxy="http://proxy.example.com:8080"
export https_proxy="https://proxy.example.com:8080"
```

### 自定义安装路径

```bash
# 指定虚拟环境路径
python3 -m venv /path/to/custom/venv
source /path/to/custom/venv/bin/activate
```

### 离线安装

```bash
# 在有网络的机器上下载依赖
pip download -r requirements.txt -d packages/

# 在离线机器上安装
pip install --no-index --find-links=packages/ -r requirements.txt
```

---

## 更新

### 更新项目

```bash
cd ProTox3-Automation
git pull origin main
```

### 更新依赖

```bash
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

---

## 卸载

```bash
# 删除虚拟环境
rm -rf venv/

# 删除项目目录
cd ..
rm -rf ProTox3-Automation/
```

---

## 获取帮助

如果遇到其他问题：

1. 查看 [故障排除文档](TROUBLESHOOTING.md)
2. 搜索 [GitHub Issues](https://github.com/YOUR_USERNAME/ProTox3-Automation/issues)
3. 创建新的 Issue 并提供详细信息

---

**最后更新**: 2026-01-08

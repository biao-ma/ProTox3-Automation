#!/bin/bash

# ProTox3-Automation 一键安装脚本
# 版本: 1.0.0
# 日期: 2026-01-08

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 打印欢迎信息
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}         ProTox3-Automation 一键安装脚本                   ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}         版本: 1.0.0                                        ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# 检查操作系统
print_info "检查操作系统..."
OS=$(uname -s)
if [[ "$OS" == "Linux" ]]; then
    print_success "操作系统: Linux"
elif [[ "$OS" == "Darwin" ]]; then
    print_success "操作系统: macOS"
else
    print_error "不支持的操作系统: $OS"
    exit 1
fi

# 检查Python版本
print_info "检查Python版本..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python版本: $PYTHON_VERSION"
else
    print_error "未找到Python3，请先安装Python 3.7+"
    exit 1
fi

# 检查pip
print_info "检查pip..."
if command -v pip3 &> /dev/null; then
    print_success "pip已安装"
else
    print_error "未找到pip3，请先安装pip"
    exit 1
fi

# 检查Chrome/Chromium
print_info "检查Chrome/Chromium浏览器..."
if command -v google-chrome &> /dev/null || command -v chromium-browser &> /dev/null || command -v chromium &> /dev/null; then
    print_success "浏览器已安装"
else
    print_warning "未检测到Chrome/Chromium浏览器"
    print_info "请手动安装Chrome或Chromium浏览器"
    read -p "是否继续安装？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "安装已取消"
        exit 0
    fi
fi

# 创建虚拟环境
print_info "创建Python虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "虚拟环境已创建"
else
    print_warning "虚拟环境已存在，跳过创建"
fi

# 激活虚拟环境
print_info "激活虚拟环境..."
source venv/bin/activate
print_success "虚拟环境已激活"

# 升级pip
print_info "升级pip..."
pip install --upgrade pip -q
print_success "pip已升级"

# 安装依赖
print_info "安装Python依赖包..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt -q
    print_success "依赖包已安装"
else
    print_warning "未找到requirements.txt，手动安装核心依赖..."
    pip install selenium rdkit -q
    print_success "核心依赖已安装"
fi

# 创建必要的目录
print_info "创建项目目录..."
mkdir -p data
mkdir -p results
mkdir -p logs
print_success "目录已创建"

# 检查示例数据文件
if [ ! -f "data/example_input.csv" ]; then
    print_info "创建示例数据文件..."
    cat > data/example_input.csv << 'EOF'
PubChem_ID,SMILES
311434,CC1=CC(=NO1)NC(=O)NC2=CC(=C(C=C2OC)OC)Cl
54576693,C1CN(CCN1CC2=CC3=C(C=C2)OC(O3)(F)F)C(=O)NC4=C(C=CN=C4)Cl
EOF
    print_success "示例数据文件已创建"
fi

# 设置执行权限
print_info "设置脚本执行权限..."
chmod +x run_protox.sh
if [ -f "src/protox_full_automation.py" ]; then
    chmod +x src/protox_full_automation.py
fi
print_success "执行权限已设置"

# 验证安装
print_info "验证安装..."
python3 -c "import selenium; print('Selenium版本:', selenium.__version__)" 2>/dev/null && print_success "Selenium安装成功" || print_warning "Selenium未安装"
python3 -c "from rdkit import Chem; print('RDKit安装成功')" 2>/dev/null && print_success "RDKit安装成功" || print_warning "RDKit未安装"

# 打印完成信息
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC}                  安装完成！                                ${GREEN}║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

print_info "下一步操作："
echo "  1. 将您的CSV文件放入 data/ 目录"
echo "  2. 确保CSV文件包含 PubChem_ID 和 SMILES 列"
echo "  3. 运行命令："
echo ""
echo -e "     ${YELLOW}bash run_protox.sh${NC}"
echo ""
echo "  或者直接运行Python脚本："
echo ""
echo -e "     ${YELLOW}source venv/bin/activate${NC}"
echo -e "     ${YELLOW}python3 src/protox_full_automation.py${NC}"
echo ""

print_info "更多信息请查看："
echo "  - README.md - 项目概览"
echo "  - docs/QUICK_START.md - 快速开始"
echo "  - docs/USER_GUIDE.md - 用户指南"
echo ""

print_success "祝您使用愉快！"
echo ""

#!/bin/bash

# ProTox-3 快速启动脚本
# 使用方法: bash run_protox.sh [start] [end]
# 示例: bash run_protox.sh 0 10

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
VENV_PATH="/home/ubuntu/venv"
SCRIPT_PATH="/home/ubuntu/protox_full_automation.py"
OUTPUT_DIR="/home/ubuntu/protox_results"

# 函数：打印带颜色的消息
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

# 检查虚拟环境
print_info "检查虚拟环境..."
if [ ! -d "$VENV_PATH" ]; then
    print_warning "虚拟环境不存在，正在创建..."
    python3 -m venv "$VENV_PATH"
    print_success "虚拟环境已创建"
fi

# 激活虚拟环境
print_info "激活虚拟环境..."
source "$VENV_PATH/bin/activate"
print_success "虚拟环境已激活"

# 检查必要的包
print_info "检查依赖包..."
pip install -q selenium rdkit 2>/dev/null || true

# 验证脚本存在
if [ ! -f "$SCRIPT_PATH" ]; then
    print_error "脚本不存在: $SCRIPT_PATH"
    exit 1
fi

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 获取命令行参数
START_IDX=${1:-0}
END_IDX=${2:-}

# 打印启动信息
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}         ProTox-3 细胞毒性预测自动化脚本                   ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

print_info "配置信息:"
echo "  虚拟环境: $VENV_PATH"
echo "  脚本路径: $SCRIPT_PATH"
echo "  输出目录: $OUTPUT_DIR"
echo ""

if [ -z "$END_IDX" ]; then
    print_info "处理范围: 从第 $START_IDX 个开始（处理所有剩余化合物）"
    echo ""
    print_warning "注意: 处理所有97个化合物需要约8-16小时"
    echo ""
    read -p "是否继续? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "已取消"
        exit 0
    fi
    echo ""
    python3 "$SCRIPT_PATH" "$START_IDX"
else
    print_info "处理范围: 从第 $START_IDX 个到第 $END_IDX 个（共 $((END_IDX - START_IDX)) 个化合物）"
    echo ""
    print_warning "注意: 处理 $((END_IDX - START_IDX)) 个化合物需要约 $(( (END_IDX - START_IDX) * 7 / 60 ))-$(( (END_IDX - START_IDX) * 10 / 60 )) 小时"
    echo ""
    read -p "是否继续? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "已取消"
        exit 0
    fi
    echo ""
    python3 "$SCRIPT_PATH" "$START_IDX" "$END_IDX"
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC}                  处理完成！                               ${GREEN}║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# 显示结果统计
COMPLETED=$(ls "$OUTPUT_DIR"/CID_*.csv 2>/dev/null | wc -l)
print_success "已完成的化合物数: $COMPLETED"

if [ -f "$OUTPUT_DIR/cytotoxicity_summary.csv" ]; then
    SUMMARY_LINES=$(wc -l < "$OUTPUT_DIR/cytotoxicity_summary.csv")
    print_success "汇总文件行数: $((SUMMARY_LINES - 1)) 个化合物（包括表头）"
    print_success "汇总文件位置: $OUTPUT_DIR/cytotoxicity_summary.csv"
fi

echo ""
print_info "日志文件: $OUTPUT_DIR/processing_log.txt"
echo ""

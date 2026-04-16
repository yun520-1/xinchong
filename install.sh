#!/bin/bash
#
# 心虫安装脚本
# 用法: bash install.sh [选项]
#
# 选项:
#   --core       仅安装核心层（真善美 + 决策引擎）
#   --full       安装全部模块
#   --psychology 安装心理模块
#   --memory     安装记忆模块
#   --embodied   安装具身认知模块
#   --help       显示帮助
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐛 心虫 (XinChong) 安装脚本${NC}"
echo ""

# 解析参数
INSTALL_CORE=false
INSTALL_PSYCHOLOGY=false
INSTALL_MEMORY=false
INSTALL_EMBODY=false

for arg in "$@"; do
    case $arg in
        --core)
            INSTALL_CORE=true
            ;;
        --full)
            INSTALL_CORE=true
            INSTALL_PSYCHOLOGY=true
            INSTALL_MEMORY=true
            INSTALL_EMBODY=true
            ;;
        --psychology)
            INSTALL_PSYCHOLOGY=true
            ;;
        --memory)
            INSTALL_MEMORY=true
            ;;
        --embodied)
            INSTALL_EMBODY=true
            ;;
        --help)
            echo "用法: $0 [选项]"
            echo ""
            echo "选项:"
            echo "  --core       仅安装核心层（真善美 + 决策引擎）"
            echo "  --full       安装全部模块"
            echo "  --psychology 安装心理模块"
            echo "  --memory     安装记忆模块"
            echo "  --embodied   安装具身认知模块"
            exit 0
            ;;
    esac
done

# 默认安装核心层
if [ "$INSTALL_CORE" = false ] && [ "$INSTALL_PSYCHOLOGY" = false ] && [ "$INSTALL_MEMORY" = false ] && [ "$INSTALL_EMBODY" = false ]; then
    INSTALL_CORE=true
fi

echo -e "${YELLOW}安装选项:${NC}"
[ "$INSTALL_CORE" = true ] && echo "  ✓ 核心层（真善美 + 决策引擎）"
[ "$INSTALL_PSYCHOLOGY" = true ] && echo "  ✓ 心理层（PHQ-9 + GAD-7 + 危机预警）"
[ "$INSTALL_MEMORY" = true ] && echo "  ✓ 记忆层（长期记忆 + 会话索引）"
[ "$INSTALL_EMBODY" = true ] && echo "  ✓ 具身层（双系统 + 7步思维链）"
echo ""

# 检查 Python 版本
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${YELLOW}检测到 Python 版本: ${PYTHON_VERSION}${NC}"

# 检查 pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}错误: pip3 未安装${NC}"
    exit 1
fi

# 安装
echo ""
echo -e "${GREEN}开始安装...${NC}"

# 创建目标目录
INSTALL_DIR="$HOME/.xinchong"
mkdir -p "$INSTALL_DIR"

# 安装到 Python 包
pip3 install -e .

echo ""
echo -e "${GREEN}✅ 安装完成！${NC}"
echo ""
echo "使用示例："
echo "  python3 -c \"from xinchong import XinChong; xin = XinChong(); print(xin.chat('你好'))\""
echo ""
echo "详细文档请查看: README.md"
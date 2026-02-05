#!/bin/bash

# 同步向量数据库到服务器脚本
# 用途：将本地生成的向量数据库推送到服务器

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "======================================"
echo "同步向量数据库到服务器"
echo "======================================"
echo ""

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LANGUAGE="${1:-zh}"

echo -e "${YELLOW}配置信息：${NC}"
echo "  语言: $LANGUAGE"
echo "  项目目录: $PROJECT_ROOT"
echo ""

# 进入项目目录
cd "$PROJECT_ROOT/mcp"

# 检查向量数据库是否存在
if [ ! -d "data/chroma" ]; then
    echo -e "${RED}✗ 错误: 向量数据库不存在${NC}"
    echo "请先运行: ./scripts/build_vector_local.sh"
    exit 1
fi

# 打包向量数据库
echo -e "${YELLOW}打包向量数据库...${NC}"
PACKAGE_FILE="chroma-data-${LANGUAGE}.tar.gz"
tar -czf "$PACKAGE_FILE" data/chroma/
PACKAGE_SIZE=$(du -h "$PACKAGE_FILE" | cut -f1)
echo -e "${GREEN}✓ 打包完成: $PACKAGE_FILE ($PACKAGE_SIZE)${NC}"
echo ""

# 读取服务器配置
if [ -f ".sync_config" ]; then
    source .sync_config
    echo -e "${YELLOW}从配置文件读取服务器信息...${NC}"
else
    echo -e "${YELLOW}请输入服务器信息：${NC}"
    read -p "服务器地址: " SERVER_HOST
    read -p "SSH 用户名: " SERVER_USER
    read -p "服务器路径 (默认: /path/to/mcp): " SERVER_PATH
    SERVER_PATH="${SERVER_PATH:-/path/to/mcp}"
fi

echo ""
echo -e "${YELLOW}推送到服务器...${NC}"
echo "  服务器: ${SERVER_USER}@${SERVER_HOST}"
echo "  路径: ${SERVER_PATH}"
echo ""

# 推送文件
scp "$PACKAGE_FILE" "${SERVER_USER}@${SERVER_HOST}:${SERVER_PATH}/"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 推送成功${NC}"
    echo ""
    echo -e "${YELLOW}下一步操作：${NC}"
    echo "  1. SSH 登录服务器:"
    echo "     ssh ${SERVER_USER}@${SERVER_HOST}"
    echo ""
    echo "  2. 解压向量数据库:"
    echo "     cd ${SERVER_PATH}"
    echo "     tar -xzf ${PACKAGE_FILE}"
    echo ""
    echo "  3. 重启 MCP 服务:"
    echo "     sudo systemctl restart mcp"
    echo ""
    echo -e "${YELLOW}或者使用一键命令：${NC}"
    echo "  ssh ${SERVER_USER}@${SERVER_HOST} 'cd ${SERVER_PATH} && tar -xzf ${PACKAGE_FILE} && sudo systemctl restart mcp'"
else
    echo -e "${RED}✗ 推送失败${NC}"
    exit 1
fi

# 保存配置（如果首次运行）
if [ ! -f ".sync_config" ]; then
    echo ""
    echo -e "${YELLOW}是否保存服务器配置？(y/n)${NC}"
    read -p "选择: " SAVE_CONFIG
    
    if [ "$SAVE_CONFIG" = "y" ] || [ "$SAVE_CONFIG" = "Y" ]; then
        cat > .sync_config << EOF
SERVER_HOST="$SERVER_HOST"
SERVER_USER="$SERVER_USER"
SERVER_PATH="$SERVER_PATH"
EOF
        echo -e "${GREEN}✓ 配置已保存到 .sync_config${NC}"
        echo -e "${YELLOW}下次运行将自动使用此配置${NC}"
    fi
fi

echo ""
echo "======================================"
echo -e "${GREEN}完成！${NC}"
echo "======================================"

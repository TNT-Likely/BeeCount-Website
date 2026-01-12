#!/bin/bash

# 本地生成高精度向量数据库脚本
# 用途：在本地使用高精度模型生成向量数据库，然后推送到服务器

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "======================================"
echo "本地生成高精度向量数据库"
echo "======================================"
echo ""

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
MODEL_NAME="paraphrase-multilingual-MiniLM-L12-v2"
LANGUAGE="${1:-ALL}"

echo -e "${YELLOW}配置信息：${NC}"
echo "  模型: $MODEL_NAME"
echo "  语言: $LANGUAGE"
echo "  项目目录: $PROJECT_ROOT"
echo ""

# 进入项目目录
cd "$PROJECT_ROOT/mcp"

# 备份现有向量数据库
if [ -d "data/chroma" ]; then
    echo -e "${YELLOW}备份现有向量数据库...${NC}"
    BACKUP_FILE="chroma-backup-$(date +%Y%m%d-%H%M%S).tar.gz"
    tar -czf "$BACKUP_FILE" data/chroma/
    echo -e "${GREEN}✓ 备份完成: $BACKUP_FILE${NC}"
    echo ""
fi

# 生成向量数据库
echo -e "${YELLOW}生成向量数据库...${NC}"
echo "这可能需要几分钟时间，请耐心等待..."
echo ""

EMBEDDING_MODEL="$MODEL_NAME" python run_server.py --rebuild-index --language "$LANGUAGE" --force

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 向量数据库生成成功${NC}"
    echo ""
    
    # 显示统计信息
    echo -e "${YELLOW}向量数据库统计：${NC}"
    if [ "$LANGUAGE" = "ALL" ]; then
        python -c "
from src.vector_store import get_vector_store
zh_stats = get_vector_store().get_stats('zh')
en_stats = get_vector_store().get_stats('en')
print(f'  中文 (zh): {zh_stats[\"total_chunks\"]} chunks, {zh_stats[\"total_documents\"]} documents')
print(f'  英文 (en): {en_stats[\"total_chunks\"]} chunks, {en_stats[\"total_documents\"]} documents')
print(f'  总计: {zh_stats[\"total_chunks\"] + en_stats[\"total_chunks\"]} chunks')
"
    else
        python -c "
from src.vector_store import get_vector_store
stats = get_vector_store().get_stats('$LANGUAGE')
print(f'  总块数: {stats[\"total_chunks\"]}')
print(f'  总文档数: {stats[\"total_documents\"]}')
print(f'  集合名称: {stats[\"collection_name\"]}')
print(f'  模型: {stats[\"model\"][\"model_name\"]}')
print(f'  向量维度: {stats[\"model\"][\"dimension\"]}')
"
    fi
    echo ""
    
    # 打包向量数据库
    echo -e "${YELLOW}打包向量数据库...${NC}"
    PACKAGE_FILE="chroma-data-${LANGUAGE}.tar.gz"
    tar -czf "$PACKAGE_FILE" data/chroma/
    PACKAGE_SIZE=$(du -h "$PACKAGE_FILE" | cut -f1)
    echo -e "${GREEN}✓ 打包完成: $PACKAGE_FILE ($PACKAGE_SIZE)${NC}"
    echo ""
    
    # 询问是否推送到服务器
    echo -e "${YELLOW}是否推送到服务器？${NC}"
    read -p "输入服务器地址 (或按 Enter 跳过): " SERVER_HOST
    
    if [ -n "$SERVER_HOST" ]; then
        read -p "输入 SSH 用户名: " SERVER_USER
        read -p "输入服务器路径 (默认: /path/to/mcp): " SERVER_PATH
        SERVER_PATH="${SERVER_PATH:-/path/to/mcp}"
        
        echo ""
        echo -e "${YELLOW}推送到服务器...${NC}"
        scp "$PACKAGE_FILE" "${SERVER_USER}@${SERVER_HOST}:${SERVER_PATH}/"
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ 推送成功${NC}"
            echo ""
            echo -e "${YELLOW}下一步操作：${NC}"
            echo "  1. SSH 登录服务器: ssh ${SERVER_USER}@${SERVER_HOST}"
            echo "  2. 解压向量数据库: cd ${SERVER_PATH} && tar -xzf ${PACKAGE_FILE}"
            echo "  3. 重启 MCP 服务: sudo systemctl restart mcp"
        else
            echo -e "${RED}✗ 推送失败${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}已跳过推送${NC}"
        echo ""
        echo -e "${YELLOW}手动推送命令：${NC}"
        echo "  scp $PACKAGE_FILE user@server:/path/to/mcp/"
    fi
else
    echo -e "${RED}✗ 向量数据库生成失败${NC}"
    exit 1
fi

echo ""
echo "======================================"
echo -e "${GREEN}完成！${NC}"
echo "======================================"

#!/bin/bash

# 自动重建向量数据库脚本
# 用途：文档更新后自动触发向量索引重建

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LANGUAGE="${1:-ALL}"
LOG_FILE="/tmp/mcp_rebuild_$(date +%Y%m%d_%H%M%S).log"

echo "======================================"
echo "自动重建向量数据库"
echo "======================================"
echo ""

echo -e "${YELLOW}配置信息：${NC}"
echo "  语言: $LANGUAGE"
echo "  日志文件: $LOG_FILE"
echo ""

# 进入项目目录
cd "$PROJECT_ROOT/mcp"

# 检查虚拟环境
if [ ! -d "mcp_env" ]; then
    echo -e "${RED}✗ 错误: 虚拟环境不存在${NC}"
    echo "请先运行部署脚本: ./deploy.sh"
    exit 1
fi

# 激活虚拟环境
source mcp_env/bin/activate

# 检查服务是否运行
if pgrep -f "python.*run_server.py" > /dev/null; then
    echo -e "${YELLOW}检测到 MCP 服务正在运行${NC}"
    echo "服务将在重建后自动重启"
    echo ""
fi

# 开始重建
echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] 开始重建向量索引...${NC}"
echo "详细信息请查看日志: $LOG_FILE"
echo ""

# 后台重建
nohup python run_server.py --rebuild-index --language "$LANGUAGE" > "$LOG_FILE" 2>&1 &
REBUILD_PID=$!

echo -e "${GREEN}✓ 重建进程已启动 (PID: $REBUILD_PID)${NC}"
echo ""

# 等待几秒确保进程启动
sleep 3

# 检查进程是否还在运行
if ! ps -p $REBUILD_PID > /dev/null; then
    echo -e "${RED}✗ 错误: 重建进程启动失败${NC}"
    echo "请查看日志: $LOG_FILE"
    exit 1
fi

echo -e "${YELLOW}监控重建进度：${NC}"
echo "  tail -f $LOG_FILE"
echo ""
echo -e "${YELLOW}或等待完成通知...${NC}"
echo ""

# 监控进程
while ps -p $REBUILD_PID > /dev/null; do
    sleep 5
done

# 检查退出状态
wait $REBUILD_PID
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo -e "${GREEN}======================================"
    echo "✓ 向量索引重建成功！"
    echo "======================================${NC}"
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
"
    fi
    echo ""
    
    # 如果服务在运行，提示重启
    if pgrep -f "python.*run_server.py" > /dev/null; then
        echo -e "${YELLOW}检测到 MCP 服务正在运行${NC}"
        echo -e "${YELLOW}建议重启服务以使用新的向量索引${NC}"
        echo ""
        echo -e "${YELLOW}重启命令：${NC}"
        echo "  sudo systemctl restart mcp"
    fi
else
    echo ""
    echo -e "${RED}======================================"
    echo "✗ 向量索引重建失败！"
    echo "======================================${NC}"
    echo ""
    echo -e "${YELLOW}查看错误日志：${NC}"
    echo "  tail -n 50 $LOG_FILE"
    exit 1
fi

# 清理旧日志（保留最近7天）
find /tmp -name "mcp_rebuild_*.log" -mtime +7 -delete 2>/dev/null || true

echo ""
echo "======================================"
echo -e "${GREEN}完成！${NC}"
echo "======================================"

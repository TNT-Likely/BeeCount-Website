#!/bin/bash

# BeeCount MCP Server 部署脚本 (Linux/Mac)
# 用途：在轻量服务器上部署 MCP 服务

set -e

echo "======================================"
echo "BeeCount MCP Server 部署脚本"
echo "======================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 Python 版本
echo -e "${YELLOW}[1/8] 检查 Python 版本...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到 Python3${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✓ Python 版本: $PYTHON_VERSION${NC}"
echo ""

# 检查系统资源
echo -e "${YELLOW}[2/8] 检查系统资源...${NC}"
TOTAL_MEM=$(free -m | awk '/Mem:/ {print $2}')
AVAILABLE_MEM=$(free -m | awk '/Mem:/ {print $7}')
DISK_SPACE=$(df -m . | awk 'NR==2 {print $4}')

echo "可用内存: ${AVAILABLE_MEM}MB / ${TOTAL_MEM}MB"
echo "可用磁盘: ${DISK_SPACE}MB"

if [ "$AVAILABLE_MEM" -lt 1024 ]; then
    echo -e "${YELLOW}警告: 可用内存不足 1GB，建议使用轻量模型${NC}"
fi

if [ "$DISK_SPACE" -lt 2048 ]; then
    echo -e "${YELLOW}警告: 可用磁盘不足 2GB，可能无法安装模型${NC}"
fi
echo ""

# 选择模型
echo -e "${YELLOW}[3/8] 选择嵌入模型...${NC}"
echo "请选择嵌入模型（影响内存占用和搜索精度）："
echo "  1) paraphrase-multilingual-MiniLM-L12-v2 (420MB, 高精度, 推荐)"
echo "  2) paraphrase-multilingual-MiniLM-L6-v2 (200MB, 平衡, 轻量服务器)"
echo "  3) paraphrase-multilingual-MiniLM-L8-v2 (300MB, 中等精度)"
echo ""
read -p "请输入选项 [1-3] (默认: 2): " MODEL_CHOICE
MODEL_CHOICE=${MODEL_CHOICE:-2}

case $MODEL_CHOICE in
    1)
        EMBEDDING_MODEL="paraphrase-multilingual-MiniLM-L12-v2"
        echo -e "${GREEN}✓ 选择模型: $EMBEDDING_MODEL (420MB)${NC}"
        ;;
    2)
        EMBEDDING_MODEL="paraphrase-multilingual-MiniLM-L6-v2"
        echo -e "${GREEN}✓ 选择模型: $EMBEDDING_MODEL (200MB)${NC}"
        ;;
    3)
        EMBEDDING_MODEL="paraphrase-multilingual-MiniLM-L8-v2"
        echo -e "${GREEN}✓ 选择模型: $EMBEDDING_MODEL (300MB)${NC}"
        ;;
    *)
        echo -e "${RED}无效选项，使用默认模型${NC}"
        EMBEDDING_MODEL="paraphrase-multilingual-MiniLM-L6-v2"
        ;;
esac
echo ""

# 创建虚拟环境
echo -e "${YELLOW}[4/8] 创建虚拟环境...${NC}"
if [ -d "mcp_env" ]; then
    echo -e "${YELLOW}虚拟环境已存在，跳过创建${NC}"
else
    python3 -m venv mcp_env
    echo -e "${GREEN}✓ 虚拟环境创建成功${NC}"
fi
echo ""

# 激活虚拟环境
echo -e "${YELLOW}[5/8] 激活虚拟环境并安装依赖...${NC}"
source mcp_env/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ 依赖安装完成${NC}"
echo ""

# 配置环境变量
echo -e "${YELLOW}[6/8] 配置环境变量...${NC}"
if [ -f ".env" ]; then
    echo -e "${YELLOW}.env 文件已存在，跳过创建${NC}"
else
    cp .env.example .env
    
    # 更新模型配置
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/^EMBEDDING_MODEL=.*/EMBEDDING_MODEL=$EMBEDDING_MODEL/" .env
    else
        sed -i "s/^EMBEDDING_MODEL=.*/EMBEDDING_MODEL=$EMBEDDING_MODEL/" .env
    fi
    
    echo -e "${GREEN}✓ .env 文件创建成功${NC}"
    echo -e "${YELLOW}请根据需要修改 .env 文件中的其他配置${NC}"
fi
echo ""

# 生成向量索引
echo -e "${YELLOW}[7/8] 生成向量索引...${NC}"
echo "这可能需要几分钟时间，请耐心等待..."
python run_server.py --rebuild-index
echo -e "${GREEN}✓ 向量索引生成完成${NC}"
echo ""

# 测试服务
echo -e "${YELLOW}[8/8] 测试 MCP 服务...${NC}"
python tests/test_basic.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 基础测试通过${NC}"
else
    echo -e "${YELLOW}基础测试失败，请检查日志${NC}"
fi

python tests/test_vector.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 向量搜索测试通过${NC}"
else
    echo -e "${YELLOW}向量搜索测试失败，请检查日志${NC}"
fi
echo ""

# 完成
echo "======================================"
echo -e "${GREEN}部署完成！${NC}"
echo "======================================"
echo ""
echo "启动 MCP 服务:"
echo "  source mcp_env/bin/activate"
echo "  python run_server.py"
echo ""
echo "后台运行:"
echo "  nohup python run_server.py > mcp.log 2>&1 &"
echo ""
echo "使用 systemd 服务 (推荐):"
echo "  sudo cp mcp.service /etc/systemd/system/"
echo "  sudo systemctl daemon-reload"
echo "  sudo systemctl enable mcp"
echo "  sudo systemctl start mcp"
echo ""
echo -e "${YELLOW}提示: 向量数据库已生成，后续文档更新后需要重新构建索引${NC}"
echo -e "${YELLOW}提示: 重建索引命令: python run_server.py --rebuild-index --language ALL${NC}"

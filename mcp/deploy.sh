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

# 获取脚本所在目录的完整路径
script_dir=$(dirname "$(realpath "$0")")

# 确定mcp项目目录
# 如果脚本在mcp目录内（即script_dir以mcp结尾），则mcp_project_dir就是script_dir
# 否则，假设当前目录下有mcp文件夹
if [[ "$script_dir" =~ /mcp$ ]]; then
    mcp_project_dir="$script_dir"
else
    mcp_project_dir="$(pwd)/mcp"
fi

# 定义虚拟环境目录（mcp同级）
mcp_parent_dir=$(dirname "$mcp_project_dir")
venv_dir="$mcp_parent_dir/mcp_env"

# 检查mcp项目目录是否存在
if [ ! -d "$mcp_project_dir" ]; then
    echo -e "${RED}✗ 错误: 未找到mcp项目目录！${NC}"
    echo -e "${RED}  使用方法1：在mcp的同级目录执行 ./mcp/deploy.sh${NC}"
    echo -e "${RED}  使用方法2：进入mcp目录执行 ./deploy.sh${NC}"
    exit 1
fi
echo -e "${GREEN}✓ 定位到MCP项目目录: $mcp_project_dir${NC}"
echo ""

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
echo -e "${YELLOW}[4/8] 创建虚拟环境（mcp同级）...${NC}"
if [ -d "$venv_dir" ]; then
    echo -e "${YELLOW}虚拟环境已存在（$venv_dir），跳过创建${NC}"
else
    python3 -m venv "$venv_dir"
    echo -e "${GREEN}✓ 虚拟环境创建成功: $venv_dir${NC}"
fi
echo ""

# 激活虚拟环境并安装依赖
echo -e "${YELLOW}[5/8] 激活虚拟环境并安装依赖...${NC}"
# 激活虚拟环境
source "$venv_dir/bin/activate"

requirements_path="$mcp_project_dir/requirements.txt"
if [ ! -f "$requirements_path" ]; then
    echo -e "${RED}✗ 错误: 未找到requirements.txt（路径：$requirements_path）${NC}"
    exit 1
fi

pip install --upgrade pip
pip install -r "$requirements_path"
echo -e "${GREEN}✓ 依赖安装完成${NC}"
echo ""

# 配置环境变量
echo -e "${YELLOW}[6/8] 配置环境变量...${NC}"
env_example_path="$mcp_project_dir/.env.example"
env_path="$mcp_project_dir/.env"

if [ -f "$env_path" ]; then
    echo -e "${YELLOW}.env 文件已存在（$env_path），跳过创建${NC}"
else
    if [ ! -f "$env_example_path" ]; then
        echo -e "${RED}✗ 错误: 未找到.env.example（路径：$env_example_path）${NC}"
        exit 1
    fi
    cp "$env_example_path" "$env_path"
    
    # 更新模型配置
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/^EMBEDDING_MODEL=.*/EMBEDDING_MODEL=$EMBEDDING_MODEL/" "$env_path"
    else
        sed -i "s/^EMBEDDING_MODEL=.*/EMBEDDING_MODEL=$EMBEDDING_MODEL/" "$env_path"
    fi
    
    echo -e "${GREEN}✓ .env 文件创建成功: $env_path${NC}"
    echo -e "${YELLOW}请根据需要修改 .env 文件中的其他配置${NC}"
fi
echo ""

# 生成向量索引
echo -e "${YELLOW}[7/8] 生成向量索引...${NC}"
run_server_path="$mcp_project_dir/run_server.py"
if [ ! -f "$run_server_path" ]; then
    echo -e "${RED}✗ 错误: 未找到run_server.py（路径：$run_server_path）${NC}"
    exit 1
fi

echo "这可能需要几分钟时间，请耐心等待..."
# 切换到mcp目录执行脚本（避免路径相关的相对导入问题）
cd "$mcp_project_dir"
python run_server.py --rebuild-index --language ALL --force
echo -e "${GREEN}✓ 向量索引生成完成${NC}"
echo ""

# 测试服务
echo -e "${YELLOW}[8/8] 测试 MCP 服务...${NC}"
# 确保在mcp目录内执行测试
cd "$mcp_project_dir"

# 测试基础功能
test_result=$(python tests/test_basic.py 2>&1)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 基础测试通过${NC}"
else
    echo -e "${YELLOW}⚠ 基础测试失败，请检查日志${NC}"
    echo "测试输出: $test_result"
fi

# 测试向量搜索
test_result=$(python tests/test_vector.py 2>&1)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 向量搜索测试通过${NC}"
else
    echo -e "${YELLOW}⚠ 向量搜索测试失败，请检查日志${NC}"
    echo "测试输出: $test_result"
fi
echo ""

# 完成
echo "======================================"
echo -e "${GREEN}部署完成！${NC}"
echo "======================================"
echo ""
echo "当前目录结构（推荐）："
echo "  $mcp_parent_dir/"
echo "  ├── mcp/ (项目代码目录)"
echo "  └── mcp_env/ (虚拟环境目录)"
echo ""
echo "启动 MCP 服务步骤:"
echo "  1. 激活虚拟环境: source $venv_dir/bin/activate"
echo "  2. 进入mcp目录: cd $mcp_project_dir"
echo "  3. 启动服务: python run_server.py"
echo ""
echo "后台运行:"
echo "  source $venv_dir/bin/activate"
echo "  cd $mcp_project_dir"
echo "  nohup python run_server.py > mcp.log 2>&1 &"
echo ""
echo "使用 systemd 服务 (推荐):"
echo "  sudo cp $mcp_project_dir/mcp.service /etc/systemd/system/"
echo "  sudo systemctl daemon-reload"
echo "  sudo systemctl enable mcp"
echo "  sudo systemctl start mcp"
echo ""
echo -e "${YELLOW}提示: 向量数据库已生成，后续文档更新后需要重新构建索引${NC}"
echo -e "${YELLOW}提示: 重建索引命令: cd $mcp_project_dir && python run_server.py --rebuild-index --language ALL${NC}"

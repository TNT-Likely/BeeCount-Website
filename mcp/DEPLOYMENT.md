# BeeCount MCP Server 部署指南

本指南详细说明如何在服务器上部署 BeeCount MCP 服务。

## 目录

- [快速开始](#快速开始)
- [系统要求](#系统要求)
- [部署方式](#部署方式)
  - [方式 1: 自动部署脚本](#方式-1-自动部署脚本)
  - [方式 2: 手动部署](#方式-2-手动部署)
  - [方式 3: 高级部署方案](#方式-3-高级部署方案)
- [配置说明](#配置说明)
- [生产环境部署](#生产环境部署)
- [常见问题](#常见问题)

## 快速开始

### 一键部署（推荐）

```bash
# Linux/Mac
cd mcp
chmod +x deploy.sh
./deploy.sh

# Windows
cd mcp
.\deploy.ps1
```

部署脚本会自动完成：
- ✅ 检查系统资源
- ✅ 选择合适的模型
- ✅ 安装依赖
- ✅ 配置环境变量
- ✅ 生成向量索引
- ✅ 运行测试

## 系统要求

### 最低配置

| 资源 | 要求 | 说明 |
|-------|------|------|
| CPU | 1核 | 单核即可运行 |
| 内存 | 1GB | 使用 L6-v2 模型 |
| 磁盘 | 2GB | 模型 + 向量数据库 |
| Python | 3.8+ | 推荐 3.10+ |

### 推荐配置

| 资源 | 要求 | 说明 |
|-------|------|------|
| CPU | 2核+ | 更快的向量计算 |
| 内存 | 2-4GB | 使用 L8-v2 或 L12-v2 模型 |
| 磁盘 | 5GB+ | 预留空间增长 |
| Python | 3.10+ | 最新稳定版 |

### 模型资源需求

| 模型 | 大小 | 内存占用 | CPU 需求 |
|------|------|---------|----------|
| L6-v2 | 200MB | ~800MB | 1核 |
| L8-v2 | 300MB | ~1.2GB | 1-2核 |
| L12-v2 | 420MB | ~1.5GB | 2核+ |
| mpnet-base-v2 | 420MB | ~1.5GB | 2核+ |

## 部署方式

### 方式 1: 自动部署脚本

#### Linux/Mac

```bash
# 1. 进入项目目录
cd /path/to/BeeCount-Website/mcp

# 2. 赋予执行权限
chmod +x deploy.sh

# 3. 运行部署脚本
./deploy.sh

# 4. 按提示选择模型
# 推荐轻量服务器选择选项 2 (L6-v2)
```

#### Windows

```powershell
# 1. 进入项目目录
cd D:\Work\code\BeeCount-Website\mcp

# 2. 运行部署脚本（PowerShell）
.\deploy.ps1

# 3. 按提示选择模型
# 推荐轻量服务器选择选项 2 (L6-v2)
```

### 方式 2: 手动部署

#### 步骤 1: 创建虚拟环境

```bash
# Linux/Mac
python3 -m venv mcp_env
source mcp_env/bin/activate

# Windows
python -m venv mcp_env
mcp_env\Scripts\activate
```

#### 步骤 2: 安装依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 步骤 3: 配置环境变量

```bash
# 复制示例配置
cp .env.example .env

# 编辑配置文件
nano .env  # 或使用其他编辑器
```

关键配置项：
```bash
# 选择模型（根据服务器内存调整）
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L6-v2

# 日志级别（生产环境建议 INFO）
LOG_LEVEL=INFO

# 网站URL（用于生成文档链接）
WEBSITE_URL=https://beecount.youths.cc
```

#### 步骤 4: 生成向量索引

```bash
# 生成中文文档索引
python run_server.py --rebuild-index --language zh

# 生成英文文档索引（如果需要）
python run_server.py --rebuild-index --language en
```

#### 步骤 5: 测试服务

```bash
# 运行基础测试
python tests/test_basic.py

# 运行向量搜索测试
python tests/test_vector.py
```

#### 步骤 6: 启动服务
```bash
# 前台运行（测试）
python run_server.py

# 后台运行（生产）
nohup python run_server.py > mcp.log 2>&1 &
```

### 方式 3: 高级部署方案

本节介绍适合特定场景的高级部署方案，请根据你的需求选择。

#### 方案 A: 本地生成高精度向量 + 服务器查询

**适用场景：**
- 本地机器配置高（内存充足）
- 服务器资源有限（轻量服务器）
- 对搜索精度要求高
- 文档更新频率较低

**架构说明：**
```
本地开发机（高配置）
  └─ L12-v2 模型（420MB）
      ├─ 生成文档向量（高精度）
      └─ 生成向量数据库
              ↓
         推送到服务器
              ↓
生产服务器（轻量）
  └─ L12-v2 模型（仅用于查询）
      ├─ 接收向量数据库
      ├─ 查询向量生成
      └─ 向量搜索
```

**优点：**
- ✅ 使用高精度模型（L12-v2）
- ✅ 搜索质量最高
- ✅ 服务器不需要重新生成向量
- ✅ 适合文档更新频率低的场景

**缺点：**
- ❌ 服务器仍需运行 L12-v2 模型（~1.5GB 内存）
- ❌ 需要手动同步向量数据库
- ❌ 文档更新需要手动触发

**实施步骤：**

```bash
# 1. 本地生成向量数据库（使用高精度模型）
cd mcp
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2
python run_server.py --rebuild-index --language zh --force

# 2. 打包向量数据库
tar -czf chroma-data.tar.gz data/chroma/

# 3. 推送到服务器
scp chroma-data.tar.gz user@server:/path/to/mcp/

# 4. 服务器解压
ssh user@server
cd /path/to/mcp
tar -xzf chroma-data.tar.gz

# 5. 服务器配置使用相同模型
# 编辑 .env
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2

# 6. 启动服务
python run_server.py
```

**注意事项：**
- ⚠️ 本地和服务器必须使用**相同**的模型
- ⚠️ 向量数据库较大（~10-100MB），传输需要时间
- ⚠️ 文档更新后需要重复此流程

---

#### 方案 B: 完全本地化部署

**适用场景：**
- 个人使用，不需要公开服务
- 本地机器配置高
- 对隐私要求高
- 不需要远程访问

**架构说明：**
```
本地开发机（高配置）
  └─ L12-v2 模型
      ├─ 生成文档向量
      ├─ 生成查询向量
      └─ 向量搜索
              ↓
         通过 MCP 返回结果
```

**优点：**
- ✅ 服务器零内存占用
- ✅ 使用最高精度模型
- ✅ 完全本地化，隐私安全
- ✅ 无网络延迟

**缺点：**
- ❌ 需要本地机器一直运行
- ❌ 第三方 AI 无法直接访问
- ❌ 不适合多用户场景

**实施步骤：**

```bash
# 1. 本地启动服务
cd mcp
python run_server.py

# 2. 配置 Claude Desktop 使用本地服务
# 编辑 model_config.json
{
  "mcpServers": {
    "beecount": {
      "command": "python",
      "args": ["run_server.py"],
      "cwd": "/path/to/mcp"
    }
  }
}
```

---

#### 方案 C: CI/CD 自动化部署（推荐）

**适用场景：**
- 文档频繁更新
- 团队协作
- 需要自动化流程
- 有 GitHub/GitLab CI/CD

**架构说明：**
```
Git 仓库
  ├─ 文档更新
  └─ 触发 CI/CD
          ↓
     CI/CD 服务器（高配置）
        └─ L12-v2 模型
            ├─ 生成向量数据库
            └─ 推送到生产服务器
                    ↓
               生产服务器（轻量）
                  └─ L12-v2 模型（仅查询）
```

**优点：**
- ✅ 完全自动化
- ✅ 使用高精度模型
- ✅ 文档更新自动触发重建
- ✅ 无需手动干预
- ✅ 支持团队协作

**缺点：**
- ❌ 需要配置 CI/CD
- ❌ 服务器仍需运行 L12-v2 模型
- ❌ 首次配置较复杂

**实施步骤：**

1. **创建 GitHub Actions 配置** `.github/workflows/deploy.yml`：

```yaml
name: Deploy MCP Server

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'i18n/**'

jobs:
  build-vector-index:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          cd mcp
          pip install -r requirements.txt
      
      - name: Build vector index
        env:
          EMBEDDING_MODEL: paraphrase-multilingual-MiniLM-L12-v2
        run: |
          cd mcp
          python run_server.py --rebuild-index --language zh --force
      
      - name: Package vector database
        run: |
          cd mcp
          tar -czf chroma-data.tar.gz data/chroma/
      
      - name: Upload to server
        uses: appleboy/scp-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_KEY }}
          source: "mcp/chroma-data.tar.gz"
          target: "/path/to/mcp/"
          strip_components: 1
      
      - name: Restart service
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /path/to/mcp
            tar -xzf chroma-data.tar.gz
            sudo systemctl restart mcp
```

2. **配置 GitHub Secrets**：

在 GitHub 仓库设置中添加以下 Secrets：
- `SERVER_HOST`: 服务器地址
- `SERVER_USER`: SSH 用户名
- `SSH_KEY`: SSH 私钥

3. **推送文档触发部署**：

```bash
# 修改文档后推送
git add docs/
git commit -m "Update documentation"
git push origin main

# 自动触发 CI/CD 流程
```

---

#### 方案 D: 混合部署（轻量服务器推荐）

**适用场景：**
- 轻量服务器（1-2GB 内存）
- 文档频繁更新
- 对搜索精度要求中等
- 需要自动化

**架构说明：**
```
日常更新：
  本地开发
    └─ 文档编辑
          ↓
        Git 推送
          ↓
    生产服务器（轻量）
      ├─ L6-v2 模型（轻量）
      ├─ Webhook 触发重建
      └─ 后台异步重建索引

重要更新：
  本地开发机（高配置）
    └─ L12-v2 模型
        ├─ 生成高精度向量
        └─ 推送到服务器
              ↓
        生产服务器（轻量）
          └─ L12-v2 模型（临时）
              └─ 重启服务
```

**优点：**
- ✅ 日常使用轻量模型（~800MB 内存）
- ✅ 重要更新使用高精度模型
- ✅ 文档更新自动触发重建
- ✅ 适合轻量服务器
- ✅ 灵活性高

**缺点：**
- ❌ 需要配置 Webhook
- ❌ 重要更新需要手动操作
- ❌ 模型切换需要重启服务

**实施步骤：**

1. **创建自动重建脚本** `scripts/auto_rebuild.sh`：

```bash
#!/bin/bash
# 文档更新后自动重建索引

echo "[$(date)] 检测到文档更新，开始重建向量索引..."

# 后台重建，不阻塞服务
nohup python run_server.py --rebuild-index --language zh > /tmp/rebuild.log 2>&1 &

echo "[$(date)] 向量索引正在后台重建，请稍后..."
echo "[$(date)] 查看进度: tail -f /tmp/rebuild.log"
```

2. **配置 Git post-receive hook**：

```bash
#!/bin/bash
# .git/hooks/post-receive

while read oldrev newrev refname
do
    # 检查是否是 docs 或 i18n 目录的更新
    if git diff --name-only $oldrev $newrev | grep -E "^(docs|i18n)/"; then
        echo "[$(date)] 检测到文档更新，触发索引重建..."
        /path/to/mcp/scripts/auto_rebuild.sh
    fi
done
```

3. **日常使用（轻量模型）**：

```bash
# 服务器 .env 配置
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L6-v2

# 启动服务
python run_server.py

# 文档更新后自动触发重建（后台）
```

4. **重要更新（高精度模型）**：

```bash
# 1. 本地生成高精度向量
cd mcp
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2
python run_server.py --rebuild-index --language zh --force

# 2. 推送到服务器
scp -r data/chroma user@server:/path/to/mcp/data/

# 3. 服务器切换模型并重启
ssh user@server
cd /path/to/mcp
# 编辑 .env
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2
# 重启服务
sudo systemctl restart mcp
```

---

#### 方案对比

| 方案 | 服务器内存 | 精度 | 自动化 | 推荐度 | 适用场景 |
|------|----------|------|--------|--------|----------|
| A: 本地生成，服务器查询 | ~1.5GB | ⭐⭐⭐⭐ | ❌ 手动 | ⭐⭐⭐ | 文档更新少，精度要求高 |
| B: 完全本地化 | 0 | ⭐⭐⭐⭐⭐ | ❌ | ⭐⭐ | 个人使用，隐私要求高 |
| C: CI/CD 自动化 | ~1.5GB | ⭐⭐⭐⭐ | ✅ 完全自动 | ⭐⭐⭐⭐⭐ | 团队协作，频繁更新 |
| D: 混合部署 | ~800MB | ⭐⭐⭐ | ✅ 半自动 | ⭐⭐⭐⭐ | 轻量服务器，灵活部署 |
| 标准部署 | ~800MB-1.5GB | ⭐⭐⭐ | ❌ | ⭐⭐⭐ | 通用场景 |

---

#### 方案选择指南

**根据服务器资源选择：**

| 服务器内存 | 推荐方案 | 理由 |
|-----------|----------|------|
| < 1GB | 方案 D（L6-v2） | 唯一可行选项 |
| 1-2GB | 方案 D（L6-v2） | 平衡性能和资源 |
| 2-4GB | 方案 C 或 D（L8-v2） | 更好的精度 |
| > 4GB | 方案 C（L12-v2） | 最高精度，完全自动化 |

**根据使用场景选择：**

| 场景 | 推荐方案 | 理由 |
|------|----------|------|
| 个人使用 | 方案 B | 完全本地化，隐私安全 |
| 小团队 | 方案 D | 灵活部署，资源优化 |
| 大团队 | 方案 C | 完全自动化，协作友好 |
| 文档频繁更新 | 方案 C 或 D | 自动化重建 |
| 文档偶尔更新 | 方案 A | 手动操作可接受 |
| 对精度要求高 | 方案 A 或 C | 使用高精度模型 |

**重要提醒：**

⚠️ **所有方案都必须使用相同的模型生成文档向量和查询向量**

❌ **不可行的方案：**
- 本地用 L12-v2 生成文档向量
- 服务器用 L6-v2 生成查询向量
- 原因：不同模型的向量空间不兼容，无法计算相似度

✅ **可行的方案：**
- 本地和服务器使用相同模型
- 或完全本地化（方案 B）
- 或使用 CI/CD 统一模型（方案 C）

---

## 配置说明

### 环境变量详解

#### 基础配置

```bash
# 服务器名称
SERVER_NAME=BeeCount MCP Server

# 服务器版本
SERVER_VERSION=1.0.0

# 日志级别: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# 网站URL（用于生成在线查看链接）
WEBSITE_URL=https://beecount.youths.cc
```

#### 向量搜索配置

```bash
# 嵌入模型选择
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L6-v2

# 向量数据库路径
VECTOR_DB_PATH=./data/chroma

# 文档分块大小（字符数）
CHUNK_SIZE=800

# 文档分块重叠（字符数）
CHUNK_OVERLAP=150

# 最小相似度分数（0-1）
MIN_SIMILARITY_SCORE=0.5
```

### 模型选择指南

#### 根据服务器内存选择

| 内存 | 推荐模型 | 理由 |
|------|----------|------|
| < 1GB | L6-v2 | 唯一可行选项 |
| 1-2GB | L6-v2 | 平衡性能和资源 |
| 2-4GB | L8-v2 | 更好的精度 |
| > 4GB | L12-v2 或 mpnet-base-v2 | 最高精度 |

#### 根据使用场景选择

| 场景 | 推荐模型 | 理由 |
|------|----------|------|
| 开发测试 | L6-v2 | 快速启动，节省资源 |
| 生产环境（轻量） | L6-v2 | 稳定可靠 |
| 生产环境（标准） | L8-v2 | 精度和资源平衡 |
| 生产环境（高性能） | L12-v2 | 最高精度 |

## 生产环境部署

### Linux/Mac (systemd)

#### 1. 创建服务配置文件

```bash
sudo cp mcp.service.example /etc/systemd/system/mcp.service
```

#### 2. 编辑服务配置

```bash
sudo nano /etc/systemd/system/mcp.service
```

修改以下内容：
```ini
[Unit]
Description=BeeCount MCP Server
After=network.target

[Service]
Type=simple
User=your_username              # 修改为你的用户名
WorkingDirectory=/path/to/mcp    # 修改为实际路径
Environment="PATH=/path/to/mcp/mcp_env/bin"
ExecStart=/path/to/mcp/mcp_env/bin/python /path/to/mcp/run_server.py
Restart=always
RestartSec=10

# 日志
StandardOutput=journal
StandardError=journal
SyslogIdentifier=beecount-mcp

# 资源限制（根据服务器配置调整）
MemoryLimit=2G
CPUQuota=200%

[Install]
WantedBy=multi-user.target
```

#### 3. 启动服务

```bash
# 重新加载 systemd
sudo systemctl daemon-reload

# 启用开机自启
sudo systemctl enable mcp

# 启动服务
sudo systemctl start mcp

# 查看状态
sudo systemctl status mcp

# 查看日志
sudo journalctl -u mcp -f
```

#### 4. 服务管理命令

```bash
# 启动服务
sudo systemctl start mcp

# 停止服务
sudo systemctl stop mcp

# 重启服务
sudo systemctl restart mcp

# 查看状态
sudo systemctl status mcp

# 查看日志
sudo journalctl -u mcp -n 100
```

### Windows (NSSM)

#### 1. 下载 NSSM

访问 https://nssm.cc/download 下载最新版本。

#### 2. 安装服务

```powershell
# 进入 NSSM 目录
cd nssm

# 安装服务
nssm install BeeCountMCP python

# 配置服务
nssm set BeeCountMCP AppDirectory D:\Work\code\BeeCount-Website\mcp
nssm set BeeCountMCP AppParameters run_server.py
nssm set BeeCountMCP AppEnvironmentExtra PATH=%PATH%;D:\Work\code\BeeCount-Website\mcp\mcp_env\Scripts

# 配置日志
nssm set BeeCountMCP AppStdout D:\Work\code\BeeCount-Website\mcp\mcp.log
nssm set BeeCountMCP AppStderr D:\Work\code\BeeCount-Website\mcp\mcp.log

# 启动服务
nssm start BeeCountMCP
```

#### 3. 服务管理

```powershell
# 启动服务
nssm start BeeCountMCP

# 停止服务
nssm stop BeeCountMCP

# 重启服务
nssm restart BeeCountMCP

# 查看状态
nssm status BeeCountMCP

# 编辑配置
nssm edit BeeCountMCP

# 删除服务
nssm remove BeeCountMCP
```

## 常见问题

### Q1: 部署脚本执行失败

**问题：** 运行 `./deploy.sh` 或 `.\deploy.ps1` 时报错

**解决方案：**

Linux/Mac:
```bash
# 检查执行权限
ls -l deploy.sh

# 赋予执行权限
chmod +x deploy.sh

# 再次运行
./deploy.sh
```

Windows:
```powershell
# 检查 PowerShell 执行策略
Get-ExecutionPolicy

# 临时允许脚本执行
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 再次运行
.\deploy.ps1
```

### Q2: 模型下载失败

**问题：** 首次运行时模型下载失败

**解决方案：**

```bash
# 方法 1: 使用镜像
export HF_ENDPOINT=https://hf-mirror.com
python run_server.py --rebuild-index

# 方法 2: 手动下载模型
pip install huggingface-hub
huggingface-cli download sentence-transformers/paraphrase-multilingual-MiniLM-L6-v2 --local-dir ~/.cache/huggingface/hub/

# 方法 3: 使用代理
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
python run_server.py --rebuild-index
```

### Q3: 内存不足

**问题：** 服务器内存不足，服务崩溃

**解决方案：**

```bash
# 1. 使用更小的模型
# 编辑 .env
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L6-v2

# 2. 调整分块大小
# 编辑 .env
CHUNK_SIZE=1500  # 增大分块，减少向量数量

# 3. 重新生成索引
python run_server.py --rebuild-index --language zh --force
```

### Q4: 向量搜索返回空结果

**问题：** 调用 semantic_search 返回空结果

**解决方案：**

```bash
# 1. 检查索引是否生成
python -c "from src.vector_store import get_vector_store; print(get_vector_store().get_stats('zh'))"

# 2. 重新生成索引
python run_server.py --rebuild-index --language zh

# 3. 降低相似度阈值
# 编辑 .env
MIN_SIMILARITY_SCORE=0.3

# 4. 检查查询语言
# 确保查询语言与文档语言匹配
```

### Q5: 服务无法启动

**问题：** 运行 `python run_server.py` 时报错

**解决方案：**

```bash
# 1. 检查 Python 版本
python --version  # 需要 3.8+

# 2. 检查依赖安装
pip list | grep -E "fastmcp|chromadb|sentence-transformers"

# 3. 重新安装依赖
pip install -r requirements.txt --force-reinstall

# 4. 查看详细错误
python run_server.py --log-level DEBUG
```

### Q6: 如何更新文档后重新索引

**问题：** 文档更新后搜索结果不包含新内容

**解决方案：**

```bash
# 方法 1: 重建中文索引
python run_server.py --rebuild-index --language zh

# 方法 2: 重建英文索引
python run_server.py --rebuild-index --language en

# 方法 3: 重建所有语言索引（推荐）
python run_server.py --rebuild-index --language ALL

# 方法 4: 强制重建（如果增量更新失败）
python run_server.py --rebuild-index --language ALL --force
```

### Q7: 如何监控服务状态

**问题：** 需要监控服务运行状态

**解决方案：**

Linux/Mac:
```bash
# 查看服务状态
sudo systemctl status mcp

# 实时查看日志
sudo journalctl -u mcp -f

# 查看最近错误
sudo journalctl -u mcp -p err -n 50
```

Windows:
```powershell
# 查看服务状态
nssm status BeeCountMCP

# 查看日志文件
Get-Content mcp.log -Tail 50 -Wait
```

### Q8: 如何备份数据

**问题：** 需要备份向量数据库

**解决方案：**

```bash
# 备份向量数据库
tar -czf chroma-backup-$(date +%Y%m%d).tar.gz data/chroma/

# 恢复向量数据库
tar -xzf chroma-backup-20250108.tar.gz

# 定期备份（cron）
# 添加到 crontab
0 2 * * * cd /path/to/mcp && tar -czf /backup/chroma-$(date +\%Y\%m\%d).tar.gz data/chroma/
```

## 性能优化

### 1. 减少内存占用

```bash
# 使用更小的模型
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L6-v2

# 增大分块大小
CHUNK_SIZE=1500
CHUNK_OVERLAP=200

# 减少返回结果数
# 在调用时设置 top_k=3
```

### 2. 提高搜索速度

```bash
# 提高相似度阈值
MIN_SIMILARITY_SCORE=0.6

# 减少返回结果数
top_k=3

# 使用更快的模型
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L6-v2
```

### 3. 优化日志

```bash
# 生产环境使用 INFO 级别
LOG_LEVEL=INFO

# 避免使用 DEBUG 级别
# DEBUG 会产生大量日志
```

## 安全建议

### 1. 环境变量保护

```bash
# 确保 .env 文件不被提交到 Git
echo ".env" >> .gitignore

# 设置文件权限
chmod 600 .env
```

### 2. 服务运行权限

```bash
# 使用非 root 用户运行
# 在 systemd 配置中设置
User=mcp_user

# 限制资源使用
MemoryLimit=2G
CPUQuota=200%
```

### 3. 日志管理

```bash
# 配置日志轮转
# 在 systemd 配置中添加
LogRateLimitIntervalSec=1s
LogRateLimitBurst=1000

# 定期清理旧日志
find /var/log/journal -name "*.journal" -mtime +30 -delete
```

## 支持

如遇到问题，请：

1. 查看日志文件 `mcp.log`
2. 检查系统资源使用情况
3. 参考本文档的常见问题部分
4. 提交 Issue 到项目仓库

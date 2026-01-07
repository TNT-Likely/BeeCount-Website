# BeeCount MCP Server

BeeCount MCP服务器是一个基于Model Context Protocol (MCP) 的文档访问服务，专注于提供BeeCount网站的使用说明文档。

## 功能特性

### 基础功能
- 文档查询和检索（支持中文和英文文档）
- 文件列表和浏览（docs和i18n目录）
- 文件内容读取（支持行范围选择）
- 媒体文件列表（图片和视频）
- 项目信息获取
- 在线查看链接（自动生成网站URL）
- 完整的日志记录
- 错误处理和异常管理

### 智能语义搜索（升级版）
- 基于向量嵌入的语义搜索
- 支持自然语言查询
- 跨语言文档检索（中英文混合）
- 相似度排序和过滤
- 文档分块和索引管理
- 增量索引更新
- 向量存储统计信息
- 高性能搜索（毫秒级响应）

### 为什么需要模型？

**MCP 服务端必须运行嵌入模型**，原因如下：

1. **语义搜索的核心原理**
   ```
   用户查询: "如何创建预算？"
       ↓
   模型转换: [0.1, 0.2, 0.3, ...]  ← 需要模型！
       ↓
   向量搜索: 在 ChromaDB 中查找相似向量
       ↓
   返回结果: 找到 3 个相关文档片段
   ```

2. **第三方 AI（Claude/GPT）的角色**
   - ❌ **不需要模型** - 只负责调用 MCP 工具
   - ✅ 发送自然语言查询："如何创建预算？"
   - ✅ 接收搜索结果并生成回答

3. **MCP 服务端的角色**
   - ✅ **必须需要模型** - 将查询转换为向量
   - ✅ 在向量数据库中搜索相似内容
   - ✅ 返回排序后的结果

**关键理解：**
```
第三方 AI = 客户端（调用者）
MCP 服务端 = 服务提供者（需要模型）
```

就像使用 Google 搜索：
- 你（第三方 AI）只需要发送查询
- Google（MCP 服务端）有搜索引擎和索引

### 为什么需要重新生成向量数据库？

**向量数据库必须重新生成的情况：**

1. **首次部署**
   - 服务器上没有向量数据
   - 必须运行 `python run_server.py --rebuild-index`

2. **文档更新**
   - 添加新的 markdown 文档
   - 修改现有文档内容
   - 删除文档后需要清理索引

3. **更换模型**
   - 从 L12 模型切换到 L6 模型
   - 不同模型的向量维度不同，必须重新生成

**如何重新生成向量数据库：**

⚠️ **重要提示：重建向量索引是高危操作，只能通过命令行执行，不能通过 MCP 工具调用。**

```bash
# 方法 1: 重建中文索引
python run_server.py --rebuild-index --language zh

# 方法 2: 重建英文索引
python run_server.py --rebuild-index --language en

# 方法 3: 重建所有语言索引（推荐）
python run_server.py --rebuild-index --language ALL

# 方法 4: 强制重建（删除现有数据后重新生成）
python run_server.py --rebuild-index --language ALL --force
```

**为什么不能通过 MCP 工具重建？**

1. **安全考虑** - 重建索引会删除现有数据，误操作可能导致服务中断
2. **性能影响** - 重建过程需要大量 CPU 和内存，可能影响正常服务
3. **权限控制** - 索引管理应该由服务器管理员控制，而不是外部 AI 或用户
4. **操作审计** - 命令行操作更容易记录和追踪

**增量更新 vs 强制重建：**

| 操作 | 说明 | 适用场景 |
|------|------|----------|
| 增量更新 | 只处理新增/修改的文档 | 日常文档更新 |
| 强制重建 | 删除所有数据，重新生成 | 首次部署、更换模型、数据损坏 |

## 项目结构

```
mcp/
├── src/
│   ├── __init__.py
│   ├── main.py              # MCP服务入口
│   ├── config.py            # 配置管理
│   ├── utils.py             # 工具函数
│   ├── embeddings.py        # 文本向量化
│   └── vector_store.py      # 向量存储管理
├── tests/
│   ├── __init__.py
│   ├── test_basic.py        # 基础测试
│   └── test_vector.py       # 向量搜索测试
├── scripts/                # 部署和自动化脚本
│   ├── README.md           # 脚本使用说明
│   ├── build_vector_local.sh  # 本地生成高精度向量
│   ├── sync_to_server.sh    # 同步向量数据库到服务器
│   └── auto_rebuild.sh     # 自动重建向量索引
├── data/                   # 向量数据存储
│   └── .gitkeep
├── .env.example             # 环境变量示例
├── model_config.json        # MCP服务器配置（用于Claude Desktop）
├── requirements.txt         # 依赖列表
├── README.md                # 说明文档
├── DEPLOYMENT.md           # 详细部署指南
├── run_server.py            # 启动脚本
├── deploy.sh               # Linux/Mac 部署脚本
├── deploy.ps1              # Windows 部署脚本
└── mcp.service.example     # systemd 服务配置示例
```

## 安装

### 1. 创建虚拟环境

```bash
python -m venv mcp_env
source mcp_env/bin/activate  # Linux/Mac
# 或
mcp_env\Scripts\activate     # Windows
```

### 2. 安装依赖

```bash
cd mcp
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并根据需要修改配置：

```bash
cp .env.example .env
```

## 使用

### 部署到服务器

#### 自动部署（推荐）

使用部署脚本自动完成所有配置：

**Linux/Mac:**
```bash
cd mcp
chmod +x deploy.sh
./deploy.sh
```

**Windows:**
```powershell
cd mcp
.\deploy.ps1
```

部署脚本会自动完成以下步骤：
1. 检查 Python 版本和系统资源
2. 选择合适的嵌入模型（推荐轻量模型）
3. 创建虚拟环境并安装依赖
4. 配置环境变量
5. 生成向量索引
6. 运行测试验证

**部署脚本选项：**
- 选项 1: L12-v2 (420MB, 高精度)
- 选项 2: L6-v2 (200MB, 轻量服务器推荐)
- 选项 3: L8-v2 (300MB, 中等精度)

#### 手动部署

如果需要手动部署，请参考以下步骤：

### 配置 MCP 服务器

#### 方法一：使用 model_config.json（推荐）

1. 将 `model_config.json` 复制到 Claude 配置目录：
   - **Windows**: `%APPDATA%\Claude\`
   - **macOS**: `~/Library/Application Support/Claude/`
   - **Linux**: `~/.config/Claude/`

2. 修改 `model_config.json` 中的 `cwd` 为你的实际项目路径：
   ```json
   {
     "mcpServers": {
       "beecount": {
         "command": "python",
         "args": [
           "run_server.py"
         ],
         "cwd": "/path/to/your/project/mcp"
       }
     }
   }
   ```

3. 重启 Claude Desktop 应用

#### 方法二：使用 MCP Inspector

1. 安装MCP Inspector：
```bash
npm install -g @modelcontextprotocol/inspector
```

2. 启动服务器并连接到Inspector：
```bash
mcp-inspector python run_server.py
```

3. 在Inspector中测试各个工具的功能

### 启动MCP服务器

#### 前台运行（开发调试）
```bash
python run_server.py
```

#### 后台运行（生产环境）

**Linux/Mac:**
```bash
# 使用 nohup
nohup python run_server.py > mcp.log 2>&1 &

# 使用 systemd（推荐）
sudo cp mcp.service.example /etc/systemd/system/mcp.service
# 编辑 mcp.service，修改 User, WorkingDirectory, ExecStart 路径
sudo systemctl daemon-reload
sudo systemctl enable mcp
sudo systemctl start mcp

# 查看日志
sudo journalctl -u mcp -f
```

**Windows:**
```powershell
# PowerShell 后台运行
Start-Process python -ArgumentList 'run_server.py' -WindowStyle Hidden

# CMD 后台运行
start /B python run_server.py > mcp.log 2>&1

# 使用 NSSM 安装为 Windows 服务（推荐）
# 1. 下载 NSSM: https://nssm.cc/download
# 2. 安装服务
nssm install BeeCountMCP python
nssm set BeeCountMCP AppDirectory (Get-Location)
nssm set BeeCountMCP AppParameters run_server.py
nssm set BeeCountMCP AppEnvironmentExtra PATH=%PATH%;(Get-Location)\mcp_env\Scripts
nssm start BeeCountMCP
```

#### 查看日志
```bash
# 查看实时日志
tail -f mcp.log

# 查看最近 100 行
tail -n 100 mcp.log
```

### MCP工具

服务器提供以下MCP工具：

#### 1. query_document
在项目文档中搜索内容。

**参数：**
- `query` (str): 搜索查询字符串
- `max_results` (int): 返回的最大结果数（默认：5）
- `language` (str): 语言选择，"zh"表示中文文档，"en"表示英文文档（默认："zh"）

**示例：**
```python
query_document("预算", max_results=10, language="zh")
query_document("budget", max_results=10, language="en")
```

#### 2. list_files
列出指定目录中的md文档文件。

**参数：**
- `directory` (str): 目录路径（相对于docs或i18n根目录，默认："."）
- `language` (str): 语言选择，"zh"表示中文文档，"en"表示英文文档（默认："zh"）

**示例：**
```python
list_files("getting-started", language="zh")
list_files("getting-started", language="en")
```

#### 3. read_file
读取文件内容。

**参数：**
- `file_path` (str): 文件路径（相对于docs或i18n根目录）
- `line_range` (str): 行范围，支持以下格式：
  - "0~100": 读取第1-100行（默认）
  - "101~200": 读取第101-200行
  - "all": 读取整个文件
  - "50": 读取前50行（等同于"0~50"）
- `language` (str): 语言选择，"zh"表示中文文档，"en"表示英文文档（默认："zh"）

**示例：**
```python
read_file("getting-started/installation.md", line_range="0~50", language="zh")
read_file("getting-started/installation.md", line_range="101~200", language="en")
read_file("changelog.md", line_range="all", language="zh")
```

#### 4. list_media_files
列出指定目录中的媒体文件（图片/视频）并获取基本信息。

**参数：**
- `directory` (str): 目录路径（相对于static目录，默认："."）
- `media_type` (str): 媒体类型，"image"表示图片文件，"video"表示视频文件，"all"表示所有媒体文件（默认："image"）
- `language` (str): 语言选择，"zh"表示中文文档，"en"表示英文文档（默认："zh"）

**示例：**
```python
list_media_files("img/preview/zh", media_type="image", language="zh")
list_media_files("img", media_type="video", language="zh")
list_media_files("img", media_type="all", language="zh")
```

#### 5. get_project_info
获取项目基本信息（包含向量搜索统计）。

**参数：**
无

**示例：**
```python
get_project_info()
```

#### 6. semantic_search
基于语义相似度搜索文档（智能搜索）。

**参数：**
- `query` (str): 搜索查询字符串（支持自然语言）
- `top_k` (int): 返回的最大结果数（默认：5）
- `language` (str): 语言选择，"zh"表示中文文档，"en"表示英文文档（默认："zh"）
- `min_score` (float): 最小相似度分数（0-1之间），低于此分数的结果将被过滤（默认：0.5）

**示例：**
```python
semantic_search("如何创建预算", top_k=5, language="zh")
semantic_search("how to create budget", top_k=5, language="en")
```

#### 7. rebuild_vector_index
重建向量索引（用于文档更新后重新索引）。

**参数：**
- `language` (str): 语言选择，"zh"表示中文文档，"en"表示英文文档（默认："zh"）
- `force` (bool): 是否强制重建（删除现有索引后重新创建）（默认：False）

**示例：**
```python
rebuild_vector_index(language="zh", force=False)
rebuild_vector_index(language="en", force=True)  # 强制重建
```

#### 8. get_vector_stats
获取向量存储统计信息。

**参数：**
- `language` (str): 语言选择，"zh"表示中文文档，"en"表示英文文档（默认："zh"）

**示例：**
```python
get_vector_stats(language="zh")
get_vector_stats(language="en")
```

## 测试

### 运行基础测试
```bash
python tests/test_basic.py
```

### 运行向量搜索测试
```bash
python tests/test_vector.py
```

## 配置说明

### 环境变量

在 `.env` 文件中可以配置以下变量：

**基础配置：**
- `SERVER_NAME`: 服务器名称（默认：BeeCount MCP Server）
- `SERVER_VERSION`: 服务器版本（默认：1.0.0）
- `LOG_LEVEL`: 日志级别（默认：INFO）
- `WEBSITE_URL`: 网站URL（默认：https://beecount.youths.cc）

**向量搜索配置：**
- `EMBEDDING_MODEL`: 嵌入模型名称（默认：paraphrase-multilingual-MiniLM-L12-v2）
- `VECTOR_DB_PATH`: 向量数据库路径（默认：./data/chroma）
- `CHUNK_SIZE`: 文档分块大小（默认：800）
- `CHUNK_OVERLAP`: 文档分块重叠大小（默认：150）
- `MIN_SIMILARITY_SCORE`: 最小相似度分数（默认：0.5）

### 嵌入模型选择

**支持的中文模型（按推荐度排序）：**

| 模型名称 | 大小 | 内存占用 | 精度 | 适用场景 |
|---------|------|---------|-------|----------|
| `paraphrase-multilingual-MiniLM-L12-v2` | 420MB | ~1.5GB | ⭐⭐⭐⭐⭐ | 高精度要求，充足内存 |
| `paraphrase-multilingual-MiniLM-L8-v2` | 300MB | ~1.2GB | ⭐⭐⭐⭐ | 平衡性能和内存 |
| `paraphrase-multilingual-MiniLM-L6-v2` | 200MB | ~800MB | ⭐⭐⭐ | 轻量服务器（推荐） |
| `paraphrase-multilingual-mpnet-base-v2` | 420MB | ~1.5GB | ⭐⭐⭐⭐⭐ | 最高精度，充足内存 |

**模型对比：**

1. **L12-v2 (420MB)**
   - ✅ 最高精度
   - ✅ 支持 50+ 语言
   - ❌ 内存占用大
   - 适用：生产环境，内存充足

2. **L8-v2 (300MB)**
   - ✅ 精度和内存平衡
   - ✅ 支持 50+ 语言
   - 适用：中等配置服务器

3. **L6-v2 (200MB) - 轻量服务器推荐**
   - ✅ 内存占用小
   - ✅ 启动快
   - ✅ 支持 50+ 语言
   - ❌ 精度略低（通常可接受）
   - 适用：轻量服务器（1-2GB 内存）

4. **mpnet-base-v2 (420MB)**
   - ✅ 最高精度
   - ✅ 支持 50+ 语言
   - ❌ 内存占用最大
   - 适用：对精度要求极高的场景

**如何选择模型：**

```bash
# 方法 1: 修改 .env 文件
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L6-v2

# 方法 2: 使用部署脚本（推荐）
# Linux/Mac
./deploy.sh
# 选择选项 2（轻量模型）

# Windows
.\deploy.ps1
# 选择选项 2（轻量模型）
```

**服务器配置建议：**

| 服务器内存 | 推荐模型 | 预计内存占用 |
|-----------|----------|-------------|
| < 1GB | L6-v2 | ~800MB |
| 1-2GB | L6-v2 | ~800MB |
| 2-4GB | L8-v2 | ~1.2GB |
| > 4GB | L12-v2 或 mpnet-base-v2 | ~1.5GB |

**模型切换：**

```bash
# 1. 修改 .env 文件中的 EMBEDDING_MODEL
# 2. 强制重建向量索引
python run_server.py --rebuild-index --language zh --force
```

### 日志级别

支持的日志级别：
- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

## 开发

### 代码规范

- 遵循PEP 8规范
- 使用类型注解
- 编写文档字符串
- 严格错误处理
- 日志记录

### 添加新工具

在 `src/main.py` 中添加新的MCP工具：

```python
@mcp.tool()
def new_tool(param: str) -> str:
    """
    工具描述
    
    Args:
        param: 参数说明
    
    Returns:
        返回值说明
    """
    try:
        # 实现逻辑
        return result
    except Exception as e:
        logger.error(f"Error in new_tool: {e}")
        return f"Error: {str(e)}"
```

## 依赖说明

**核心依赖：**
- `fastmcp==2.14.2`: MCP服务器框架（固定版本）
- `python-dotenv`: 环境变量管理
- `pydantic`: 数据验证
- `mcp`: MCP协议核心库

**向量搜索依赖：**
- `chromadb>=0.4.0`: 向量数据库
- `sentence-transformers>=2.2.0`: 嵌入模型（支持多语言）
- `numpy>=1.24.0`: 数值计算库

## 故障排除

### 问题：无法启动服务器

**解决方案：**
1. 检查Python版本（需要Python 3.13.11）
2. 确认所有依赖已正确安装
3. 检查环境变量配置

### 问题：工具调用失败

**解决方案：**
1. 查看服务器日志输出
2. 检查文件路径是否正确
3. 确认文件权限

### 问题：向量搜索返回空结果

**解决方案：**
1. 确认向量索引已构建（使用rebuild_vector_index工具）
2. 检查查询语言是否与文档语言匹配
3. 尝试降低min_score参数值
4. 查看日志中的相似度分数

### 问题：嵌入模型加载失败

**解决方案：**
1. 检查网络连接（首次加载需要下载模型）
2. 确认有足够的磁盘空间（模型约420MB）
3. 查看日志中的错误信息

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

# BeeCount MCP Server

BeeCount MCP服务器是一个基于Model Context Protocol (MCP) 的文档访问服务，专注于提供BeeCount网站的使用说明文档。

## 功能特性

- 文档查询和检索（支持中文和英文文档）
- 文件列表和浏览（docs和i18n目录）
- 文件内容读取（支持行范围选择）
- 媒体文件列表（图片和视频）
- 项目信息获取
- 在线查看链接（自动生成网站URL）
- 完整的日志记录
- 错误处理和异常管理

## 项目结构

```
mcp/
├── src/
│   ├── __init__.py
│   ├── main.py              # MCP服务入口
│   ├── config.py            # 配置管理
│   └── utils.py             # 工具函数
├── tests/
│   ├── __init__.py
│   └── test_basic.py        # 基础测试
├── .env.example             # 环境变量示例
├── model_config.json        # MCP服务器配置（用于Claude Desktop）
├── requirements.txt         # 依赖列表
├── README.md                # 说明文档
└── run_server.py            # 启动脚本
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

```bash
python run_server.py
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
获取项目基本信息。

**参数：**
无

**示例：**
```python
get_project_info()
```

## 测试

### 运行基础测试

```bash
python tests/test_basic.py
```

## 配置说明

### 环境变量

在 `.env` 文件中可以配置以下变量：

- `SERVER_NAME`: 服务器名称（默认：BeeCount MCP Server）
- `SERVER_VERSION`: 服务器版本（默认：1.0.0）
- `LOG_LEVEL`: 日志级别（默认：INFO）
- `WEBSITE_URL`: 网站URL（默认：https://beecount.youths.cc）

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

- `fastmcp==2.14.2`: MCP服务器框架（固定版本）
- `python-dotenv`: 环境变量管理
- `pydantic`: 数据验证
- `mcp`: MCP协议核心库

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

## 后续计划

### 阶段二：智能语义搜索

- 集成ChromaDB向量数据库
- 实现文档向量化
- 添加语义搜索功能
- 支持相似度查询

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

# MCP 部署脚本使用说明

本目录包含用于高级部署方案的自动化脚本。

## 脚本列表

### 1. build_vector_local.sh

**用途：** 在本地使用高精度模型生成向量数据库

**使用场景：**
- 本地机器配置高（内存充足）
- 服务器资源有限（轻量服务器）
- 对搜索精度要求高

**使用方法：**

```bash
# 基本使用（默认中文）
./scripts/build_vector_local.sh

# 指定语言
./scripts/build_vector_local.sh en

# 使用自定义模型
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2 ./scripts/build_vector_local.sh
```

**脚本功能：**
- ✅ 备份现有向量数据库
- ✅ 使用 L12-v2 高精度模型生成向量
- ✅ 显示向量数据库统计信息
- ✅ 打包向量数据库
- ✅ 可选推送到服务器
- ✅ 保存服务器配置（.sync_config）

**输出文件：**
- `chroma-data-zh.tar.gz` - 中文向量数据库
- `chroma-data-en.tar.gz` - 英文向量数据库
- `chroma-backup-YYYYMMDD-HHMMSS.tar.gz` - 备份文件

---

### 2. sync_to_server.sh

**用途：** 将本地生成的向量数据库推送到服务器

**使用场景：**
- 已在本地生成向量数据库
- 需要同步到服务器
- 频繁更新，需要快速同步

**使用方法：**

```bash
# 首次使用（交互式输入服务器信息）
./scripts/sync_to_server.sh

# 后续使用（从配置文件读取）
./scripts/sync_to_server.sh

# 指定语言
./scripts/sync_to_server.sh en
```

**配置文件：**
首次运行后会创建 `.sync_config` 文件，包含：
```bash
SERVER_HOST="your-server.com"
SERVER_USER="username"
SERVER_PATH="/path/to/mcp"
```

**脚本功能：**
- ✅ 检查向量数据库是否存在
- ✅ 打包向量数据库
- ✅ 推送到服务器
- ✅ 提供下一步操作指引
- ✅ 保存服务器配置

**输出文件：**
- `chroma-data-zh.tar.gz` - 打包的向量数据库
- `.sync_config` - 服务器配置（首次运行）

---

### 3. auto_rebuild.sh

**用途：** 文档更新后自动触发向量索引重建

**使用场景：**
- 文档频繁更新
- 需要自动化流程
- 轻量服务器使用轻量模型

**使用方法：**

```bash
# 基本使用（默认中文）
./scripts/auto_rebuild.sh

# 指定语言
./scripts/auto_rebuild.sh en
```

**脚本功能：**
- ✅ 后台重建向量索引（不阻塞服务）
- ✅ 记录详细日志
- ✅ 监控重建进度
- ✅ 重建完成后提示重启服务
- ✅ 自动清理旧日志（7天）

**日志文件：**
- `/tmp/mcp_rebuild_YYYYMMDD_HHMMSS.log` - 重建日志
- 自动清理：保留最近7天的日志

**监控进度：**

```bash
# 查看实时日志
tail -f /tmp/mcp_rebuild_*.log

# 查看最近的重建日志
ls -lt /tmp/mcp_rebuild_*.log | head -1
```

---

## 部署流程示例

### 方案 A: 本地生成 + 服务器查询

```bash
# 1. 本地生成高精度向量数据库
cd mcp
./scripts/build_vector_local.sh

# 2. 推送到服务器
./scripts/sync_to_server.sh

# 3. 服务器解压并重启
ssh user@server
cd /path/to/mcp
tar -xzf chroma-data-zh.tar.gz
sudo systemctl restart mcp
```

### 方案 D: 混合部署

#### 日常使用（轻量模型）

```bash
# 1. 服务器配置使用 L6-v2 轻量模型
# 编辑服务器 .env
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L6-v2

# 2. 启动服务
python run_server.py

# 3. 文档更新后自动触发重建
# Git push 后自动触发（需要配置 Git hook）
./scripts/auto_rebuild.sh
```

#### 重要更新（高精度模型）

```bash
# 1. 本地生成高精度向量
cd mcp
./scripts/build_vector_local.sh

# 2. 推送到服务器
./scripts/sync_to_server.sh

# 3. 服务器切换到高精度模型
ssh user@server
cd /path/to/mcp
# 编辑 .env
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2
sudo systemctl restart mcp
```

### 方案 C: CI/CD 自动化

```bash
# 1. 配置 GitHub Secrets
# 在 GitHub 仓库设置中添加：
# - SERVER_HOST
# - SERVER_USER
# - SSH_KEY
# - SERVER_PATH

# 2. 推送文档触发部署
git add docs/
git commit -m "Update documentation"
git push origin main

# 3. GitHub Actions 自动执行：
# - 生成向量数据库（L12-v2）
# - 推送到服务器
# - 重启服务
# - 验证部署
```

---

## Git Hook 配置

### 自动触发重建

在服务器的 Git 仓库中配置 post-receive hook：

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

**安装 hook：**

```bash
# 在服务器 Git 仓库中
cd /path/to/git-repo/.git/hooks
cp /path/to/mcp/scripts/auto_rebuild.sh post-receive
chmod +x post-receive
```

---

## 故障排除

### 问题 1: 脚本执行权限错误

**错误：** `bash: ./scripts/build_vector_local.sh: Permission denied`

**解决方案：**

```bash
# 赋予执行权限
chmod +x scripts/*.sh
```

### 问题 2: 向量数据库不存在

**错误：** `错误: 向量数据库不存在`

**解决方案：**

```bash
# 先生成向量数据库
./scripts/build_vector_local.sh
```

### 问题 3: SSH 连接失败

**错误：** `ssh: connect to host ... port 22: Connection refused`

**解决方案：**

```bash
# 1. 检查服务器地址
ping your-server.com

# 2. 检查 SSH 服务
ssh user@your-server.com

# 3. 检查防火墙
# 确保端口 22 开放

# 4. 使用 SSH 密钥
# 确保已配置 SSH 密钥认证
```

### 问题 4: 重建进程卡住

**错误：** 重建进程长时间无响应

**解决方案：**

```bash
# 1. 查看重建日志
tail -f /tmp/mcp_rebuild_*.log

# 2. 检查进程状态
ps aux | grep python

# 3. 手动终止进程
pkill -f "python.*run_server.py"

# 4. 重新运行
./scripts/auto_rebuild.sh
```

### 问题 5: 磁盘空间不足

**错误：** `No space left on device`

**解决方案：**

```bash
# 1. 检查磁盘空间
df -h

# 2. 清理旧备份
find . -name "chroma-backup-*.tar.gz" -mtime +30 -delete

# 3. 清理向量数据库
rm -rf data/chroma/

# 4. 重新生成
./scripts/build_vector_local.sh
```

---

## 性能优化

### 加快向量生成速度

```bash
# 1. 使用更快的模型
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L6-v2 ./scripts/build_vector_local.sh

# 2. 增大分块大小
# 编辑 .env
CHUNK_SIZE=1500
CHUNK_OVERLAP=200

# 3. 减少文档数量
# 只索引必要的文档
```

### 减少内存占用

```bash
# 1. 使用轻量模型
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L6-v2

# 2. 调整分块大小
CHUNK_SIZE=1500

# 3. 限制并发
# 在 .env 中添加
export OMP_NUM_THREADS=2
```

---

## 监控和日志

### 查看重建进度

```bash
# 实时查看日志
tail -f /tmp/mcp_rebuild_*.log

# 查看最近的重建
ls -lt /tmp/mcp_rebuild_*.log | head -1

# 查看错误
grep -i error /tmp/mcp_rebuild_*.log
```

### 查看向量数据库统计

```bash
# 中文统计
python -c "
from src.vector_store import get_vector_store
stats = get_vector_store().get_stats('zh')
print(f'Total chunks: {stats[\"total_chunks\"]}')
print(f'Total documents: {stats[\"total_documents\"]}')
print(f'Collection: {stats[\"collection_name\"]}')
"

# 英文统计
python -c "
from src.vector_store import get_vector_store
stats = get_vector_store().get_stats('en')
print(f'Total chunks: {stats[\"total_chunks\"]}')
print(f'Total documents: {stats[\"total_documents\"]}')
print(f'Collection: {stats[\"collection_name\"]}')
"
```

---

## 最佳实践

### 1. 定期备份

```bash
# 添加到 crontab
0 2 * * * cd /path/to/mcp && tar -czf /backup/chroma-$(date +\%Y\%m\%d).tar.gz data/chroma/
```

### 2. 监控磁盘空间

```bash
# 设置告警
df -h | grep -E '/$' | awk '{ if ($5+0 > 80) print "WARNING: Disk usage " $5 "%"}'
```

### 3. 日志轮转

```bash
# 清理旧日志
find /tmp -name "mcp_rebuild_*.log" -mtime +7 -delete
```

### 4. 版本控制

```bash
# 记录向量数据库版本
echo "$(date +%Y%m%d-%H%M%S)" > data/chroma/version.txt

# 查看版本
cat data/chroma/version.txt
```

---

## 支持

如遇到问题，请：

1. 查看日志文件
2. 参考 [DEPLOYMENT.md](../DEPLOYMENT.md)
3. 提交 Issue 到项目仓库

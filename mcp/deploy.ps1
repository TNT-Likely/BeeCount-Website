# BeeCount MCP Server 部署脚本 (Windows)
# 用途：在 Windows 服务器上部署 MCP 服务

$ErrorActionPreference = "Stop"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "BeeCount MCP Server 部署脚本" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python 版本
Write-Host "[1/8] 检查 Python 版本..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python 版本: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ 错误: 未找到 Python" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 检查系统资源
Write-Host "[2/8] 检查系统资源..." -ForegroundColor Yellow
$os = Get-CimInstance Win32_OperatingSystem
$totalMem = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
$freeMem = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
$disk = Get-PSDrive -Name C
$freeDisk = [math]::Round($disk.Free / 1GB, 2)

Write-Host "总内存: ${totalMem}GB"
Write-Host "可用内存: ${freeMem}GB"
Write-Host "可用磁盘: ${freeDisk}GB"

if ($freeMem -lt 1) {
    Write-Host "⚠ 警告: 可用内存不足 1GB，建议使用轻量模型" -ForegroundColor Yellow
}

if ($freeDisk -lt 2) {
    Write-Host "⚠ 警告: 可用磁盘不足 2GB，可能无法安装模型" -ForegroundColor Yellow
}
Write-Host ""

# 选择模型
Write-Host "[3/8] 选择嵌入模型..." -ForegroundColor Yellow
Write-Host "请选择嵌入模型（影响内存占用和搜索精度）："
Write-Host "  1) paraphrase-multilingual-MiniLM-L12-v2 (420MB, 高精度, 推荐)"
Write-Host "  2) paraphrase-multilingual-MiniLM-L6-v2 (200MB, 平衡, 轻量服务器)"
Write-Host "  3) paraphrase-multilingual-MiniLM-L8-v2 (300MB, 中等精度)"
Write-Host ""

$modelChoice = Read-Host "请输入选项 [1-3] (默认: 2)"
if ([string]::IsNullOrEmpty($modelChoice)) {
    $modelChoice = "2"
}

switch ($modelChoice) {
    "1" {
        $embeddingModel = "paraphrase-multilingual-MiniLM-L12-v2"
        Write-Host "✓ 选择模型: $embeddingModel (420MB)" -ForegroundColor Green
    }
    "2" {
        $embeddingModel = "paraphrase-multilingual-MiniLM-L6-v2"
        Write-Host "✓ 选择模型: $embeddingModel (200MB)" -ForegroundColor Green
    }
    "3" {
        $embeddingModel = "paraphrase-multilingual-MiniLM-L8-v2"
        Write-Host "✓ 选择模型: $embeddingModel (300MB)" -ForegroundColor Green
    }
    default {
        Write-Host "✗ 无效选项，使用默认模型" -ForegroundColor Red
        $embeddingModel = "paraphrase-multilingual-MiniLM-L6-v2"
    }
}
Write-Host ""

# 创建虚拟环境
Write-Host "[4/8] 创建虚拟环境..." -ForegroundColor Yellow
if (Test-Path "mcp_env") {
    Write-Host "虚拟环境已存在，跳过创建" -ForegroundColor Yellow
} else {
    python -m venv mcp_env
    Write-Host "✓ 虚拟环境创建成功" -ForegroundColor Green
}
Write-Host ""

# 激活虚拟环境并安装依赖
Write-Host "[5/8] 激活虚拟环境并安装依赖..." -ForegroundColor Yellow
& .\mcp_env\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
Write-Host "✓ 依赖安装完成" -ForegroundColor Green
Write-Host ""

# 配置环境变量
Write-Host "[6/8] 配置环境变量..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host ".env 文件已存在，跳过创建" -ForegroundColor Yellow
} else {
    Copy-Item .env.example .env
    
    # 更新模型配置
    (Get-Content .env) -replace "^EMBEDDING_MODEL=.*", "EMBEDDING_MODEL=$embeddingModel" | Set-Content .env
    
    Write-Host "✓ .env 文件创建成功" -ForegroundColor Green
    Write-Host "请根据需要修改 .env 文件中的其他配置" -ForegroundColor Yellow
}
Write-Host ""

# 生成向量索引
Write-Host "[7/8] 生成向量索引..." -ForegroundColor Yellow
Write-Host "这可能需要几分钟时间，请耐心等待..."
python run_server.py --rebuild-index
Write-Host "✓ 向量索引生成完成" -ForegroundColor Green
Write-Host ""

# 测试服务
Write-Host "[8/8] 测试 MCP 服务..." -ForegroundColor Yellow
$testResult = python tests\test_basic.py 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ 基础测试通过" -ForegroundColor Green
} else {
    Write-Host "⚠ 基础测试失败，请检查日志" -ForegroundColor Yellow
}

$testResult = python tests\test_vector.py 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ 向量搜索测试通过" -ForegroundColor Green
} else {
    Write-Host "⚠ 向量搜索测试失败，请检查日志" -ForegroundColor Yellow
}
Write-Host ""

# 完成
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "部署完成！" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "启动 MCP 服务:"
Write-Host "  .\mcp_env\Scripts\activate"
Write-Host "  python run_server.py"
Write-Host ""
Write-Host "后台运行 (PowerShell):"
Write-Host "  Start-Process python -ArgumentList 'run_server.py' -WindowStyle Hidden"
Write-Host ""
Write-Host "后台运行 (CMD):"
Write-Host "  start /B python run_server.py > mcp.log 2>&1"
Write-Host ""
Write-Host "使用 Windows 服务 (推荐):"
Write-Host "  # 安装 NSSM (Non-Sucking Service Manager)"
Write-Host "  nssm install BeeCountMCP python"
Write-Host "  nssm set BeeCountMCP AppDirectory (Get-Location)"
Write-Host "  nssm set BeeCountMCP AppParameters run_server.py"
Write-Host "  nssm set BeeCountMCP AppEnvironmentExtra PATH=%PATH%;(Get-Location)\mcp_env\Scripts"
Write-Host "  nssm start BeeCountMCP"
Write-Host ""
Write-Host "提示: 向量数据库已生成，后续文档更新后需要重新构建索引" -ForegroundColor Yellow
Write-Host "提示: 重建索引命令: python run_server.py --rebuild-index --language ALL" -ForegroundColor Yellow

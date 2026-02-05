# BeeCount MCP Server 部署脚本 (Windows)
# 用途：在 Windows 服务器上部署 MCP 服务

$ErrorActionPreference = "Stop"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "BeeCount MCP Server 部署脚本" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# 获取脚本所在目录的完整路径
$scriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent

# 确定mcp项目目录
# 如果脚本在mcp目录内（即$scriptDir包含mcp），则mcpProjectDir就是$scriptDir
# 否则，假设当前目录下有mcp文件夹
if ($scriptDir -match "\\mcp$" -or $scriptDir -match "/mcp$") {
    $mcpProjectDir = $scriptDir
} else {
    $mcpProjectDir = Join-Path -Path (Get-Location) -ChildPath "mcp"
}

# 定义虚拟环境目录（mcp同级）
$mcpParentDir = Split-Path -Path $mcpProjectDir -Parent
$venvDir = Join-Path -Path $mcpParentDir -ChildPath "mcp_env"

# 检查mcp项目目录是否存在
if (-not (Test-Path -Path $mcpProjectDir -PathType Container)) {
    Write-Host "✗ 错误: 未找到mcp项目目录！" -ForegroundColor Red
    Write-Host "  使用方法1：在mcp的同级目录执行 .\mcp\deploy.ps1"
    Write-Host "  使用方法2：进入mcp目录执行 .\deploy.ps1"
    exit 1
}
Write-Host "✓ 定位到MCP项目目录: $mcpProjectDir" -ForegroundColor Green
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

# 创建虚拟环境（mcp同级）
Write-Host "[4/8] 创建虚拟环境（mcp同级）..." -ForegroundColor Yellow
if (Test-Path -Path $venvDir) {
    Write-Host "虚拟环境已存在（$venvDir），跳过创建" -ForegroundColor Yellow
} else {
    python -m venv $venvDir
    Write-Host "✓ 虚拟环境创建成功: $venvDir" -ForegroundColor Green
}
Write-Host ""

# 激活虚拟环境并安装依赖
Write-Host "[5/8] 激活虚拟环境并安装依赖..." -ForegroundColor Yellow
# 拼接激活脚本路径
$activateScript = Join-Path -Path $venvDir -ChildPath "Scripts\Activate.ps1"
& $activateScript

$requirementsPath = Join-Path -Path $mcpProjectDir -ChildPath "requirements.txt"
if (-not (Test-Path -Path $requirementsPath)) {
    Write-Host "✗ 错误: 未找到requirements.txt（路径：$requirementsPath）" -ForegroundColor Red
    exit 1
}

python -m pip install --upgrade pip
pip install -r $requirementsPath
Write-Host "✓ 依赖安装完成" -ForegroundColor Green
Write-Host ""

# 配置环境变量
Write-Host "[6/8] 配置环境变量..." -ForegroundColor Yellow
$envExamplePath = Join-Path -Path $mcpProjectDir -ChildPath ".env.example"
$envPath = Join-Path -Path $mcpProjectDir -ChildPath ".env"

if (Test-Path -Path $envPath) {
    Write-Host ".env 文件已存在（$envPath），跳过创建" -ForegroundColor Yellow
} else {
    if (-not (Test-Path -Path $envExamplePath)) {
        Write-Host "✗ 错误: 未找到.env.example（路径：$envExamplePath）" -ForegroundColor Red
        exit 1
    }
    Copy-Item -Path $envExamplePath -Destination $envPath -Force
    
    # 更新模型配置
    (Get-Content -Path $envPath) -replace "^EMBEDDING_MODEL=.*", "EMBEDDING_MODEL=$embeddingModel" | Set-Content -Path $envPath
    
    Write-Host "✓ .env 文件创建成功: $envPath" -ForegroundColor Green
    Write-Host "请根据需要修改 .env 文件中的其他配置" -ForegroundColor Yellow
}
Write-Host ""

# 生成向量索引
Write-Host "[7/8] 生成向量索引..." -ForegroundColor Yellow
$runServerPath = Join-Path -Path $mcpProjectDir -ChildPath "run_server.py"
if (-not (Test-Path -Path $runServerPath)) {
    Write-Host "✗ 错误: 未找到run_server.py（路径：$runServerPath）" -ForegroundColor Red
    exit 1
}

Write-Host "这可能需要几分钟时间，请耐心等待..."
# 切换到mcp目录执行脚本（避免路径相关的相对导入问题）
Push-Location -Path $mcpProjectDir
python run_server.py --rebuild-index --language ALL --force
Pop-Location
Write-Host "✓ 向量索引生成完成" -ForegroundColor Green
Write-Host ""

# 测试服务  
Write-Host "[8/8] 测试 MCP 服务..." -ForegroundColor Yellow
# -------------------------- 核心修改5：指定mcp内的测试脚本路径 --------------------------
$testBasicPath = Join-Path -Path $mcpProjectDir -ChildPath "tests\test_basic.py"
$testVectorPath = Join-Path -Path $mcpProjectDir -ChildPath "tests\test_vector.py"

# 测试基础功能
Push-Location -Path $mcpProjectDir
$testResult = python tests\test_basic.py 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ 基础测试通过" -ForegroundColor Green
} else {
    Write-Host "⚠ 基础测试失败，请检查日志" -ForegroundColor Yellow
    Write-Host "测试输出: $testResult"
}

# 测试向量搜索
$testResult = python tests\test_vector.py 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ 向量搜索测试通过" -ForegroundColor Green
} else {
    Write-Host "⚠ 向量搜索测试失败，请检查日志" -ForegroundColor Yellow
    Write-Host "测试输出: $testResult"
}
Pop-Location
Write-Host ""

# 完成
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "部署完成！" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "当前目录结构（推荐）："
Write-Host "  $mcpParentDir/"
Write-Host "  ├── mcp/ (项目代码目录)"
Write-Host "  └── mcp_env/ (虚拟环境目录)"
Write-Host ""
Write-Host "启动 MCP 服务步骤:"
Write-Host "  1. 激活虚拟环境: $venvDir\Scripts\activate"
Write-Host "  2. 进入mcp目录: cd $mcpProjectDir"
Write-Host "  3. 启动服务: python run_server.py"
Write-Host ""
Write-Host "后台运行 (PowerShell):"
Write-Host "  $venvDir\Scripts\activate"
Write-Host "  cd $mcpProjectDir"
Write-Host "  Start-Process python -ArgumentList 'run_server.py' -WindowStyle Hidden"
Write-Host ""
Write-Host "后台运行 (CMD):"
Write-Host "  $venvDir\Scripts\activate.bat"
Write-Host "  cd /d $mcpProjectDir"
Write-Host "  start /B python run_server.py > mcp.log 2>&1"
Write-Host ""
Write-Host "使用 Windows 服务 (推荐):"
Write-Host "  # 安装 NSSM (Non-Sucking Service Manager)"
Write-Host "  nssm install BeeCountMCP $venvDir\Scripts\python.exe"
Write-Host "  nssm set BeeCountMCP AppDirectory $mcpProjectDir"
Write-Host "  nssm set BeeCountMCP AppParameters run_server.py"
Write-Host "  nssm start BeeCountMCP"
Write-Host ""
Write-Host "提示: 向量数据库已生成，后续文档更新后需要重新构建索引" -ForegroundColor Yellow
Write-Host "提示: 重建索引命令: cd $mcpProjectDir && python run_server.py --rebuild-index --language ALL" -ForegroundColor Yellow
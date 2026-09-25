# =============================================================================
# 企业级一体化平台 —— Windows 一键部署 (PowerShell)
# 前置: Windows 10/11 或 Server 2019+, 已安装 Docker Desktop (使用 WSL2 后端)
# 用法(管理员 PowerShell):
#   Set-ExecutionPolicy Bypass -Scope Process -Force
#   .\scripts\install.ps1
# =============================================================================
$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

function Info($m){ Write-Host "[INFO]  $m" -ForegroundColor Green }
function Warn($m){ Write-Host "[WARN]  $m" -ForegroundColor Yellow }
function Step($m){ Write-Host "`n==> $m" -ForegroundColor Cyan }
function Die($m){ Write-Host "[ERROR] $m" -ForegroundColor Red; exit 1 }

Write-Host "============================================================"
Write-Host " 企业级一体化平台 Windows 一键部署"
Write-Host " 目录: $Root"
Write-Host "============================================================"

# ------------------------------------------------------------ 1. Docker 检查
Step "1/6 检查 Docker Desktop"
$dockerOk = $false
try { docker info *> $null; if ($LASTEXITCODE -eq 0) { $dockerOk = $true } } catch {}
if (-not $dockerOk) {
    Die "未检测到运行中的 Docker Desktop。请先安装并启动 Docker Desktop (WSL2): https://www.docker.com/products/docker-desktop/"
}
Info "Docker: $(docker --version)"
try { docker compose version *> $null; if ($LASTEXITCODE -ne 0) { Die "Docker Desktop 版本过旧, 请升级以内置 compose v2" } } catch {}

# ------------------------------------------------------------ 2. 目录
Step "2/6 创建数据/日志/备份目录"
$dirs = @("data/mysql","data/redis","data/shared","data/ocr-models",
          "data/static","data/uploads","logs/nginx","logs/backend","logs/worker","backup")
foreach ($d in $dirs) { New-Item -ItemType Directory -Force -Path $d | Out-Null }
Info "目录就绪"

# ------------------------------------------------------------ 3. .env
Step "3/6 生成 .env"
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    function New-Pwd { -join ((48..57)+(65..90)+(97..122) | Get-Random -Count 20 | ForEach-Object {[char]$_}) }
    $rp = New-Pwd; $mp = New-Pwd; $up = New-Pwd
    # Windows 几乎都是 x86; ARM Windows 时改 rapid
    $arch = $env:PROCESSOR_ARCHITECTURE
    (Get-Content ".env") `
        -replace '^MYSQL_ROOT_PASSWORD=.*', "MYSQL_ROOT_PASSWORD=$rp" `
        -replace '^MYSQL_PASSWORD=.*',      "MYSQL_PASSWORD=$mp" `
        -replace '^REDIS_PASSWORD=.*',      "REDIS_PASSWORD=$up" | Set-Content ".env"
    if ($arch -match "ARM") {
        (Get-Content ".env") -replace '^OCR_ENGINE=.*','OCR_ENGINE=rapid' | Set-Content ".env"
        Warn "ARM 设备, OCR 引擎自动切换为 rapid(ONNX)"
    }
    Info ".env 已生成并随机化密码"
} else { Info ".env 已存在, 保留" }

# ------------------------------------------------------------ 4. 拉取/构建
Step "4/6 拉取基础镜像"
docker compose pull mysql redis nginx
if ($LASTEXITCODE -ne 0) { Warn "基础镜像拉取失败, 请检查网络/镜像加速配置(Docker Desktop -> Settings -> Docker Engine)" }

$profileArgs = @()
if (Test-Path "backend/app.jar") { $profileArgs += @("--profile","backend"); Info "检测到 app.jar, 启用 Java 后端" }
else { Warn "未发现 backend/app.jar, 跳过 Java 后端" }

Step "5/6 构建本地镜像(OCR/Browser/Worker)"
docker compose @profileArgs build
if ($LASTEXITCODE -ne 0) { Die "镜像构建失败" }

Step "6/6 启动"
docker compose @profileArgs up -d
Start-Sleep -Seconds 10
docker compose ps

Write-Host "`n==================== 部署完成 ====================" -ForegroundColor Green
Write-Host " Nginx 入口 : http://localhost"
Write-Host " 状态/日志  : .\scripts\control.ps1 status | logs"
Write-Host " 停止/重启  : .\scripts\control.ps1 stop | restart"
Write-Host "==================================================" -ForegroundColor Green

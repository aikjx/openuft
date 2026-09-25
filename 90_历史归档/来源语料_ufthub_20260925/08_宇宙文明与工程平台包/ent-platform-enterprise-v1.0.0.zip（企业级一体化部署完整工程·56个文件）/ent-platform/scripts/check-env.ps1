# Windows 环境自检
$ErrorActionPreference = "Continue"
Write-Host "==> 1. Docker Desktop" -ForegroundColor Cyan
try { docker info *> $null; if ($LASTEXITCODE -eq 0) { Write-Host " [√] Docker 运行中" -ForegroundColor Green } else { Write-Host " [×] Docker 未运行, 请启动 Docker Desktop" -ForegroundColor Red } } catch { Write-Host " [×] 未安装 Docker Desktop" -ForegroundColor Red }

Write-Host "==> 2. Compose" -ForegroundColor Cyan
try { docker compose version *> $null; if ($LASTEXITCODE -eq 0) { Write-Host " [√] compose v2 可用" -ForegroundColor Green } else { Write-Host " [×] 缺少 compose, 升级 Docker Desktop" -ForegroundColor Red } } catch {}

Write-Host "==> 3. WSL2" -ForegroundColor Cyan
$wsl = wsl -l -v 2>$null
if ($wsl) { Write-Host " [√] WSL 已安装:" -ForegroundColor Green; $wsl | ForEach-Object { Write-Host "     $_" } }
else { Write-Host " [×] 未安装 WSL2 (wsl --install)" -ForegroundColor Red }

Write-Host "==> 4. 端口占用" -ForegroundColor Cyan
foreach ($p in 80,3306,6379) {
    $busy = Get-NetTCPConnection -State Listen -LocalPort $p -ErrorAction SilentlyContinue
    if ($busy) { Write-Host " [×] 端口 $p 被占用, 修改 .env" -ForegroundColor Red }
    else { Write-Host " [√] 端口 $p 空闲" -ForegroundColor Green }
}

Write-Host "==> 5. 工程文件" -ForegroundColor Cyan
$files = @("docker-compose.yml",".env.example","mysql/conf/my.cnf","redis/conf/redis.conf","nginx/nginx.conf")
foreach ($f in $files) {
    if (Test-Path $f) { Write-Host " [√] $f" -ForegroundColor Green }
    else { Write-Host " [×] 缺失 $f" -ForegroundColor Red }
}
Write-Host "`n自检完成, 无 [×] 后执行 .\scripts\install.ps1"

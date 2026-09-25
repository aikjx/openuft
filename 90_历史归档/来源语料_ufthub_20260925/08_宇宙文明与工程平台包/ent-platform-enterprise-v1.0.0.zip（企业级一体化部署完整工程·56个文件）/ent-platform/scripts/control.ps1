# =============================================================================
# Windows 统一运维控制
# 用法: .\scripts\control.ps1 start|stop|restart|status|logs|down|rebuild|shell
# 例 : .\scripts\control.ps1 logs worker
# =============================================================================
param(
    [Parameter(Position=0)][string]$Action = "status",
    [Parameter(Position=1, ValueFromRemainingArguments=$true)][string[]]$Rest
)
$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot ".."))

$profileArgs = @()
if (Test-Path "backend/app.jar") { $profileArgs = @("--profile","backend") }

switch ($Action) {
    "start"   { docker compose @profileArgs up -d @Rest; docker compose ps }
    "stop"    { docker compose stop @Rest }
    "restart" { docker compose @profileArgs restart @Rest; docker compose ps }
    "down"    { docker compose down @Rest }
    "status"  { docker compose ps @Rest }
    "ps"      { docker compose ps @Rest }
    "logs"    { docker compose logs --tail=200 @Rest }
    "rebuild" { docker compose @profileArgs build @Rest; docker compose @profileArgs up -d @Rest }
    "pull"    { docker compose pull; docker compose @profileArgs build --pull }
    "shell"   {
        $svc = if ($Rest) { $Rest[0] } else { "worker" }
        docker compose exec $svc bash
    }
    default {
        Write-Host "用法: .\scripts\control.ps1 <start|stop|restart|status|logs|down|rebuild|shell> [服务]"
        exit 1
    }
}

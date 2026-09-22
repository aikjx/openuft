# 一次性整理脚本：将各独立体系根目录的松散 .md 报告按性质归入 12_研究结论 / 13_论文与成果
# 根目录保留：README.md / sources.md / system.json / claims.csv
# 碰撞安全：目标已存在同名文件则跳过（避免覆盖阶段目录中已有的规范文件）
$ErrorActionPreference = 'Stop'
$base = "d:\a10\aikjx\code\my_lib\openuft\01_独立体系"
$keep = @('README.md', 'sources.md')

function Classify($name) {
  if ($name -match '报告|总结|分析') { return '12_研究结论' }
  if ($name -match '定理|证明|推导|精算|谱') { return '13_论文与成果' }
  return '12_研究结论'
}

foreach ($sysDir in Get-ChildItem -Path $base -Directory) {
  $loose = Get-ChildItem -Path $sysDir.FullName -File -Filter *.md |
    Where-Object { $_.Name -notin $keep }
  if ($loose.Count -eq 0) { continue }
  Write-Host "== $($sysDir.Name) : $($loose.Count) 个松散文件 =="
  foreach ($f in $loose) {
    $destDir = Join-Path $sysDir.FullName (Classify $f.Name)
    if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir | Out-Null }
    $dest = Join-Path $destDir $f.Name
    if (Test-Path $dest) {
      Write-Host "  SKIP (目标已存在): $($f.Name) -> $destDir"
    } else {
      Move-Item -LiteralPath $f.FullName -Destination $dest
      Write-Host "  MOVED: $($f.Name) -> $destDir"
    }
  }
}
Write-Host "整理完成。"

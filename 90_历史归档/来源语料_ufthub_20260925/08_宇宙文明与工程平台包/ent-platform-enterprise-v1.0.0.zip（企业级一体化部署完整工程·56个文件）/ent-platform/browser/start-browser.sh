#!/bin/bash
# 找到 Playwright 镜像内置的 Chromium 可执行文件并以 headless + CDP 常驻启动
set -euo pipefail

CHROME_BIN="$(find /ms-playwright -type f \( -name chrome -o -name headless_shell \) | grep -v crashpad | head -n1)"
if [ -z "${CHROME_BIN}" ]; then
  echo "[browser] chromium not found under /ms-playwright, run 'npx playwright install chromium'" >&2
  exit 1
fi
echo "[browser] using chromium: ${CHROME_BIN}"

# --no-sandbox: 容器内必须; --disable-dev-shm-usage: 配合 shm_size 防崩溃
# --remote-allow-origins=*: 新版 Chromium CDP 跨域要求
exec "${CHROME_BIN}" \
  --headless=new \
  --no-sandbox \
  --disable-dev-shm-usage \
  --disable-gpu \
  --hide-scrollbars \
  --font-render-hinting=none \
  --remote-debugging-address=0.0.0.0 \
  --remote-debugging-port=9222 \
  --remote-allow-origins=* \
  --user-data-dir=/tmp/chrome-profile \
  about:blank

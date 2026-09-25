#!/bin/bash
# =============================================================================
# 多架构镜像构建 (x86_64 + aarch64), 用于在一台机器上给两类服务器出镜像
# 前置: docker buildx create --use (脚本会自动初始化 builder)
# 用法:
#   bash scripts/build-multiarch.sh registry.local/ent   # 构建并推送到私有仓库
#   LOAD_AMD64=1 bash scripts/build-multiarch.sh         # 只构建本机架构并 load
# 信创(鲲鹏/飞腾 = arm64) 服务器直接拉 arm64 tag 即可; 龙芯见 docs/08
# =============================================================================
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"
load_env 2>/dev/null || true

REG="${1:-ent}"   # 镜像名前缀
ARCH="$(detect_arch)"

# 初始化 buildx (只需一次)
if ! docker buildx ls | grep -q ent-builder; then
    step "初始化 buildx builder (ent-builder)"
    docker buildx create --name ent-builder --driver docker-container --use
else
    docker buildx use ent-builder
fi
docker buildx inspect --bootstrap

OCR_ENGINE="${OCR_ENGINE:-paddle}"

build_push() {
    local svc="$1" ctx="$2" extra="$3"
    step "多架构构建 $svc -> $REG/$svc"
    docker buildx build --platform linux/amd64,linux/arm64 \
        $extra -t "$REG/$svc:latest" --push "$ctx"
}

if [ "${LOAD_AMD64:-0}" = "1" ]; then
    step "仅构建本机($ARCH)镜像并导入本地 docker"
    compose build
    exit 0
fi

build_push browser ./browser "--build-arg PLAYWRIGHT_TAG=${PLAYWRIGHT_TAG:-v1.48.0-jammy}"
build_push worker  ./worker  "--build-arg PYTHON_TAG=${PYTHON_TAG:-3.10-slim}"
build_push ocr     ./ocr     "--build-arg OCR_ENGINE=${OCR_ENGINE} --build-arg PYTHON_TAG=${PYTHON_TAG:-3.10-slim}"
[ -f backend/app.jar ] && build_push backend ./backend "" || warn "无 backend/app.jar, 跳过"

step "完成。信创 arm64 服务器拉取示例:"
cat <<EOF
  docker pull $REG/ocr:latest
  # 或离线: bash scripts/offline-save.sh  在目标架构机器上执行后拷贝
EOF

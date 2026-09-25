#!/bin/bash
# =============================================================================
# 离线交付包制作 (信创内网/政务专网场景)
# 产物: packages/ent-offline-<arch>-<date>.tar.gz
#   内容: 1) 全部镜像 images.tar (目标机 docker load)
#         2) 工程代码/compose/配置/脚本
# 注意: 必须在【与目标服务器相同 CPU 架构】的机器上执行本脚本!
#   x86 服务器部署 -> 在 x86 机器执行; 鲲鹏/飞腾 arm64 -> 在 arm64 机器执行
# =============================================================================
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"
load_env
ARCH="$(detect_arch)"
TS="$(date +%Y%m%d)"
STAGE="packages/offline-${ARCH}-${TS}"
PKG="packages/ent-offline-${ARCH}-${TS}.tar.gz"

step "1/4 确保本地镜像为最新"
PROFILE_ARGS="$(backend_profile_args)"
compose ${PROFILE_ARGS} build
compose pull mysql redis nginx || true

step "2/4 收集镜像清单并 docker save"
IMAGES=$(compose config --images | sort -u)
echo "$IMAGES"
mkdir -p "$STAGE"
# shellcheck disable=SC2086
docker save $IMAGES -o "$STAGE/images.tar"

step "3/4 拷贝工程文件(排除数据/日志/历史包)"
mkdir -p "$STAGE/app"
tar --exclude='./data' --exclude='./logs' --exclude='./packages' \
    --exclude='./.git' -cf - . | tar -xf - -C "$STAGE/app"
cat > "$STAGE/离线安装说明.txt" <<EOF
企业平台离线安装包 (架构: ${ARCH}, 制作: ${TS})
1. 解压: tar -xzf ent-offline-${ARCH}-${TS}.tar.gz
2. 导入镜像: docker load -i images.tar
3. 进入 app 目录: OFFLINE=1 bash scripts/install.sh
EOF

step "4/4 打包"
tar -czf "$PKG" -C packages "offline-${ARCH}-${TS}"
rm -rf "$STAGE"
ls -lh "$PKG"
log "离线包完成: $PKG —— 拷贝到同架构内网服务器即可"

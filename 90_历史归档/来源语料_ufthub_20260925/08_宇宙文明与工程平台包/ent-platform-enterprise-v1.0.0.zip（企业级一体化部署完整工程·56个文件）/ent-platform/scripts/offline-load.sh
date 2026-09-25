#!/bin/bash
# =============================================================================
# 离线安装: 在目标内网服务器上执行
# 用法: bash scripts/offline-load.sh packages/ent-offline-<arch>-xxx.tar.gz
# =============================================================================
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"
require_docker

PKG="${1:-}"
[ -z "$PKG" ] && die "用法: bash scripts/offline-load.sh <离线包.tar.gz>"
[ -f "$PKG" ] || die "找不到 $PKG"

step "1/3 解压离线包"
TMP="packages/_offline_tmp"
rm -rf "$TMP"; mkdir -p "$TMP"
tar -xzf "$PKG" -C "$TMP"
DIR="$(find "$TMP" -maxdepth 1 -type d -name 'offline-*' | head -1)"

step "2/3 导入镜像"
docker load -i "$DIR/images.tar"

step "3/3 进入工程目录执行离线安装"
cp -a "$DIR/app/." ./
rm -rf "$TMP"
OFFLINE=1 bash scripts/install.sh
log "离线部署完成"

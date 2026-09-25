#!/bin/bash
# =============================================================================
# 一键恢复: bash scripts/restore.sh backup/backup-YYYYmmdd-HHMMSS.tar.gz
# 警告: 会覆盖当前数据库内容, 执行前请先停掉 Worker/后端写入
# =============================================================================
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"
load_env

PKG="${1:-}"
[ -z "$PKG" ] && die "用法: bash scripts/restore.sh backup/backup-xxxx.tar.gz"
[ -f "$PKG" ] || die "备份包不存在: $PKG"

step "解压 $PKG"
TMP="$(mktemp -d)"
tar -xzf "$PKG" -C "$TMP"
DIR="$(find "$TMP" -maxdepth 1 -type d | tail -1)"

step "恢复 MySQL"
SQL_GZ="$(find "$DIR" -name '*.sql.gz' | head -1 || true)"
if [ -n "$SQL_GZ" ]; then
    gunzip -c "$SQL_GZ" | compose exec -T mysql sh -c "mysql -uroot -p\"$MYSQL_ROOT_PASSWORD\""
    log "数据库已恢复"
else
    warn "备份包中无 MySQL 备份"
fi

step "恢复 Redis 数据"
if [ -f "$DIR/redis-data.tar.gz" ]; then
    compose stop redis
    tar -xzf "$DIR/redis-data.tar.gz" -C data
    compose start redis
    log "Redis 已恢复"
fi

rm -rf "$TMP"
step "恢复完成, 建议执行 bash scripts/control.sh restart"

#!/bin/bash
# =============================================================================
# 一键备份: MySQL 逻辑备份 + Redis RDB + 共享截图目录, 打包到 backup/
# 用法: bash scripts/backup.sh            # 全量
#       bash scripts/backup.sh db         # 只备数据库
# 建议 crontab:  0 2 * * * cd /opt/ent-platform && bash scripts/backup.sh >> logs/backup.log 2>&1
# =============================================================================
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"
load_env
MODE="${1:-all}"
TS="$(date +%Y%m%d-%H%M%S)"
OUT="backup/backup-${TS}"
mkdir -p "$OUT"

if [ "$MODE" = "all" ] || [ "$MODE" = "db" ]; then
    step "备份 MySQL (${MYSQL_DATABASE})"
    compose exec -T mysql sh -c \
      "mysqldump -uroot -p\"$MYSQL_ROOT_PASSWORD\" --single-transaction --routines --triggers --events --databases \"$MYSQL_DATABASE\"" \
      | gzip > "$OUT/mysql-${MYSQL_DATABASE}.sql.gz"
    log "-> $OUT/mysql-${MYSQL_DATABASE}.sql.gz"
fi

if [ "$MODE" = "all" ] || [ "$MODE" = "redis" ]; then
    step "触发 Redis BGSAVE 并拷贝 RDB/AOF"
    compose exec -T redis redis-cli -a "$REDIS_PASSWORD" --no-auth-warning BGSAVE >/dev/null || true
    sleep 2
    tar -czf "$OUT/redis-data.tar.gz" -C data redis
    log "-> $OUT/redis-data.tar.gz"
fi

if [ "$MODE" = "all" ]; then
    step "备份共享数据(截图等)"
    tar -czf "$OUT/shared.tar.gz" -C data shared 2>/dev/null || true
    # 同时快照一份 .env(含密码, 注意权限)
    cp .env "$OUT/env.snapshot" && chmod 600 "$OUT/env.snapshot"
fi

tar -czf "${OUT}.tar.gz" -C backup "backup-${TS}" && rm -rf "$OUT"
step "备份完成: ${OUT}.tar.gz ($(du -h "${OUT}.tar.gz" | awk '{print $1}'))"

# 自动清理 14 天前备份
find backup -name 'backup-*.tar.gz' -mtime +14 -print -delete

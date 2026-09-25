#!/bin/bash
# =============================================================================
# 按宿主机可用内存自动生成 MySQL/Redis 最优内存参数覆盖文件
# 生成结果: mysql/conf/zz-auto.cnf / redis/conf/zz-auto.conf
# ( compose 已挂载 conf 目录的等价路径; 本脚本直接改写主配置中的关键行)
# 参考基准:
#   2G  -> MySQL 512M / Redis 256M
#   4G  -> MySQL 1G   / Redis 512M
#   8G  -> MySQL 4G   / Redis 1G
#  16G  -> MySQL 8G   / Redis 2G
# =============================================================================
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"

MEM_MB=$(awk '/MemTotal/{printf "%d", $2/1024}' /proc/meminfo)
log "宿主机内存: ${MEM_MB} MB"

if   [ "$MEM_MB" -ge 15000 ]; then MYSQL_POOL=8G; REDIS_MAX=2g
elif [ "$MEM_MB" -ge 7000 ];  then MYSQL_POOL=4G; REDIS_MAX=1g
elif [ "$MEM_MB" -ge 3500 ];  then MYSQL_POOL=1G; REDIS_MAX=512mb
else                            MYSQL_POOL=384M; REDIS_MAX=256mb
fi

# 重算 buffer pool instances (每实例约 1G)
case "$MYSQL_POOL" in
    8G) INST=8 ;; 4G) INST=4 ;; 1G) INST=1 ;; *) INST=1 ;;
esac

log "调优结果: innodb_buffer_pool_size=${MYSQL_POOL}, instances=${INST}, redis maxmemory=${REDIS_MAX}"
sed -i -E "s/^innodb_buffer_pool_size[[:space:]]*=.*/innodb_buffer_pool_size = ${MYSQL_POOL}/" mysql/conf/my.cnf
sed -i -E "s/^innodb_buffer_pool_instances[[:space:]]*=.*/innodb_buffer_pool_instances = ${INST}/" mysql/conf/my.cnf
sed -i -E "s/^maxmemory[[:space:]]+.*/maxmemory ${REDIS_MAX}/" redis/conf/redis.conf
log "已写入 mysql/conf/my.cnf 与 redis/conf/redis.conf"

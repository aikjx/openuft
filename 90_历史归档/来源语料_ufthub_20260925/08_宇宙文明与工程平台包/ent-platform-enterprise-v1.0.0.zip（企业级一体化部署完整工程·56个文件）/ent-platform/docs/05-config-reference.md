# 05 · 配置详解（.env 每项含义 + 最优默认）

> 原则：**只改 `.env`，不改 compose**。改完执行 `bash scripts/control.sh restart`。

## 1. 全量配置项说明

| 配置项 | 默认值 | 说明 / 最优实践 |
|---|---|---|
| `TZ` | Asia/Shanghai | 容器时区，MySQL 也单独设了 +08:00 |
| `HTTP_PORT` | 80 | Nginx 对外端口；80 被占（如 IIS/apache）改 8080 |
| `MYSQL_PORT` | 3306 | 只绑 127.0.0.1；被占就改，容器内仍是 3306 |
| `REDIS_PORT` | 6379 | 同上 |
| `MYSQL_ROOT_PASSWORD` | 随机生成 | root 仅管理用，业务不用 root |
| `MYSQL_DATABASE` | appdb | 业务库名，首启自动建 |
| `MYSQL_USER/PASSWORD` | appuser/随机 | 业务账号，只授业务库权限 |
| `REDIS_PASSWORD` | 随机 | 启动参数注入，不写死在 redis.conf |
| `TASK_QUEUE/RESULT_QUEUE` | rpa:tasks/results | Worker 消费/回写队列名 |
| `MYSQL_TAG` | 8.0 | 生产锁大版本，不用 latest |
| `REDIS_TAG` | 7.2 | 同上 |
| `NGINX_TAG` | 1.27 | 稳定版 |
| `PYTHON_TAG` | 3.10-slim | slim 体积小；信创若源缺包可换 3.10（完整） |
| `PLAYWRIGHT_TAG` | v1.48.0-jammy | **必须与 worker 的 playwright==1.48.0 大版本一致**，否则 CDP 协议可能不兼容 |
| `SPRING_PROFILES` | prod | Spring profile |
| `JAVA_OPTS` | -Xms512m -Xmx1024m G1GC | 见下方按规格表 |
| `OCR_ENGINE` | x86=paddle / arm=rapid | 飞桨 vs ONNX，安装时按架构自动定 |
| `OCR_LANG` | ch | 中文；英文 en、多语言见 PaddleOCR 文档 |
| `OCR_WORKERS` | 1 | 单实例非线程安全，要并发就扩副本不要加这个 |
| `WORKER_CONCURRENCY` | 2 | 单 worker 容器内并发页面，吃 CPU/内存，低配设 1 |
| `PAGE_TIMEOUT` | 60000 | 页面超时 ms |
| `HTTP_PROXY/HTTPS_PROXY` | 空 | IP 任务出口代理 `http://user:pass@ip:port`，留空直连 |

## 2. 按机器规格的最优参数（直接抄）

### 2C2G（最小/边缘信创机）
```ini
JAVA_OPTS=-Xms256m -Xmx512m -XX:+UseG1GC
WORKER_CONCURRENCY=1
OCR_ENGINE=rapid
# tune-memory.sh 会自动把 MySQL pool=384M / Redis=256M
```
### 4C8G（标准生产）
```ini
JAVA_OPTS=-Xms1g -Xmx2g -XX:+UseG1GC -XX:MaxGCPauseMillis=200
WORKER_CONCURRENCY=3
OCR_ENGINE=paddle
# MySQL pool=4G / Redis=1g
```
### 8C16G+（高吞吐）
```ini
JAVA_OPTS=-Xms2g -Xmx4g -XX:+UseG1GC
WORKER_CONCURRENCY=4
# docker compose up -d --scale ocr=2 --scale worker=3
# MySQL pool=8G / Redis=2g
```

## 3. MySQL 关键调优解释（mysql/conf/my.cnf）

| 参数 | 默认给值 | 为什么 |
|---|---|---|
| `innodb_buffer_pool_size` | 按内存 50~70% | 缓存索引+数据，最影响性能的参数，tune-memory.sh 自动算 |
| `innodb_flush_log_at_trx_commit` | 2 | 1 最安全但每次事务刷盘；2 每秒刷，宕机最多丢 1s，自动化业务性价比最高；金融场景改回 1 |
| `innodb_flush_method` | O_DIRECT | 绕过 OS 页缓存，避免双重缓冲 |
| `innodb_io_capacity(_max)` | 2000/4000 | SSD 基准；SATA 机械盘降到 400/800，NVMe 提到 4000/8000 |
| `max_connections` | 500 | 配合 Java Hikari 连接池（建议池大小 10~30，不是越大越好） |
| `skip-name-resolve` | ON | 跳过 DNS 反查，连接更快，授权只认 IP |
| `binlog_expire_logs_seconds` | 7 天 | 防止 binlog 撑爆磁盘 |

## 4. Redis 关键调优解释（redis/conf/redis.conf）

| 参数 | 值 | 为什么 |
|---|---|---|
| `appendonly` / `appendfsync` | yes / everysec | AOF，宕机最多丢 1 秒，任务队列不轻易丢 |
| `maxmemory-policy` | volatile-lru | 只淘汰带 TTL 的缓存 key，**队列 List 不设 TTL 永不淘汰**；纯缓存场景可换 allkeys-lru |
| `maxmemory` | 内存 60% | 留足 AOF fork 与系统内存，防止 OOM |
| `save` | 900/300/60 三档 | RDB 兜底，AOF+RDB 混合持久化 |

## 5. Nginx 关键配置解释

| 配置 | 值 | 作用 |
|---|---|---|
| `worker_processes` | auto | 自动等于 CPU 核数 |
| `worker_connections` | 10240 | 单 worker 连接上限 |
| `upstream keepalive 64` | — | 到 Java 保持长连接，省掉反复 TCP 握手 |
| `limit_req_zone` | 10r/s burst20 | 每 IP 限流，按业务调/删 |
| `client_max_body_size` | 50m | 截图/上传上限 |
| `proxy_read_timeout` | 60s | 自动化接口若耗时长，在这里和 Java 侧一起调大 |

## 6. 改配置的标准动作
```bash
vim .env                                   # 1.改配置
bash scripts/control.sh restart           # 2.重启生效(改 my.cnf 只 restart mysql)
bash scripts/control.sh logs --tail=100   # 3.看日志确认
```

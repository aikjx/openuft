# 06 · 运维手册

## 1. 日常命令（control.sh / control.ps1）

| 操作 | Linux | Windows |
|---|---|---|
| 启动 | `bash scripts/control.sh start` | `.\scripts\control.ps1 start` |
| 停止（数据保留） | `bash scripts/control.sh stop` | `.\scripts\control.ps1 stop` |
| 重启 | `bash scripts/control.sh restart` | `.\scripts\control.ps1 restart` |
| 只重启一个服务 | `... restart ocr` | `... restart ocr` |
| 状态 | `... status` | `... status` |
| 实时日志 | `... logs -f worker` | `... logs worker` |
| 资源占用 | `... top` | `docker stats` |
| 进容器 | `... shell mysql` | `... shell mysql` |
| 改代码后上线 | `... rebuild worker` | `... rebuild worker` |
| 彻底下线 | `... down` | `... down` |

## 2. 备份与恢复

### 自动备份（每天凌晨 2 点）
```bash
crontab -e
0 2 * * * cd /opt/ent-platform && bash scripts/backup.sh >> logs/backup.log 2>&1
```
- 备份内容：MySQL 逻辑备份(gzip) + Redis RDB/AOF + 共享截图 + `.env` 快照
- 输出：`backup/backup-YYYYmmdd-HHMMSS.tar.gz`，自动清理 14 天前
- 只备库：`bash scripts/backup.sh db`

### 恢复演练（每季度至少一次）
```bash
bash scripts/control.sh stop worker backend     # 先停写入方
bash scripts/restore.sh backup/backup-20260910-020000.tar.gz
bash scripts/control.sh start
```

### 整机迁移（换服务器/信创替换）
```bash
# 旧机
bash scripts/control.sh stop
tar -czf ent-migrate.tar.gz ent-platform
# 同架构新机: 解压后 docker compose up -d 即可(数据目录原样)
```

## 3. 水平扩容

```bash
# Worker 扩到 3 个并发副本、OCR 扩 2 个
docker compose up -d --scale worker=3 --scale ocr=2
```
- Worker 是队列消费模型，多副本天然竞争消费，**无需改代码**。
- OCR 多副本时 Worker 默认访问服务名 `http://ocr:8000`，Docker 内置 DNS 会轮询；也可在前面加一个内网 Nginx 做 least_conn。
- Browser 多副本同理；注意每个 Chromium 约 300~600M 内存。

## 4. 版本升级

```bash
# 1) 备份!
bash scripts/backup.sh db
# 2) 更新代码/镜像版本(改 .env 的 TAG 或替换 jar)
bash scripts/control.sh pull        # 拉新基础镜像并重build本地镜像
bash scripts/control.sh restart
# 3) 观察
bash scripts/control.sh status && bash scripts/control.sh logs --tail=200
# 回滚: 把 TAG 改回旧版本 restart; 数据层回滚用 restore.sh
```

## 5. 日志治理

- 容器 stdout：compose 已统一 `json-file max-size=50m max-file=5`，单服务最多 250M。
- 文件日志：`./logs/<服务>/`。建议再加 logrotate：
```
# /etc/logrotate.d/ent-platform
/opt/ent-platform/logs/*.log {
    weekly rotate 8 missingok notifempty compress copytruncate
}
```
- 截图目录 `./data/shared` 定期清理（示例：删 7 天前）：
```bash
find /opt/ent-platform/data/shared -name '*.png' -mtime +7 -delete
```

## 6. 健康巡检（可做每日脚本/监控接入）

| 检查 | 命令 | 期望 |
|---|---|---|
| 容器状态 | `docker compose ps` | 全部 running/healthy |
| Nginx | `curl -s http://127.0.0.1/healthz` | ok |
| MySQL | `docker exec ent-mysql mysqladmin -uroot -p$PWD ping` | alive |
| Redis | `docker exec ent-redis redis-cli -a $PWD ping` | PONG |
| OCR | `docker exec ent-ocr python -c "import urllib.request;print(urllib.request.urlopen('http://127.0.0.1:8000/health').read())"` | engine 信息 |
| 队列堆积 | `redis-cli LLEN rpa:tasks` | 持续增长说明 Worker 不够或卡死，需扩容/排查 |
| 磁盘 | `df -h /opt` | 低于 80% |
| 内存 | `free -h` / `docker stats` | 无接近 limit 的容器 |

对接 Prometheus 时：MySQL 用 mysqld-exporter、Redis 用 redis-exporter、Java 用 Actuator+Micrometer、cAdvisor 采容器指标。

## 7. 常用排障命令速查
```bash
docker compose ps -a                      # 看退出码
docker logs ent-ocr --tail 200            # 单容器日志
docker inspect ent-worker --format '{{json .State}}'   # 崩溃原因
docker exec -it ent-mysql mysql -uroot -p # 进 MySQL
docker exec -it ent-redis redis-cli -a 密码            # 进 Redis
docker stats                              # 实时资源
docker system df                          # docker 磁盘占用
docker system prune -af                   # 清理悬空镜像(谨慎)
```

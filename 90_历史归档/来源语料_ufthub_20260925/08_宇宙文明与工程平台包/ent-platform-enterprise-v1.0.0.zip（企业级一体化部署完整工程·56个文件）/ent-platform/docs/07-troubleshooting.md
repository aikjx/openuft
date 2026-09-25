# 07 · 故障排查手册（现象 → 原因 → 解决）

## 1. 安装阶段

### install.sh 卡在拉镜像 / timeout / TLS handshake timeout
- **原因**：访问 DockerHub 慢。
- **解决**：脚本已写阿里云/通用镜像加速；手动改 `/etc/docker/daemon.json` 的 `registry-mirrors` 后 `systemctl restart docker`。信创内网用离线包（04 第 5 节）。

### 麒麟/UOS 装 docker-ce 失败（找不到包/依赖冲突）
- **原因**：信创系统自带源与 docker-ce 源不匹配。
- **解决**：直接用系统源 `sudo apt install docker.io docker-compose-plugin`（脚本已优先走这条）；或用系统厂商软件仓库里的 docker-engine。

### arm64 构建 OCR paddle 镜像时报 pip 找不到 paddlepaddle
- **原因**：飞桨某些版本 aarch64 wheel 不全。
- **解决**：`.env` 设 `OCR_ENGINE=rapid`（安装脚本在 arm 上已自动切换）。需要飞桨时去飞桨官网按 aarch64 安装命令替换 `requirements-paddle.txt` 的索引地址。

### Windows：WSL2 错误 / Docker Desktop 起不来
- 解决：管理员执行 `wsl --update`、`wsl --set-default-version 2`；BIOS 开虚拟化；Settings→General 勾选 WSL2。

## 2. 容器反复重启（restarting）

### ent-mysql 一直 restart
1. `docker logs ent-mysql`：
   - `different lower_case_table_names` / `unknown variable`：之前用别的 MySQL 大版本初始化过 `data/mysql`，**数据目录版本不兼容**。备份后清空 `data/mysql` 重新初始化（或保持同一大版本）。
   - `Access denied; ... password`：`.env` 密码与 data 目录里初始化过的密码不一致——数据目录一旦初始化，改 `.env` 密码不会改库内密码。要么改回旧密码，要么进库 `ALTER USER`。
   - `InnoDB: Cannot allocate memory`：内存不足，调小 `innodb_buffer_pool_size`（tune-memory.sh）。

### ent-ocr 启动 90 秒后 unhealthy
- 首次启动要下载模型，内网不通会卡住：把模型预置到 `./data/ocr-models`（映射 `/root/.ocr-models`），或先在联网环境跑一次再整体拷贝 data。
- 看日志确认是否 warmup 报错；rapid 引擎模型随 pip 包自带，不存在下载问题。

### ent-browser 崩溃 / `SessionNotCreated` / 页面白屏崩溃
- 90% 是 shm 不足：compose 已给 `shm_size: 2g`，若被覆盖请恢复；启动参数必须有 `--no-sandbox --disable-dev-shm-usage`。
- 截图中文是方块：镜像已装 Noto CJK / 文泉驿；自定义镜像记得装 `fonts-noto-cjk`。

### worker 报 `connect ECONNREFUSED browser:9222 / ocr:8000`
- 启动顺序问题：worker 已内置 30 次重试等待；若仍失败，`control.sh status` 看 browser/ocr 是否 healthy；确认三个服务都在同一 `ent-core` 网络：`docker network inspect ent-core`。

## 3. 运行阶段

### 任务在队列里不减少（LLEN 一直涨）
1. `docker logs ent-worker` 看是否在报错循环。
2. Worker 并发不够：`--scale worker=3` 或调大 `WORKER_CONCURRENCY`（注意内存）。
3. 页面卡死：调小 `PAGE_TIMEOUT`，检查代理 `HTTP_PROXY` 是否可用、目标站是否封 IP（换代理池）。

### OCR 识别慢
- 确认模型只加载一次（日志只出现一次 warmup），不要在业务代码里反复 new。
- 小图多走 `/ocr/batch` 批量；GPU 用 gpu compose；x86 上 paddle 比 rapid 精度高，arm CPU 上 rapid 更稳。
- Docker 本身损耗仅 1~3%，慢基本都在模型加载/图片传输/单线程串行。

### Java 连不上 MySQL：Communications link failure / Access denied
- 容器内主机名是 `mysql` 不是 `127.0.0.1`（compose 服务名互通）。
- 账号允许远程：MySQL 8 用户 host 为 `%`（初始化账号默认就是 `%`）。
- 时区参数带 `serverTimezone=Asia/Shanghai`。

### Java 连不上 Redis：NOAUTH / WRONGPASS
- 容器内地址 `redis://:密码@redis:6379/0`，注意密码里有特殊字符要 URL 编码。

### Nginx 502 Bad Gateway
- backend 没起（没放 app.jar 就不会起）或还没启动完；`curl http://backend:8080` 在 nginx 容器内测。
- Java OOM：调大 `JAVA_OPTS`，`docker logs ent-backend` 看 GC/堆。

### Nginx 413 Request Entity Too Large
- 已设 `client_max_body_size 50m`，更大文件同步调 nginx.conf 与 Java 的 `spring.servlet.multipart.max-file-size`。

### 磁盘被打满
- `docker system df` 看镜像/卷/日志占用；`docker system prune -af` 清理。
- 容器日志已限 5×50m；`./data/shared` 截图与 `backup/` 加定时清理（见 06）。
- MySQL binlog 已设 7 天自动过期；紧急清理：`PURGE BINARY LOGS BEFORE NOW() - INTERVAL 1 DAY;`。

### 容器时间不对 / 差 8 小时
- 所有镜像注入了 `TZ=Asia/Shanghai`；自建镜像记得装 tzdata。

## 4. 网络与防火墙
- 外部只能访问 80；3306/6379 只绑 127.0.0.1。要远程调试临时改 compose 绑定 `0.0.0.0` 并用**安全组限源 IP**，完事改回。
- 容器间不通：`docker network ls` / `docker network inspect ent-core`，确认服务在同一网络。
- Worker 要访问外网但服务器走代理：在 `.env` 配 `HTTP_PROXY/HTTPS_PROXY`。

## 5. 数据与密码
- **忘了密码**：`.env` 里有（安装时写入）；若 .env 丢失但数据目录还在，root 密码以库内为准，需要 `--skip-grant-tables` 重置（标准 MySQL 流程）。
- **误删 data/mysql**：只能用 backup 恢复，强调每日备份。

## 6. 一键收集诊断信息（报障时执行）
```bash
{
  echo "### compose ps"; docker compose ps -a
  echo "### docker info"; docker info
  echo "### stats"; docker stats --no-stream
  echo "### disk"; df -h
  echo "### logs"; for c in $(docker compose ps -q); do docker logs --tail 100 $c; done
} > diagnose-$(date +%F).txt 2>&1
```

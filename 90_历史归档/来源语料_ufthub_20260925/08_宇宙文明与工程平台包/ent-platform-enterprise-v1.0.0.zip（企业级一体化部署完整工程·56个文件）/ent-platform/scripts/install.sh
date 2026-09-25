#!/bin/bash
# =============================================================================
# 企业级一体化平台 —— Linux 一键部署脚本
# 兼容: Ubuntu/Debian/Kylin(麒麟)/UOS(统信)/CentOS/RHEL/openEuler
# 架构: x86_64(amd64) / aarch64(arm64 鲲鹏、飞腾) ; loongarch 见 docs/08
# 用法:
#   bash scripts/install.sh           # 在线安装
#   OFFLINE=1 bash scripts/install.sh # 离线环境(假设 docker 已装, 镜像已 load)
# =============================================================================
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"

OFFLINE="${OFFLINE:-0}"
ARCH="$(detect_arch)"

banner() {
cat <<'EOF'
============================================================
  企业级一体化平台 (Nginx + Java + MySQL + Redis
  + Python RPA Worker + Headless Browser + OCR)  一键部署
============================================================
EOF
}
banner
log "安装目录: $ROOT"
log "系统架构: $ARCH / $(detect_os)"

# ---------------------------------------------------------------- 0. 目录
step "0/7 准备数据/日志/备份目录"
mkdir -p data/mysql data/redis data/shared data/ocr-models data/static data/uploads \
         logs/nginx logs/backend logs/worker backup
ok() { log "$*"; }
ok "目录就绪"

# ---------------------------------------------------------------- 1. Docker
step "1/7 检查 Docker"
install_docker_apt() {
    log "使用 apt 安装 docker (Debian/Ubuntu/麒麟/UOS 系)"
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -y
    apt-get install -y ca-certificates curl gnupg lsb-release || true
    # 信创系统源里自带 docker.io / docker-compose-plugin, 优先用系统源, 最稳
    if apt-get install -y docker.io docker-compose-plugin 2>/dev/null; then
        :
    else
        # 回退官方源 (国内用阿里云镜像)
        install -m 0755 -d /etc/apt/keyrings
        curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/$(. /etc/os-release; echo "$ID_LIKE" | awk '{print $1}')/gpg \
            -o /etc/apt/keyrings/docker.gpg 2>/dev/null || true
        apt-get update -y && apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    fi
}
install_docker_yum() {
    log "使用 yum/dnf 安装 docker (CentOS/RHEL/openEuler 系)"
    if command -v dnf >/dev/null 2>&1; then DNF=dnf; else DNF=yum; fi
    $DNF install -y dnf-utils 2>/dev/null || true
    $DNF install -y docker docker-compose-plugin 2>/dev/null || {
        curl -fsSL https://get.docker.com | sh
    }
}

if ! command -v docker >/dev/null 2>&1; then
    [ "$OFFLINE" = "1" ] && die "离线模式要求宿主机已预装 docker"
    if command -v apt-get >/dev/null 2>&1; then
        [ "$(id -u)" = "0" ] || die "安装 docker 需要 root: sudo bash scripts/install.sh"
        install_docker_apt
    elif command -v yum >/dev/null 2>&1 || command -v dnf >/dev/null 2>&1; then
        [ "$(id -u)" = "0" ] || die "安装 docker 需要 root: sudo bash scripts/install.sh"
        install_docker_yum
    else
        die "无法识别的包管理器, 请手动安装 docker 24+ 与 compose 插件后重跑"
    fi
fi
systemctl enable docker 2>/dev/null || true
systemctl start docker 2>/dev/null || service docker start 2>/dev/null || true
docker info >/dev/null 2>&1 || die "docker 无法启动, 执行 systemctl status docker 排查"
log "Docker: $(docker --version)"

# compose 插件兜底
if ! docker compose version >/dev/null 2>&1 && ! command -v docker-compose >/dev/null 2>&1; then
    log "安装 compose 插件..."
    if command -v apt-get >/dev/null 2>&1; then apt-get install -y docker-compose-plugin || curl -fsSL https://get.docker.com | sh; fi
fi

# Docker 守护层最优默认: 日志轮转 + 国内镜像加速(只写一次, 已配置则不动)
if [ "$(id -u)" = "0" ] && [ ! -f /etc/docker/daemon.json ]; then
    step "  写入 /etc/docker/daemon.json (日志轮转+镜像加速)"
    mkdir -p /etc/docker
    cat > /etc/docker/daemon.json <<'JSON'
{
  "log-driver": "json-file",
  "log-opts": { "max-size": "50m", "max-file": "5" },
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.xuanyuan.me"
  ],
  "live-restore": true
}
JSON
    systemctl restart docker 2>/dev/null || true
fi

# ---------------------------------------------------------------- 2. .env
step "2/7 生成 .env (强密码 + 按架构选 OCR 引擎)"
gen_pwd() { openssl rand -base64 18 2>/dev/null | tr -dc 'A-Za-z0-9' | head -c 20 || echo "Pwd$(date +%s)$RANDOM"; }
if [ ! -f .env ]; then
    cp .env.example .env
    RP=$(gen_pwd); MP=$(gen_pwd); MUP=$(gen_pwd)
    # 架构适配: arm64/loong64 默认 rapid(ONNX 全兼容), x86 默认 paddle
    if [ "$ARCH" != "amd64" ]; then
        sed -i "s/^OCR_ENGINE=.*/OCR_ENGINE=rapid/" .env
        log "非 x86 架构($ARCH), OCR 引擎自动选择 rapid(ONNX Runtime, 跨架构稳定)"
    fi
    sed -i "s|^MYSQL_ROOT_PASSWORD=.*|MYSQL_ROOT_PASSWORD=${RP}|" .env
    sed -i "s|^MYSQL_PASSWORD=.*|MYSQL_PASSWORD=${MP}|" .env
    sed -i "s|^REDIS_PASSWORD=.*|REDIS_PASSWORD=${MUP}|" .env
    chmod 600 .env
    log ".env 已生成并随机化全部密码 (权限 600)"
else
    log ".env 已存在, 保留现有配置"
fi
set -a; . ./.env; set +a

# 内存自适应调优
bash scripts/tune-memory.sh || warn "内存自适应调优跳过(不影响部署)"

# ---------------------------------------------------------------- 3. 拉镜像
step "3/7 拉取基础镜像 (mysql/redis/nginx)"
compose pull mysql redis nginx || warn "部分镜像拉取失败, 若为离线/信创环境请见 docs/08"

# ---------------------------------------------------------------- 4. 构建
step "4/7 构建本地服务镜像 (OCR / Browser / Worker)"
PROFILE_ARGS=""
if [ -f backend/app.jar ]; then
    PROFILE_ARGS="--profile backend"
    log "检测到 backend/app.jar, 将一并构建 Java 后端"
else
    warn "未发现 backend/app.jar, 跳过 Java 后端 (其余服务正常启动)"
fi
compose ${PROFILE_ARGS} build

# ---------------------------------------------------------------- 5. 启动
step "5/7 启动全部容器"
compose ${PROFILE_ARGS} up -d

# ---------------------------------------------------------------- 6. 健康等待
step "6/7 等待健康检查 (最长 120s)"
for i in $(seq 1 24); do
    sleep 5
    HEALTH=$(compose ps --format '{{.Service}}:{{.State}}:{{.Health}}' 2>/dev/null | tr '\n' ' ')
    echo "  [$((i*5))s] $HEALTH"
    if compose ps 2>/dev/null | grep -qiE 'restarting|exited'; then
        ERR_SVC=$(compose ps --format '{{.Service}} {{.State}}' | grep -iE 'restart|exit' || true)
        warn "存在异常容器: $ERR_SVC (docs/07 故障排查)"
    fi
    echo "$HEALTH" | grep -q mysql && echo "$HEALTH" | grep -q redis && break
done

# ---------------------------------------------------------------- 7. 汇总
step "7/7 部署完成"
compose ps
cat <<EOF

${C_GREEN}${C_BOLD}==================== 部署结果 ====================${C_NC}
  安装目录      : $ROOT
  配置文件      : $ROOT/.env (改完执行 bash scripts/control.sh restart)
  Nginx 入口    : http://<服务器IP>:${HTTP_PORT:-80}
  健康检查      : curl http://127.0.0.1:${HTTP_PORT:-80}/healthz
  MySQL(仅本机) : 127.0.0.1:${MYSQL_PORT:-3306}  root 密码见 .env
  Redis(仅本机) : 127.0.0.1:${REDIS_PORT:-6379}  密码见 .env
  OCR 引擎      : ${OCR_ENGINE} (内部 http://ocr:8000, 不对外)
  浏览器 CDP    : 内部 http://browser:9222 (不对外)

  常用命令:
    bash scripts/control.sh status   # 状态
    bash scripts/control.sh logs -f  # 日志
    bash scripts/control.sh restart  # 重启
    bash scripts/control.sh stop     # 停止
    bash scripts/backup.sh           # 数据备份
  投递测试任务:
    docker exec -it ent-redis redis-cli -a "\$REDIS_PASSWORD" \\
        LPUSH ${TASK_QUEUE:-rpa:tasks} "\$(cat worker/app/task_example.json)"
${C_GREEN}${C_BOLD}==================================================${C_NC}
EOF

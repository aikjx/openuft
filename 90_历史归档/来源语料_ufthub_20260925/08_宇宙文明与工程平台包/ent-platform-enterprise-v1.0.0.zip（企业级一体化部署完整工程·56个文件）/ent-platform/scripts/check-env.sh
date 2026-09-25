#!/bin/bash
# =============================================================================
# 环境自检: OS/架构、Docker、Compose、磁盘、内存、端口占用、GPU
# 用法: bash scripts/check-env.sh
# =============================================================================
set -u
source "$(dirname "$0")/lib/common.sh"

PASS=0; FAIL=0
ok()   { echo -e "  ${C_GREEN}[√]${C_NC} $*"; PASS=$((PASS+1)); }
bad()  { echo -e "  ${C_RED}[×]${C_NC} $*"; FAIL=$((FAIL+1)); }
info() { echo -e "  ${C_BLUE}[i]${C_NC} $*"; }

step "1. 系统信息"
ARCH="$(detect_arch)"; OS="$(detect_os)"
info "架构: ${ARCH}    系统: ${OS}    内核: $(uname -r)"
case "$ARCH" in
    amd64|arm64) ok "官方镜像原生支持 ${ARCH}" ;;
    loong64)     bad "LoongArch 需使用信创镜像源, 见 docs/08 (不能直接拉 DockerHub 官方镜像)" ;;
    *)           warn "架构 $ARCH 兼容性需人工确认, 见 docs/08" ;;
esac

step "2. CPU / 内存 / 磁盘"
CPU_N=$(nproc 2>/dev/null || echo "?")
MEM_MB=$(awk '/MemTotal/{printf "%d", $2/1024}' /proc/meminfo 2>/dev/null || echo "?")
info "CPU 核数: ${CPU_N}    内存: ${MEM_MB} MB"
[ "${MEM_MB:-0}" -ge 3500 ] 2>/dev/null && ok "内存 >= 4G, 满足全量组件" || bad "内存 < 4G, 建议关闭部分组件或加内存(最低 2G 跑精简版)"
DISK_AVAIL=$(df -Pm "$ROOT" | awk 'NR==2{print $4}')
info "安装目录可用磁盘: ${DISK_AVAIL} MB"
[ "${DISK_AVAIL:-0}" -ge 20480 ] && ok "磁盘可用 >= 20G" || bad "磁盘可用 < 20G, 镜像+数据可能不足"

step "3. Docker"
if command -v docker >/dev/null 2>&1; then
    ok "docker 已安装: $(docker --version)"
    if docker info >/dev/null 2>&1; then
        ok "docker 守护进程运行中"
        info "存储驱动: $(docker info 2>/dev/null | awk '/Storage Driver/{print $3}')"
    else
        bad "docker 已装但未运行 -> systemctl start docker"
    fi
    if docker compose version >/dev/null 2>&1; then
        ok "compose v2: $(docker compose version --short)"
    elif command -v docker-compose >/dev/null 2>&1; then
        ok "docker-compose v1: $(docker-compose --version | awk '{print $NF}')"
    else
        bad "缺少 compose 插件"
    fi
else
    bad "未安装 docker (install.sh 可自动安装)"
fi

step "4. GPU (可选)"
if command -v nvidia-smi >/dev/null 2>&1; then
    ok "检测到 NVIDIA GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null)"
    docker info 2>/dev/null | grep -qi runtime=nvidia \
        && ok "nvidia-container-toolkit 已就绪 (USE_GPU=1 启用)" \
        || bad "未检测到 nvidia-container runtime, 见 docs/04 GPU 章节"
else
    info "无 NVIDIA GPU, 使用 CPU 模式 (正常)"
fi

step "5. 端口占用检查"
for p in 80 3306 6379; do
    if ss -lnt 2>/dev/null | awk '{print $4}' | grep -qE "[:.]${p}\$"; then
        bad "端口 ${p} 已被占用 (改 .env 中对应 PORT)"
    else
        ok "端口 ${p} 空闲"
    fi
done

step "6. 工程文件完整性"
for f in docker-compose.yml .env.example mysql/conf/my.cnf redis/conf/redis.conf \
         nginx/nginx.conf ocr/Dockerfile browser/Dockerfile worker/Dockerfile; do
    [ -f "$ROOT/$f" ] && ok "$f" || bad "缺失 $f"
done

echo
if [ "$FAIL" -eq 0 ]; then
    echo -e "${C_GREEN}${C_BOLD}自检通过: ${PASS} 项正常, 可以执行 bash scripts/install.sh${C_NC}"
    exit 0
else
    echo -e "${C_YELLOW}${C_BOLD}自检完成: ${PASS} 正常 / ${FAIL} 异常, 请先处理上述 [×] 项${C_NC}"
    exit 1
fi

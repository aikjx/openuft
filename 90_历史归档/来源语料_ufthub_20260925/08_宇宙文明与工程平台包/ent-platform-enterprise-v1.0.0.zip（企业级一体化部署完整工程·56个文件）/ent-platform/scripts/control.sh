#!/bin/bash
# =============================================================================
# 统一运维控制脚本
# 用法: bash scripts/control.sh <start|stop|restart|status|ps|logs|down|up|pull>
# 例 : bash scripts/control.sh logs -f worker
# =============================================================================
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"
require_docker
load_env

ACTION="${1:-status}"
shift || true
PROFILE_ARGS="$(backend_profile_args)"

case "$ACTION" in
  up|start)
    compose ${PROFILE_ARGS} up -d "$@"
    compose ps
    ;;
  stop)      compose stop "$@" ;;
  down)      compose down "$@" ;;                 # 保留数据卷
  restart)
    compose ${PROFILE_ARGS} restart "$@"
    compose ps
    ;;
  status|ps) compose ps "$@" ;;
  logs)      compose logs --tail=200 "$@" ;;
  top)       docker stats --no-stream $(docker compose ps -q) ;;
  pull)
    compose pull mysql redis nginx
    compose ${PROFILE_ARGS} build --pull
    ;;
  rebuild)   # 改完 Dockerfile/代码后重新构建并滚动
    compose ${PROFILE_ARGS} build "$@"
    compose ${PROFILE_ARGS} up -d "$@"
    ;;
  shell)     # 进容器排障: control.sh shell ocr
    SVC="${1:-worker}"; compose exec "$SVC" bash 2>/dev/null || compose exec "$SVC" sh
    ;;
  *)
    cat <<EOF
用法: bash scripts/control.sh <命令> [参数]
  start           启动全部
  stop            停止全部(容器保留)
  restart [服务]  重启(可指定单个服务)
  status          查看容器状态
  logs [-f] [服务]查看日志
  top             查看实时资源占用快照
  down            下线(数据保留在 ./data)
  rebuild [服务]  改代码后重新构建并上线
  shell <服务>    进入容器
  pull            更新基础镜像并重建本地镜像
EOF
    exit 1
    ;;
esac

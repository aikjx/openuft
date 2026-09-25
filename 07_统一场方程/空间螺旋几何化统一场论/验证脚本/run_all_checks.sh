#!/usr/bin/env bash
# 空间螺旋几何化统一场论 · 一键批量校验（bash 入口）
# 用法：bash run_all_checks.sh [--stdout]
# 依赖：Python 3.8+（仅标准库），无需第三方包

set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PY=""
for cand in python3 python py; do
    if command -v "$cand" >/dev/null 2>&1; then
        PY="$cand"
        break
    fi
done

if [ -z "$PY" ]; then
    echo "[FATAL] 未找到 python3 / python / py 命令" >&2
    exit 127
fi

echo "[info] interpreter: $("$PY" --version 2>&1)"
cd "$HERE" || exit 1

"$PY" run_all_checks.py "$@"
rc=$?

if [ $rc -ne 0 ]; then
    echo "[FATAL] 校验脚本异常退出，退出码=$rc" >&2
    exit $rc
fi

echo "[ok] 报告已生成：$HERE/audit_report.md"
exit 0

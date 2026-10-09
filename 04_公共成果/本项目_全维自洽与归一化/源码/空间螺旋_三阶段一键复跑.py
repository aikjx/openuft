# -*- coding: utf-8 -*-
"""
空间螺旋审计 · 三阶段一键复跑
==============================

把三个阶段引擎串成一条命令，聚合退出码（任一失败即非零）——沿用本仓库
`验证脚本/run_all_checks.py` 的既有惯例，避免"逐个手敲三个命令、漏跑一个还以为是绿的"。

阶段
----
1. 空间螺旋修复版_第一性审计与伪派生判定.py        （自检 13/13；判定 35 条）
2. 空间螺旋修复版_最小修复闭环与继承缺陷审计.py      （自检 8/8；判定 10 条）
3. 空间螺旋判定_总览与防回潮守卫.py                 （守卫 8/8；退出码 1 可作门禁）

用法
----
    python 空间螺旋_三阶段一键复跑.py            # 全量输出
    python 空间螺旋_三阶段一键复跑.py --quiet    # 只打印汇总（CI 友好）
    python 空间螺旋_三阶段一键复跑.py --tail 15  # 每阶段只打印末 15 行

退出码：0 = 三阶段全部通过；非零 = 首个失败阶段的退出码（便于 CI 定位）
"""

import io
import os
import re
import sys
import time
import subprocess

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))

STAGES = [
    ("S1 第一性审计与伪派生判定", "空间螺旋修复版_第一性审计与伪派生判定.py"),
    ("S2 最小修复闭环与继承缺陷", "空间螺旋修复版_最小修复闭环与继承缺陷审计.py"),
    ("S3 总览与防回潮守卫", "空间螺旋判定_总览与防回潮守卫.py"),
]

# 从各引擎输出里抽取判定的正则（引擎自身的汇总行格式）
PAT_SELFCHECK = re.compile(r"自检\s+(\d+)/(\d+)")
PAT_VERDICT = re.compile(r"判定\s+总数=(\d+)\s+PASS=(\d+)\s+FAIL=(\d+)\s+BOUNDARY=(\d+)\s+INFO=(\d+)")
PAT_GUARD = re.compile(r"守卫\s+(\d+)/(\d+)\s+通过")


def run_stage(name, script, quiet, tail):
    path = os.path.join(HERE, script)
    if not os.path.isfile(path):
        return {"name": name, "script": script, "rc": 127, "out": "脚本不存在：" + path,
                "secs": 0.0, "summary": "缺失"}
    t0 = time.time()
    proc = subprocess.run([sys.executable, "-B", path], cwd=HERE,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    secs = time.time() - t0
    out = proc.stdout.decode("utf-8", errors="replace")

    lines = out.splitlines()
    if not quiet:
        print("-" * 76)
        print("▶ " + name + "（" + script + "）")
        print("-" * 76)
        body = lines if tail <= 0 else lines[-tail:]
        for ln in body:
            print(ln)

    summary = []
    m = PAT_SELFCHECK.search(out)
    if m:
        summary.append("自检 " + m.group(1) + "/" + m.group(2))
    m = PAT_VERDICT.search(out)
    if m:
        summary.append("判定 %s 条（PASS %s / FAIL %s / BOUNDARY %s / INFO %s）"
                       % (m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)))
    m = PAT_GUARD.search(out)
    if m:
        summary.append("守卫 " + m.group(1) + "/" + m.group(2) + " 通过")
    return {"name": name, "script": script, "rc": proc.returncode, "out": out,
            "secs": secs, "summary": "；".join(summary) if summary else "（未识别到汇总行）"}


def main():
    args = sys.argv[1:]
    quiet = "--quiet" in args
    tail = 0
    if "--tail" in args:
        try:
            tail = int(args[args.index("--tail") + 1])
        except (IndexError, ValueError):
            tail = 0

    print("=" * 76)
    print("空间螺旋审计 · 三阶段一键复跑")
    print("解释器：" + sys.executable)
    print("=" * 76)

    results = [run_stage(n, s, quiet, tail) for n, s in STAGES]

    print("\n" + "=" * 76)
    print("汇总")
    print("=" * 76)
    print("%-26s %-8s %-8s %s" % ("阶段", "退出码", "耗时", "识别到的汇总"))
    for r in results:
        print("%-26s %-8d %-8s %s" % (r["name"], r["rc"], "%.1fs" % r["secs"], r["summary"]))

    failed = [r for r in results if r["rc"] != 0]
    total = sum(r["secs"] for r in results)
    print("-" * 76)
    if failed:
        print("结果：FAIL —— %d/%d 阶段失败（首个失败：%s，退出码 %d）"
              % (len(failed), len(results), failed[0]["name"], failed[0]["rc"]))
        for r in failed:
            print("  失败阶段 " + r["script"] + " 的输出尾部：")
            for ln in r["out"].splitlines()[-12:]:
                print("    " + ln)
        print("总耗时 %.1f s" % total)
        return failed[0]["rc"]
    print("结果：PASS —— %d/%d 阶段全部通过 | 总耗时 %.1f s" % (len(results), len(results), total))
    print("（S3 的退出码 1 表示检测到「已判 falsified 的主张被改回」——门禁报警，请勿忽略）")
    return 0


if __name__ == "__main__":
    sys.exit(main())

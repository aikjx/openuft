# -*- coding: utf-8 -*-
"""
空间螺旋 V21 拟合层 · 一键复跑（可复跑，CI 友好）
================================================

为什么单独一个入口
------------------
既有三处门禁各有自己的对象，本册**不改任何一处**：

    `空间螺旋_三阶段一键复跑.py`   —— 空间螺旋体系门禁（不碰）
    `靶场统计层_一键复跑.py`       —— 联盟级**读数层**（χ² / p / δ_min；不估参数）
   本文件                          —— 联盟级**拟合层**（参数估计 + 协方差；V21 专项）

两阶段（串行，聚合退出码）
--------------------------
    S1  读数  `空间螺旋V21_水星与精细结构_卡方联合拟合.py`
    S2  门禁  `空间螺旋V21_水星与精细结构_卡方联合拟合.py --teeth`

S2 非零 ⇒ 汇总退出码非零（牙齿有 MISSED 即报警，请勿忽略）。

用法：
    python 空间螺旋V21_拟合层_一键复跑.py
    python 空间螺旋V21_拟合层_一键复跑.py --quiet
    python 空间螺旋V21_拟合层_一键复跑.py --tail 40
"""

import os
import re
import sys
import subprocess
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable

STAGES = [
    ("S1 拟合层读数", ["空间螺旋V21_水星与精细结构_卡方联合拟合.py"]),
    ("S2 拟合层牙齿门禁", ["空间螺旋V21_水星与精细结构_卡方联合拟合.py", "--teeth"]),
]

# 从各阶段输出里抽取摘要行（正则按引擎的实际打印格式）
SUMMARY_PATTERNS = [
    re.compile(r"^  判定：总数.*$", re.M),
    re.compile(r"^  牙齿：.*$", re.M),
    re.compile(r"^  产出：.*$", re.M),
    re.compile(r"^  χ²_min = .*$", re.M),
]


def run_stage(name, args):
    t0 = time.time()
    proc = subprocess.run([PY, "-B"] + args, cwd=HERE,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = proc.stdout.decode("utf-8", errors="replace")
    hits = []
    for pat in SUMMARY_PATTERNS:
        hits.extend(m.strip() for m in pat.findall(out))
    return {"name": name, "code": proc.returncode,
            "seconds": time.time() - t0, "out": out, "hits": hits}


def main():
    quiet = "--quiet" in sys.argv
    tail = 0
    if "--tail" in sys.argv:
        try:
            tail = int(sys.argv[sys.argv.index("--tail") + 1])
        except (IndexError, ValueError):
            tail = 20

    print("=" * 78)
    print("空间螺旋 V21 拟合层 · 一键复跑")
    print("解释器：" + PY)
    print("=" * 78)

    results = []
    for name, args in STAGES:
        print("\n---- %s ----" % name)
        r = run_stage(name, args)
        results.append(r)
        if not quiet:
            lines = r["out"].rstrip("\n").split("\n")
            show = lines if tail == 0 else lines[-tail:]
            for line in show:
                print(line)
        else:
            for h in r["hits"]:
                print("  " + h)
            print("  退出码 %d | 用时 %.1fs" % (r["code"], r["seconds"]))

    print("\n" + "=" * 78)
    print("汇总")
    print("=" * 78)
    print("%-20s %-8s %-10s %s" % ("阶段", "退出码", "耗时", "识别到的汇总"))
    for r in results:
        print("%-20s %-8d %-10s %s"
              % (r["name"], r["code"], "%.1fs" % r["seconds"],
                 "；".join(r["hits"]) if r["hits"] else "—"))
    print("-" * 78)
    bad = [r for r in results if r["code"] != 0]
    total = sum(r["seconds"] for r in results)
    if bad:
        print("结果：FAIL —— %d/%d 阶段失败（%s）| 总耗时 %.1fs"
              % (len(bad), len(results), "、".join(r["name"] for r in bad), total))
        return 1
    print("结果：PASS —— %d/%d 阶段全部通过 | 总耗时 %.1fs" % (len(results), len(results), total))
    print("（S2 非零表示牙齿有 MISSED —— 统计量本身可疑，门禁报警，请勿忽略）")
    return 0


if __name__ == "__main__":
    sys.exit(main())

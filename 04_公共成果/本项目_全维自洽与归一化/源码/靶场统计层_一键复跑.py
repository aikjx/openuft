# -*- coding: utf-8 -*-
"""
靶场统计层 · 一键复跑（可复跑，CI 友好）
========================================

为什么单独一个入口
------------------
`空间螺旋_三阶段一键复跑.py` 是**该体系**（空间螺旋几何化统一场论）的门禁，已 3/3 全绿；
本册是**联盟级统计层**，服务全部 19 个体系的靶场登记，两者对象不同。
**不改动既有门禁**（避免把它从 3/3 变成 4/4 而影响历史记录），故另起一个入口。

四阶段（串行，聚合退出码）
--------------------------
  S1  上游靶表真源 `无量纲靶场审计.py`   —— 确认 10 靶表未被改动（统计层不复制靶表）
  S2  `靶场卡方联合拟合_统计层与判决力读数.py`          —— 产出读数
  S3  `靶场卡方联合拟合_统计层与判决力读数.py --teeth`  —— 牙齿门禁（10 项必须全 CAUGHT/CLEAN）
  S4  `靶场登记列校验_写入侧门禁.py --check`            —— 登记列写入侧门禁（相对基线**只许不增**）

任一阶段非零 ⇒ 汇总退出码非零。

用法：
    python 靶场统计层_一键复跑.py
    python 靶场统计层_一键复跑.py --quiet
    python 靶场统计层_一键复跑.py --tail 40
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
    ("S1 上游靶表真源", ["无量纲靶场审计.py"]),
    ("S2 卡方统计层读数", ["靶场卡方联合拟合_统计层与判决力读数.py"]),
    ("S3 牙齿门禁", ["靶场卡方联合拟合_统计层与判决力读数.py", "--teeth"]),
    ("S4 登记列写入侧门禁", ["靶场登记列校验_写入侧门禁.py", "--check"]),
]

# 从各阶段输出里抽取摘要行（正则按各脚本的实际打印格式；多行匹配取最后一条）
SUMMARY_PATTERNS = [
    re.compile(r"^  判定：总数.*$", re.M),
    re.compile(r"^  牙齿：.*$", re.M),
    re.compile(r"^  产出：.*$", re.M),
    re.compile(r"^  结论：.*$", re.M),
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
    print("靶场统计层 · 一键复跑")
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
    print("%-22s %-8s %-10s %s" % ("阶段", "退出码", "耗时", "识别到的汇总"))
    for r in results:
        print("%-22s %-8d %-10s %s"
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
    print("（S3 非零表示牙齿有 MISSED —— 统计量本身可疑；"
          "S4 非零表示登记列**新增**违规 —— 两者都是门禁报警，请勿忽略）")
    return 0


if __name__ == "__main__":
    sys.exit(main())

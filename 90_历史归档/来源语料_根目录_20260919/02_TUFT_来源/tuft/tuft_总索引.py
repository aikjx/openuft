# -*- coding: utf-8 -*-
"""
TUFT 全景索引（可复跑）
=======================
扫描 tuft/ 下全部脚本与报告，提取每份报告的判定统计（PASS/FAIL/BOUNDARY/INFO），
生成索引文件 tuft_总索引.md，便于交付与复核。
红线：数学自洽 != 实验证实。
"""
from __future__ import print_function

import os
import re
import glob
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "tuft_总索引.md")


def parse_counts(text):
    """鲁棒读取：优先汇总行（PASS = N）；无汇总行时回退统计行内 [PASS] 标记。

    修复盲点：r3/r4/knot_slsqp 等报告只有行内标记、无汇总行，旧版会被静默跳过。
    """
    counts = {}
    for m in re.finditer(r"(PASS|FAIL|BOUNDARY|INFO)\s*[=:]\s*(\d+)", text):
        counts[m.group(1)] = int(m.group(2))
    if counts:
        return counts
    c = {}
    for k in ("PASS", "FAIL", "BOUNDARY", "INFO"):
        c[k] = len(re.findall(r"\[\s*%s[^\]]*\]" % k, text))
    return c


def main():
    scripts = sorted(glob.glob(os.path.join(HERE, "*.py")))
    reports = sorted(glob.glob(os.path.join(HERE, "*_report.txt")))
    mds = sorted(glob.glob(os.path.join(HERE, "*.md")))

    rows = []
    total = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for rp in reports:
        try:
            text = open(rp, encoding="utf-8").read()
        except Exception:
            continue
        c = parse_counts(text)
        if not c:
            continue
        rows.append((os.path.basename(rp), c))
        for k in total:
            total[k] += c.get(k, 0)

    md = []
    md.append("# TUFT 全景索引\n")
    md.append("> 自动扫描生成（`tuft_总索引.py`）。红线：数学自洽 != 实验证实。\n")

    md.append("## 一、报告判定统计汇总\n")
    md.append("| 报告 | PASS | FAIL | BOUNDARY | INFO |")
    md.append("|---|---|---|---|---|")
    for name, c in rows:
        md.append("| %s | %d | %d | %d | %d |" % (
            name, c.get("PASS", 0), c.get("FAIL", 0), c.get("BOUNDARY", 0), c.get("INFO", 0)))
    md.append("| **合计** | **%d** | **%d** | **%d** | **%d** |" % (
        total["PASS"], total["FAIL"], total["BOUNDARY"], total["INFO"]))
    md.append("")

    md.append("## 二、脚本清单（%d）\n" % len(scripts))
    for s in scripts:
        md.append("- `%s`" % os.path.basename(s))
    md.append("")

    md.append("## 三、报告文档清单（%d）\n" % len(mds))
    for s in mds:
        md.append("- `%s`" % os.path.basename(s))
    md.append("")

    md.append("## 四、原始报告（txt，%d）\n" % len(reports))
    for s in reports:
        md.append("- `%s`" % os.path.basename(s))
    md.append("")

    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")

    print("已生成: " + OUT_PATH)
    print("报告数 %d；合计 PASS=%d FAIL=%d BOUNDARY=%d INFO=%d" % (
        len(rows), total["PASS"], total["FAIL"], total["BOUNDARY"], total["INFO"]))
    for name, c in rows:
        print("  %-44s P=%d F=%d B=%d I=%d" % (
            name, c.get("PASS", 0), c.get("FAIL", 0), c.get("BOUNDARY", 0), c.get("INFO", 0)))


if __name__ == "__main__":
    main()

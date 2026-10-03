# -*- coding: utf-8 -*-
"""扫描引号奇偶，定位吞掉代码的未闭合字符串。"""
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

p = sys.argv[1] if len(sys.argv) > 1 else "29_作用量变分审计_耦合能动张量与迹_2026-10-03.py"
lines = open(p, encoding="utf-8").read().split("\n")
for i, ln in enumerate(lines, 1):
    # 去掉三引号再数字符
    t = ln.replace('"""', "").replace("'''", "")
    nq = t.count('"') + t.count("'")
    if nq % 2 == 1:
        print(i, nq, ln[:100])

# -*- coding: utf-8 -*-
"""在完整语句边界上二分定位（跳过模块 docstring 未闭合的前缀）。"""
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

p = sys.argv[1] if len(sys.argv) > 1 else "29_作用量变分审计_耦合能动张量与迹_2026-10-03.py"
lines = open(p, encoding="utf-8").read().replace("\r\n", "\n").split("\n")
# 找到模块 docstring 结束行
start = 0
for i in range(1, len(lines)):
    if lines[i].strip() == '"""':
        start = i + 1
        break
print("docstring ends at line", start + 1)

bad = None
for i in range(start + 1, len(lines) + 1):
    src = "\n".join(lines[:i])
    try:
        compile(src, p, "exec")
    except SyntaxError as e:
        bad = i
        print("FIRST BAD PREFIX END:", i, "| err:", e.msg, "at line", e.lineno)
        break
if bad:
    lo = start + 1
    hi = bad
    # 逐行回退，找出引入错误的那一行
    for i in range(lo, bad + 1):
        src = "\n".join(lines[:i])
        try:
            compile(src, p, "exec")
        except SyntaxError:
            print("CULPRIT LINE:", i)
            for k in range(max(0, i - 4), min(len(lines), i + 2)):
                print("   ", k + 1, repr(lines[k]))
            break
else:
    print("no syntax error")

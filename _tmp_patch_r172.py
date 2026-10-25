# -*- coding: utf-8 -*-
import io
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

P = (r"d:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/源码/"
     "TUFT-r172_光速飞行器动力学方程_定义重排与三重硬伤_精算_2026-10-24.py")

s = io.open(P, encoding="utf-8").read()

pairs = [
    ('/ r170（本卷）', '/ r172（本卷）'),
    ('_tmp_ctrl_u7_r170.py', '_tmp_ctrl_u7_r172.py'),
    ('"id": "TUFT-r170"', '"id": "TUFT-r172"'),
    ('Rl.append("TUFT-r170 报告")', 'Rl.append("TUFT-r172 报告")'),
    ('print(" TUFT-r170｜', 'print(" TUFT-r172｜'),
]

for a, b in pairs:
    n = s.count(a)
    print("{}  <- {}".format(n, b[:44]))
    s = s.replace(a, b)

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("left r170 count =", s.count("r170"))

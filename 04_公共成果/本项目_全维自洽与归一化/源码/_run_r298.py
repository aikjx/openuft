# -*- coding: utf-8 -*-
"""r298 runner（复现入口）—— ROOT V15.0 六维 Einstein–Maxwell 磁通稳定化与 α 关系审计
（本 runner 指向 r298 先到卷；2026-11-01 碰撞治理：曾被并行后到卷（现 r299）误覆，已按先占四件套者权威纪律恢复指向本卷引擎）"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r298_ROOTV15六维EinsteinMaxwell磁通稳定化与alpha关系审计_独立重推与N两难定理与Lambda6微调_精算与可视化_2026-11-01.py")
OUT = os.path.join(SRC, "_out_r298.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-5000:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)

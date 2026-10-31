# -*- coding: utf-8 -*-
"""r263 runner（复现入口）"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r263_攻坚任务书审计_可证伪预言与GW170817裁定_"
        "R等于αλ除2π复现与轴向延迟逐位对拍与literal-helix排除因子6.3e10_"
        "精算与可视化_2026-10-31.py")
PY = sys.executable
OUT = os.path.join(SRC, "_out_r263.txt")

p = subprocess.run([PY, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-7000:])
print("RC=", p.returncode)

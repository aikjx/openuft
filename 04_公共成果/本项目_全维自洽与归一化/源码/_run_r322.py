# -*- coding: utf-8 -*-
"""r322 runner —— X-R318-1 审计 · 真几何扭转模式约束与 NO-GO 存活检验"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r322_XR318-1审计_真几何扭转模式约束与NO-GO存活检验_"
        "精算与可视化_2026-11-01.py")
OUT = os.path.join(SRC, "_out_r322.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-6000:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)

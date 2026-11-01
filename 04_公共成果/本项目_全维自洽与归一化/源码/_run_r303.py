# -*- coding: utf-8 -*-
"""r303 runner（复现入口）—— ROOT V19 非阿贝尔规范统一与 α 本源来料审计"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r303_ROOTV19非阿贝尔规范统一与alpha本源审计_SU5归一化与三耦合运行_"
        "精算与可视化_2026-11-01.py")
OUT = os.path.join(SRC, "_out_r303.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-5000:])
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)

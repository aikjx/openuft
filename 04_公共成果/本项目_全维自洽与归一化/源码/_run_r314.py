# -*- coding: utf-8 -*-
"""r314 runner（复现入口）—— ROOT V21 固定点机制独立复核（含对表并发卷 r313）"""
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r314_ROOTV21固定点机制独立复核与截断自等价定理与f0可证伪窗口与记忆擦除律与格点基准率"
        "与六格门禁_精算与可视化_2026-11-01.py")
OUT = os.path.join(SRC, "_out_r314.txt")

p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-6000:].encode("ascii", "backslashreplace").decode("ascii"))
print("RC=", p.returncode)
sys.exit(0 if p.returncode == 0 else 1)

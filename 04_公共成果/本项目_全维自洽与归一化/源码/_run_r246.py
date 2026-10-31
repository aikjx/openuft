# -*- coding: utf-8 -*-
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r246_观测统计层_TUFT3S贝叶斯MCMC联合后验_"
        "源码AST量纲与似然三重审计_PPN可行体积归零与gamma提取解耦_"
        "精算与可视化_2026-10-31.py")
PY = sys.executable
OUT = os.path.join(SRC, "_out_r246.txt")

p = subprocess.run([PY, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-7000:])
print("RC=", p.returncode)

# -*- coding: utf-8 -*-
# ASCII runner：中文路径只出现在脚本内部，不进 argv
import io
import os
import subprocess
import sys

SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = ("TUFT-r253_力的无模型定理层_通量守恒与传播子极点及自旋符号与软定理普适性"
        "_七靶大统一方程判决_精算与可视化_2026-10-31.py")
PY = sys.executable
OUT = os.path.join(SRC, "_out_r253.txt")

p = subprocess.run([PY, os.path.join(SRC, NAME)], cwd=SRC,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-12000:])
print("RC=", p.returncode)

# -*- coding: utf-8 -*-
"""r282 runner（复现入口；三次让号竞态后落定）"""
import io, os, subprocess, sys
SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = "TUFT-r282_Φ曲线双端解析锚定与四体系闭合_接触极限解析链与Φ无穷等于α平方除20_精算与可视化_2026-10-31.py"
OUT = os.path.join(SRC, "_out_r282.txt")
p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-4400:])
print("RC=", p.returncode)

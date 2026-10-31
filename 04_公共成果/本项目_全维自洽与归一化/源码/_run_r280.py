# -*- coding: utf-8 -*-
"""r280 runner（复现入口；二次让号竞态后落定）"""
import io, os, subprocess, sys
SRC = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码"
NAME = "TUFT-r280_方法全谱总攻与VP标度函数曲线_十方法族普查与九点x全谱与Z普适性机检_精算与可视化_2026-10-31.py"
OUT = os.path.join(SRC, "_out_r280.txt")
p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(SRC, NAME)], cwd=SRC, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
txt = p.stdout.decode("utf-8", "replace")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(txt)
print(txt[-4600:])
print("RC=", p.returncode)
